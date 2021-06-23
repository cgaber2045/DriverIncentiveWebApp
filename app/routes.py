from app import app
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import Response
from datetime import date
from io import StringIO, BytesIO
from decimal import Decimal
from functools import reduce
from app.database.db_functions import *
from app.database.db_users import *
from app.database.db_connection import *
from flask.json import JSONEncoder
from tempfile import TemporaryFile
from app.products.etsy_driver import EtsyController
from app.products.catalog import CatalogController
from app.reports.reporting import ReportController
import datetime
import json
import time
import csv
import calendar

# Using this to encode our class to store user data
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AbsUser):
            return obj.__dict__
        else:
            return ""
            #JSONEncoder.default(self, obj)

# Set default JSON encoder for Flask to allow for classes
app.json_encoder = CustomJSONEncoder

# Chooses a class to use for User
userInfo = Driver()

#Message for alerts
Message = ""

def permissionCheck(allowedRole):
    global userInfo
    suspendedUsers = Admin().get_suspended_users()

    if userInfo.getUsername() == 'NULL':
        if session['userInfo']['properties']['role'] == "admin": 
            userInfo = Admin()
        elif session['userInfo']['properties']['role'] == "sponsor":
            userInfo = Sponsor()
        else:
            userInfo = Driver()

    try:
        userInfo.populate(session['userInfo']['properties']['user'])

    except Exception as e:
        session['logged_in'] = False
        return redirect(url_for('home'))

    if userInfo.getUsername() in suspendedUsers:
        session['logged_in'] = False
        return redirect(url_for('home'))

    if not session['userInfo']['properties']['role'] in allowedRole:
        return False


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
# Check if uploaded file is an acceptable file format
def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Create temporary file to send to DB driver
def upload_file(f):
    """ Expect f to be the file-like from the form input """
    tempf = TemporaryFile()
    f.save(tempf)
    # Send tempf to driver
    tempf.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    # Using the global class to access data
    global userInfo
    global Message
    #test()
    if not session.get('logged_in'):
        return render_template('landing/login.html')
    else:
        permissionCheck(["driver", "sponsor", "admin"])

        # Messages to be displayed in banner
        inbox_list = userInfo.get_inbox_list()
        if 'System' in inbox_list and len(inbox_list) == 1:
            Message = "You have an important message from our System Management"
        elif 'System' in inbox_list and len(inbox_list) > 1:
            Message = 'You have an important message from our System Management and ' + str(len(inbox_list) - 1) + ' other unread messages'
        elif len(inbox_list) > 0:
            Message = "You have " + str(len(inbox_list)) + ' unread messages'
        else:
            Message = ""

        if session['userInfo']['properties']['role'] == "driver" or session['sandbox'] == 'driver':

            # Product page information
            recommended = []
            genres = []
            popitems = []
            numproducts = 0
            userid = session['userInfo']['properties']['id']

            if not session['userInfo']['properties']['selectedSponsor'] == None:
                genres = getgenres()
                sponsorId = session['userInfo']['properties']['selectedSponsor'][0]
                recommended = recommend(userid, sponsorId)
                numproducts = getnumproducts(sponsorId)
                popitems = getpopitems(sponsorId)
                convert = get_point_value(sponsorId)
                
                # Added left side of and to check if an empty list is returned
                if recommended and recommended != ' ':
                    recommended[0]['price'] = int(recommended[0]['price']/convert)
                if popitems != ' ':
                    for row in popitems:
                            if row != ' ':
                                row['price'] = int(row['price']/convert)
            else:
                sponsorId = None

            return render_template('driver/driverHome.html', head = Message, genres = genres, resultrec = recommended, numprod = numproducts, popular = popitems, curspon= sponsorId)

        if session['userInfo']['properties']['role'] == "sponsor" or session['sandbox'] == 'sponsor':
            # Tally up expenses for sponsor
            cont = ReportController()
            now = date.today()
            sid = session['userInfo']['properties']['id']
            start = datetime.datetime(now.year, 1, 1)
            end = datetime.datetime(now.year, 12, 31)
            stats = cont.sponsor_stats(sid, (start, end))
            del cont
            expenses = reduce(lambda x,y: x + y, stats.values())

            return render_template('sponsor/sponsorHome.html', head = Message, expenses=expenses)

        if session['userInfo']['properties']['role'] == "admin":
            sponsors = Sponsor().get_users()
            sponsors = list(map(lambda x: (x[0], x[2]), sponsors))
            return render_template('admin/adminHome.html', head = Message, sponsors=sponsors)

    return render_template('landing/login.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    session['sandbox'] = None
    session.modified = True
    # Using the global class to access data
    global userInfo
    suspendedUsers = Admin().get_suspended_users()
    # Get user input from web page
    username = request.form['username']
    pwd = request.form['password']

    # Do basic login verification
    if not username_exist(username):
        flash('Incorrect login credentials!')
    elif not isActive(username):
        flash("This account has been disabled! Please contact us if you think this is a mistake.")
    elif username in suspendedUsers:
        flash('Your account is currently suspended! Please contact us if you think this is a mistake.')
    else:
        current_hash = get_password(username)
        if check_password_hash(current_hash, pwd):
            session['logged_in'] = True
            session.modified = True
            # Sets the class based on which user role
            id, role = get_table_id(username)
            if role == "admin": 
                userInfo = Admin()
            elif role == "sponsor":
                userInfo = Sponsor()
            else:
                userInfo = Driver()
            # Populate our class with data
            userInfo.populate(username)

            # Flask session data to store data for webpage use
            session['userInfo'] = userInfo
            session.modified = True
        else:
            flash('Incorrect login credentials!')
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session['logged_in'] = False
    global userInfo
    del userInfo
    del session['userInfo']
    del session['sandbox']
    session.modified = True
    userInfo = Driver()
    return redirect(url_for('home'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        form = request.form
        username = form['user']
        pwd = form['pass']
        pwd_check = form['pass_repeat']
        
        if pwd != pwd_check:
            flash('Passwords do not match!')
            return render_template('landing/signup.html')
        
        sponsor = form['sponsorid'] or 'NULL'
        fname = form['fname']
        mname = form['mname'] or 'NULL'
        lname = form['lname']
        address = form['address'] or 'NULL' # Need to look into address fetching
        phone = form['phone']
        email = form['email'] or 'NULL'
        pwd_hash = generate_password_hash(pwd, method='sha256')
        img = 'NULL'

        newDriver = Driver(fname, mname, lname, username, address, phone, email, pwd_hash, img)

        if newDriver.check_username_available():
            newDriver.add_user()
           
            if not sponsor == "NULL":
                try:
                    newDriver.apply_to_sponsor(int(sponsor))
                except:
                    flash("No sponsor found!")
            del newDriver

            flash('Account created!')
            return redirect(url_for('home'))
        else:
           flash('Username taken!')

    return render_template('landing/signup.html')

@app.route("/about")
def about():
    return render_template('landing/about.html')

# Driver Page Routes
@app.route("/driverPointsLeader")
def driverPointsLeader():
    if permissionCheck(["driver", "sponsor", "admin"]) == False:
        return redirect(url_for('home'))
    elif not session['userInfo']['properties']['selectedSponsor']:
        return redirect(url_for('home'))

    currSponsor = Sponsor()
    sponsorId = session['userInfo']['properties']['selectedSponsor'][0]
    sponsorName = currSponsor.username_from_id(sponsorId)
    currSponsor.populate(sponsorName)

    drivers = currSponsor.view_leaderboard()
    del currSponsor
    return render_template('driver/driverPointsLeader.html', drivers=drivers)

@app.route("/driverNotification")
def driverNotification():
    if permissionCheck(["driver", "sponsor", "admin"]) == False:
        return redirect(url_for('home'))
    return render_template('driver/driverNotification.html')

@app.route("/driverManagePurchase")
def driverManagePurchase():
    if permissionCheck(["driver", "sponsor", "admin"]) == False or not session['userInfo']['properties']['selectedSponsor']:
        return redirect(url_for('home'))

    spid = session['userInfo']['properties']['selectedSponsor'][0]
    convert = get_point_value(spid)
    now = datetime.datetime.utcnow()

    def getProductInfo(id):
        admin = Admin()
        prodinfo = admin.getProductInfo(id)
        del admin
        return prodinfo
    
    purchaseList = []
    # get purchase list
    purchaseList = get_orders_by_driver(session['userInfo']['properties']['id'])
    return render_template('driver/driverManagePurchase.html', now = now, convert = convert, getProductInfo = getProductInfo,  purchaseList = purchaseList)

@app.route("/driverProfile")
def driverProfile():
    if permissionCheck(["driver", "sponsor", "admin"]) == False:
        return redirect(url_for('home'))
    return render_template('driver/driverProfile.html')

@app.route("/driverCart")
def driverCart():
    if permissionCheck(["driver", "sponsor", "admin"]) == False or not session['userInfo']['properties']['selectedSponsor']:
        return redirect(url_for('home'))
    spid = session['userInfo']['properties']['selectedSponsor'][0]
    convert = get_point_value(spid)

    # Update price in cart view
    cont = CatalogController()
    _ = map(lambda item: cont.update_price(item), session['shoppingCart'])
    del cont

    def getProductInfo(id):
        admin = Admin()
        prodinfo = admin.getProductInfo(id)
        del admin
        return prodinfo
    
    return render_template('driver/driverCart.html', convert = convert, getProductInfo = getProductInfo)

# Sponsor Page Routes
@app.route("/sponsorNotification")
def sponsorNotification():
    if permissionCheck(["sponsor", "admin"]) == False:
        return redirect(url_for('home'))
    return render_template('sponsor/sponsorNotification.html')

@app.route("/sponsorPointsLeader")
def sponsorPointsLeader():
    if permissionCheck(["sponsor", "admin"]) == False:
        return redirect(url_for('home'))

    currSponsor = Sponsor()
    
    if (session['userInfo']['properties']['role'] == "sponsor"):
        currSponsor.populate(userInfo.getUsername())
        drivers = currSponsor.view_leaderboard()
    else:
        sponsorId = session['userInfo']['properties']['selectedSponsor'][0]
        sponsorName = currSponsor.username_from_id(sponsorId)
        currSponsor.populate(sponsorName)
        drivers = currSponsor.view_leaderboard()

    del currSponsor
    return render_template('sponsor/sponsorPointsLeader.html', drivers=drivers)

@app.route("/sponsorProfile")
def sponsorProfile():
    if permissionCheck(["sponsor", "admin"]) == False:
        return redirect(url_for('home'))
    return render_template('sponsor/sponsorProfile.html')

@app.route("/sponsorSystemSettings", methods=['GET', 'POST'])
def sponsorSystemSettings():
    if permissionCheck(["sponsor"]) == False:
        return redirect(url_for('home'))

    if request.method == 'POST':
        rate = request.form['rate']
        sid = session['userInfo']['properties']['id']
        userInfo.properties['point_value'] = float(rate)
        update_sponsor_rate(sid, rate)
        flash('Conversion rate updated!')

    print(userInfo.properties['point_value'])
    return render_template('sponsor/sponsorSystemSettings.html', rate=userInfo.properties['point_value'])

@app.route("/sponsorViewDriver")
def sponsorViewDriver():
    if permissionCheck(["sponsor", "admin"]) == False:
        return redirect(url_for('home'))
    suspendedUsers = Admin().get_suspended_users()

    currSponsor = Sponsor()

    if session['userInfo']['properties']['role'] == 'admin' or session['sandbox'] == 'sponsor':
        sponsor = currSponsor.get_users()[0][1]
        drivers = currSponsor.view_drivers()
    else:
        sponsor = userInfo.getUsername()
        drivers = userInfo.view_drivers()

    currSponsor.populate(sponsor)
    applications = currSponsor.view_applications()

    del currSponsor
    return render_template('sponsor/sponsorViewDriver.html', drivers=drivers, applications = applications, suspendedUsers=suspendedUsers, sponsor=sponsor)

@app.route("/adminManageAcc", methods=["GET", "POST"])
def adminManageAcc():
    if permissionCheck(["admin"]) == False:
        return redirect(url_for('home'))

    admin = Admin()

    if request.method == "POST":
       form = request.form
       username = form['user']
       pwd = form['pass']
       role = form['roleSelect']
       title = form['title']
       sponsorid = form['sponsorid'] or 'Null'

       fname = 'NULL'
       mname = 'NULL'
       lname = 'NULL'
       address = 'NULL'
       phone = 'NULL'
       email = 'NULL'
       pwd_hash = generate_password_hash(pwd, method='sha256')
       img = 'NULL'
      
       if role == "driver":
           newUser = Driver(fname, mname, lname, username, address, phone, email, pwd_hash, img)
       elif role == "sponsor":
           newUser = Sponsor(title, username, address, phone, email, pwd_hash, img)
       else:
           newUser = Admin(fname, mname, lname, username, phone, email, pwd_hash, img)
    
       if newUser.check_username_available():
           newUser.add_user()
           if sponsorid != 'Null':
               admin.add_to_sponsor(newUser.getID(), sponsorid)
           flash('Account created!')
           del newUser
       elif role == "driver":
            newUser.populate(username)
            if sponsorid != 'Null':
                admin.add_to_sponsor(newUser.getID(), sponsorid)
            else:
                flash('No sponsor id entered!')
            del newUser
       else:
           flash('Username taken!')

    
    sponsor = Sponsor()
    suspendedUsers = admin.get_suspended_users()
    adminList = admin.get_users()
    sponsorList = sponsor.get_users()
    print(sponsorList[0])
    sponsorlessDrivers = admin.get_sponsorless_drivers()
    disabledDrivers = admin.get_disabled_drivers()
    disabledSponsors = admin.get_disabled_sponsors()
    disabledAdmins = admin.get_disabled_admins()
    spon_list = list()
    title_list = list()
    for spon in sponsorList:
        title = spon[0]
        if title not in title_list:
            spon_list.append(spon)
            title_list.append(title)


    def getDriverList(sponsorName):
        currSponsor = Sponsor()
        currSponsor.populate(sponsorName)
        drivers = currSponsor.view_drivers()
        del currSponsor
        return drivers

    del admin
    del sponsor
    return render_template('admin/adminManageAcc.html', sponsorList = spon_list, adminList = adminList, 
                                                        suspendedUsers = suspendedUsers, getDriverList = getDriverList, 
                                                        sponsorlessDrivers = sponsorlessDrivers, disabled = (disabledDrivers, disabledSponsors, disabledAdmins))

@app.route("/adminNotifications")
def adminNotifications():
    if permissionCheck(["admin"]) == False:
        return redirect(url_for('home'))
    return render_template('admin/adminNotifications.html')

@app.route("/adminPointsLeader")
def adminPointsLeader():
    if permissionCheck(["admin"]) == False:
        return redirect(url_for('home'))

    currSponsor = Sponsor()
    sponsorList = currSponsor.get_users()
    spon_list = list()
    title_list = list()
    for spon in sponsorList:
        title = spon[0]
        if title not in title_list:
            spon_list.append(spon)
            title_list.append(title)
        
    sponsors = []
    for sponsor in spon_list:
        currSponsor.populate(sponsor[0])
        sponsors.append(currSponsor.view_leaderboard())
    del currSponsor
    return render_template('admin/adminPointsLeader.html', sponsors=sponsors)

@app.route("/adminReports")
def adminReports():
    if permissionCheck(["admin"]) == False:
        return redirect(url_for('home'))
    return render_template('admin/adminReports.html')

@app.route("/adminSysSettings")
def adminSysSettings():
    if permissionCheck(["admin"]) == False:
        return redirect(url_for('home'))
    return render_template('admin/adminSysSettings.html')

# Consolidated Inbox route 
@app.route('/inbox', defaults={'username': None}, methods=["GET","POST"])
@app.route("/inbox/<username>", methods=["GET","POST"])
def inbox(username):
    if permissionCheck(["driver", "sponsor", "admin"]) == False:
        return redirect(url_for('home'))

    # Driver Inbox
    if session['userInfo']['properties']['role'] == "driver":
        currentDriver = Driver()
        currentDriver.populate(session['userInfo']['properties']['user'])
        messages = currentDriver.view_messages()
        if not bool(messages):
            system = Admin()
            system.populate('System')
            system.send_message(session['userInfo']['properties']['user'], "Welcome to Reward App!")
            del system
            messages = currentDriver.view_messages()
        inbox_list = currentDriver.get_inbox_list()
        del currentDriver
        
        def mark_as_seen(username):
            currentDriver = Driver()
            currentDriver.populate(session['userInfo']['properties']['user'])
            currentDriver.messages_are_seen(username)
            del currentDriver

        return render_template('driver/driverInbox.html', messages = messages, selectedUser = username, seen = mark_as_seen, inbox_list = inbox_list)

    # Sponsor Inbox
    if session['userInfo']['properties']['role'] == "sponsor":
        currentDriver = Sponsor()
        currentDriver.populate(session['userInfo']['properties']['user'])
        messages = currentDriver.view_messages()
        if not bool(messages):
            system = Admin()
            system.populate('System')
            system.send_message(session['userInfo']['properties']['user'], "Welcome to Reward App!")
            del system
            messages = currentDriver.view_messages()
        inbox_list = currentDriver.get_inbox_list()
        del currentDriver

        def mark_as_seen(username):
            currentDriver = Sponsor()
            currentDriver.populate(session['userInfo']['properties']['user'])
            currentDriver.messages_are_seen(username)
            del currentDriver

        return render_template('sponsor/sponsorInbox.html', messages = messages, selectedUser = username, seen = mark_as_seen, inbox_list = inbox_list)

    # Admin Inbox
    if session['userInfo']['properties']['role'] == "admin":
        currentDriver = Admin()
        currentDriver.populate(session['userInfo']['properties']['user'])
        messages = currentDriver.view_messages()
        if not bool(messages):
            system = Admin().populate('System')
            system.send_message(session['userInfo']['properties']['user'], "Welcome to Reward App!")
            del system
            messages = currentDriver.view_messages()
        inbox_list = currentDriver.get_inbox_list()
        del currentDriver

        def mark_as_seen(username):
            currentDriver = Admin()
            currentDriver.populate(session['userInfo']['properties']['user'])
            currentDriver.messages_are_seen(username)
            del currentDriver

        return render_template('admin/adminInbox.html', messages = messages, selectedUser = username, seen = mark_as_seen, inbox_list = inbox_list)


# Settings page
@app.route("/settings", methods=["GET","POST"])
def settings():
        if permissionCheck(["driver", "sponsor", "admin"]) == False:
            return redirect(url_for('home'))
        session['sandbox'] = None
        session.modified = True

        if request.method == 'POST':
            if 'delete-account' in request.form.keys():
                userInfo.delete()
                session['logged_in'] = False
                flash('Account successfully deleted')
                session.modified = True
                return redirect(url_for('home'))

            if 'change-info' in request.form.keys():
                # Filter out form items that are not filled in
                data = dict(filter(lambda elem: elem[1] != '', request.form.items()))
                
                # Check if no form boxes were filled in
                if not len(data):
                    flash("Please fill in at least one box")
                    return render_template(session['userInfo']['properties']['role'] + "/settings.html")
                
                userInfo.update_info(data)
                return render_template(session['userInfo']['properties']['role'] + "/settings.html")

            elif 'pwd-submit' in request.form.keys():
                oldPwd = request.form['old_pass']
                currentHash = get_password(session['userInfo']['properties']['user'])
                if not check_password_hash(currentHash, oldPwd):
                    flash("Wrong old password!")
                    return render_template(session['userInfo']['properties']['role'] + "/settings.html")
                pwd = generate_password_hash(request.form['pass'], 'sha256')
                userInfo.update_info({'pwd': pwd})
                return render_template(session['userInfo']['properties']['role'] + "/settings.html")
            elif 'add_new_sponsor_login' in request.form.keys():
                form = request.form
                username = form['username']
                password = form['password']
                confirm_password = form['confirm_password']
                sponsor = Sponsor(user=username)
                if sponsor.check_username_available():
                    if password != confirm_password:
                        flash("Passwords do not match!")
                        return render_template('sponsor/settings.html')
                    else:
                        pwd = generate_password_hash(password, method='sha256')
                        sponsor.populate(session['userInfo']['properties']['user'])
                        sponsor.add_new_sponsor_login(username, pwd)
                        del sponsor
                        flash("New login successfully created")
                        return render_template('sponsor/settings.html')
                else:
                    flash("Username already taken")
                    return render_template('sponsor/settings.html')

            elif 'change-notis' in request.form.keys():
                notis = {}
                notis['points'] = 1 if 'points' in request.form.keys() else 0
                notis['orders'] = 1 if 'orders' in request.form.keys() else 0
                notis['issue'] = 1 if 'issue' in request.form.keys() else 0
                driver = Driver()
                driver.populate(session['userInfo']['properties']['user'])
                driver.update_noti(notis)
                del driver
                return render_template('driver/settings.html', notis = notis)
            elif 'join_code_button' in request.form.keys():
                driver = Driver()
                driver.populate(session['userInfo']['properties']['user'])
                id = request.form['join_code']
                driver.apply_to_sponsor(id)
                del driver
                
        if session['userInfo']['properties']['role'] == "driver":
            driver = Driver()
            driver.populate(session['userInfo']['properties']['user'])
            notis = driver.get_notifications()
            return render_template('driver/settings.html', notis = notis)
        else:
            return render_template(session['userInfo']['properties']['role'] + '/settings.html')

# App Functions
@app.route("/switchSponsor", methods=['GET', 'POST'])
def switchSponsor():
    if permissionCheck(["driver", "sponsor", "admin"]) == False:
            return redirect(url_for('home'))

    if not session['userInfo']['properties']['role'] == "admin" or session['userInfo']['properties']['role'] == "sponsor":
        newSponsorid = request.form.get('sponsorSelect')
        sponsorlist = userInfo.view_sponsors()
        points = 0
        for sponsor in sponsorlist:
            if int(sponsor[0]) == int(newSponsorid):
                points = sponsor[1]

        userInfo.setSponsorView([newSponsorid, points])
        session['shoppingCart'].clear()
        session['userInfo']['properties']['selectedSponsor'] = [newSponsorid, points]
        session.modified = True

    return redirect(url_for('home'))

@app.route("/sponsorView")
def sponsorView():
    permissionCheck(["driver", "sponsor", "admin"])
    if session['userInfo']['properties']['role'] == "admin":
        session['sandbox'] = "sponsor"
        session.modified = True
    return redirect(url_for('home'))

@app.route("/driverView")
def driverView():
    permissionCheck(["driver", "sponsor", "admin"])
    if session['userInfo']['properties']['role'] == "admin" or session['userInfo']['properties']['role'] == "sponsor":
        session['sandbox'] = "driver"
        session.modified = True
    return redirect(url_for('home'))

@app.route("/returnView")
def returnView():
    permissionCheck(["driver", "sponsor", "admin"])
    session['sandbox'] = "NULL"
    session.modified = True
    return redirect(url_for('home'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.route("/acceptapp", methods=["GET","POST"])
def acceptapp():
    data = request.get_data().decode("utf-8").split("&")
    user = data[0].split("=")
    sponsorname = data[1].split("=")

    sponsor = Sponsor()
    sponsor.populate(sponsorname[1])

    sponsor.accept_application(user[1].strip('+'))
    del sponsor
    return ('', 204)

@app.route("/rejectapp", methods=["GET","POST"])
def rejectapp():
    data = request.get_data().decode("utf-8").split("&")
    user = data[0].split("=")
    sponsorname = data[1].split("=")

    sponsor = Sponsor()
    sponsor.populate(sponsorname[1])
    sponsor.decline_application(user[1].strip('+'))
    del sponsor
    return ('', 204)

@app.route("/suspend", methods=["GET","POST"])
def suspend():
    admin = Admin()
    user = request.get_data().decode("utf-8") 
    user = user.strip()
    admin.suspend_user(user, 9999, 12, 30)
    del admin
    return ('', 204)

@app.route("/unsuspend", methods=["GET","POST"])
def unsuspend():
    admin = Admin()
    user = request.get_data().decode("utf-8") 
    user = user.strip()
    admin.cancel_suspension(user)
    del admin
    return ('', 204)

@app.route("/remove", methods=["GET","POST"])
def remove():
    admin = Admin()
    user = request.get_data().decode("utf-8") 
    user = user.strip()
    admin.remove_user(user)
    del admin
    return ('', 204)

@app.route("/reactivate", methods=["GET","POST"])
def reactivate():
    admin = Admin()
    user = request.get_data().decode("utf-8") 
    user = user.strip()
    admin.reactivate_user(user)
    del admin
    return ('', 204)

@app.route("/removeFromSponsor", methods=["GET","POST"])
def removeFromSponsor():
    data = request.get_data().decode("utf-8").split("&")
    user = data[0].split("=")
    sponsorname = data[1].split("=")

    driver = Driver()
    driver_username = user[1].strip('+')
    driver.populate(driver_username)
    driver_id = driver.getID()

    sponsor = Sponsor()
    sponsor.populate(sponsorname[1])
    sponsor.remove_driver(driver_id)
    del sponsor
    return ('', 204)

@app.route("/addpts", methods=["GET","POST"])
def addpts():
    data = request.get_data().decode("utf-8").split("&")
    user = data[0].split("=")
    points = data[1].split("=")
    sponsorname = data[2].split("=")

    driver = Driver()
    driver_username = user[1].strip('+')
    driver.populate(driver_username)
    driver_id = driver.getID()
    sponsor = Sponsor()
    sponsor.populate(sponsorname[1])
    sponsor.add_points(driver_id, int(points[1]))
    del driver
    del sponsor
    return ('', 204)

@app.route("/sendmessage", methods=["GET","POST"])
def sendmessage():
    data = request.get_data().decode("utf-8").split("&")
    reciever = data[0].split("=")
    sender = data[1].split("=")
    message = data[2].split("=")

    id, role = get_table_id(sender[1])

    if role == "admin":
        user = Admin()
    elif role == "sponsor":
        user = Sponsor()
    else:
        user = Driver()
    
    username = sender[1].strip('+')

    if not message == "":
        user.populate(username)
        user.send_message(reciever[1].strip('+'), message[1].replace('+', " "))
    del user
    return ('', 204)

@app.route("/addToCart", methods=["GET","POST"])
def addToCart():
    data = request.get_data().decode("utf-8").split("&")
    id = data[0].split("=")[1]

    if not 'shoppingCart' in session:
        session['shoppingCart'] = dict()
    
    if id in session['shoppingCart']:
        session['shoppingCart'][id] += 1
    
    else:
        session['shoppingCart'][id] = 1

    session.modified = True

    return ('', 204)

@app.route("/removeFromCart", methods=["GET","POST"])
def removeFromCart():
    data = request.get_data().decode("utf-8").split("&")
    id = data[0].split("=")[1]
    session['shoppingCart'].pop(id)
    session.modified = True
    return ('', 204)

@app.route("/cancelOrder", methods=["GET","POST"])
def cancelOrder():
    data = request.get_data().decode("utf-8") 
    order = data.strip()
    spid = get_order_info(order)[0][1]
    convert = get_point_value(spid)
    orderTotal = 0
    # Refund Points
    orderinfo = get_order_info(order)
    for item in orderinfo:
        orderTotal += int(float(item[4]) / convert)
    sponsor = Sponsor()
    name = getSponsorTitle(spid)
    sponsor.populate(name)
    sponsor.add_points(session['userInfo']['properties']['id'], orderTotal)
    session['userInfo']['properties']['selectedSponsor'][1] += orderTotal
    session.modified = True
    # Cancel Order
    cancel_order(order)
    del sponsor
    return ('', 204)

@app.route("/checkout", methods=["GET","POST"])
def checkout():
    def getProductInfo(id):
        admin = Admin()
        prodinfo = admin.getProductInfo(id)
        del admin
        return prodinfo

    # Vars
    cartTotal = 0
    success = True
    purchase = session['shoppingCart'].copy()
    ordernum = get_next_order_id()
    now = datetime.datetime.now()
    uid = session['userInfo']['properties']['id']
    spid = session['userInfo']['properties']['selectedSponsor'][0]
    convert = get_point_value(spid)

    # Update price of all items in cart
    cont = CatalogController()
    _ = list(map(lambda item: cont.update_price(item ), session['shoppingCart']))
    del cont

    for item in session['shoppingCart']:
        cartTotal += int((getProductInfo(item)[1]) / convert)
    
    if cartTotal > session['userInfo']['properties']['selectedSponsor'][1]:
        success = False
    
    else:
        sponsor = Sponsor()
        name = getSponsorTitle(spid)
        sponsor.populate(name)

        # Subtract the points
        sponsor.add_points(session['userInfo']['properties']['id'], -cartTotal)
        session['userInfo']['properties']['selectedSponsor'][1] -= cartTotal
        session.modified = True

        # Add to the database
        for item in session['shoppingCart']:
            amount = getProductInfo(item)[1]
            for x in range(0, session['shoppingCart'].get(item)):
                add_new_order(uid, item, '3', spid, amount, ordernum)

        # Clear the cart
        session['shoppingCart'].clear()
        session.modified = True
        del sponsor
    return render_template('driver/driverReciept.html', convert = convert, purchase = purchase, orderNumber = ordernum, success = success, total = cartTotal, date = now, getProductInfo = getProductInfo)

@app.route("/sendto", methods=["GET","POST"])
def sendto():
    data = request.get_data().decode("utf-8").split("&")
    sender = data[0].split("=")
    receiver = data[1].split("=")
    message = data[2].split("=")

    id, role = get_table_id(sender[1])

    if role == "admin":
        user = Admin()
    elif role == "sponsor":
        user = Sponsor()
    else:
        user = Driver()
    
    username = sender[1].strip('+')
    if username_exist(receiver[1]) and not message == "":
        user.populate(username)
        user.send_message(receiver[1].strip('+'), message[1].replace('+', " "))

    del user
    return ('', 204)

@app.route("/productsearch", methods=["GET","POST"])
def productsearch():
    if permissionCheck(["driver", "sponsor", "admin"]) == False:
        return redirect(url_for('home'))

    # Setting up default variables
    search = ""
    results = "" 
    amount = 0
    sponsorId = session['userInfo']['properties']['selectedSponsor'][0]

    # On post, get information from filter form
    if request.method == 'POST':
        form = request.form
        search = form['search']
        mylist = form['mylist']
        order = form['orderby']
        amount = int(form['amount'])
        results = product_search(search, sponsorId, mylist, order)

    # Store limited amount of results and send to page
    limitedresults = []
    convert = get_point_value(sponsorId)
    # Loop to the minimum of the amount of results and the amount of products to show
    for i in range(0, min(amount, len(results))):
        limitedresults.append(results[i])
    for row in limitedresults:
        row['price'] = int(row['price']/convert)

    return render_template('driver/driverResults.html', numresults = len(results), query = search, results = limitedresults)


#Very much a building block, may scrap if need be
@app.route("/productpage", methods=["GET","POST"])
def productpage():
    if permissionCheck(["driver", "sponsor", "admin"]) == False:
        return redirect(url_for('home'))

    sponsorId = session['userInfo']['properties']['selectedSponsor'][0]
    convert = get_point_value(sponsorId)
    if request.method == 'POST':
        form = request.form
        got = form['productname']
        results = product_search(got, sponsorId, "None", "priceup" )

        # Update price and then re-search
        cont = CatalogController()
        rc = cont.update_price(results[0]['id'])
        del cont
        if not rc:
            flash('Item not available!')
            return redirect(url_for('home'))

        results = product_search(got, sponsorId, "None", "priceup" )

#    print(results[0]['name'])
        return render_template('driver/driverProduct.html',convert = convert, results = results[0])

@app.route("/buynowrecipt", methods=["GET", "POST"])
def buynowrecipt():
    if permissionCheck(["driver", "sponsor", "admin"]) == False:
        return redirect(url_for('home'))

    def getProductInfo(id):
        admin = Admin()
        prodinfo = admin.getProductInfo(id)
        del admin
        return prodinfo
    
    #Retooling checkout for single item purchases
    spid = session['userInfo']['properties']['selectedSponsor'][0]
    results = []

    if request.method == 'POST':
        form = request.form
        got = form['buy']
        results = product_search(got, spid, "None", "priceup" )

        # Update price and get product again
        cont = CatalogController()
        cont.update_price(results[0]['id'])
        del cont

        results = product_search(got, spid, "None", "priceup")

    # Vars
    cartTotal = 0
    success = True
    purchase = dict()
    purchase[results[0]['id']] = 1
    #ordernum is the single id from the product
    ordernum = results[0]['id']
    now = datetime.datetime.now()
    uid = session['userInfo']['properties']['id']
    convert = get_point_value(spid)

    #cartTotal only needs one price
    cartTotal = int(results[0]['price']/convert)

    if cartTotal > session['userInfo']['properties']['selectedSponsor'][1]:
        success = False
    
    else:
        sponsor = Sponsor()
        name = getSponsorTitle(spid)
        sponsor.populate(name)

        # Subtract the points
        sponsor.add_points(session['userInfo']['properties']['id'], -cartTotal)
        session['userInfo']['properties']['selectedSponsor'][1] -= cartTotal
        session.modified = True

        #Switched cart for results, the single item info
        # Add to the database
        for item in results:
            amount = getProductInfo(item['id'])[1]
            add_new_order(uid, item['id'], '3', spid, amount, ordernum)

        del sponsor
    return render_template('driver/driverReciept.html', convert = convert, purchase = purchase, orderNumber = ordernum, success = success, total = cartTotal, date = now, getProductInfo = getProductInfo)

@app.route("/thanks", methods=["GET","POST"])
def thanks():
    if permissionCheck(["driver", "sponsor", "admin"]) == False:
        return redirect(url_for('home'))

    userId = session['userInfo']['properties']['id']

    if request.method == "POST":
        form = request.form
        num = form['review']
        pid = form['product']
        updateproductorder(userId, pid, num)

    return render_template('driver/driverThanks.html')

@app.route("/productAJAX", methods=["POST"])
def productAJAX():
    data = request.json
    search = data['search']
    print(session['userInfo']['properties']['selectedSponsor'][0])
    return json.dumps(get_products_by_name(search, session['userInfo']['properties']['selectedSponsor'][0]))

@app.route("/purchaseItem", methods=["POST"])
def purchaseItem():
    def getProductInfo(id):
        admin = Admin()
        prodinfo = admin.getProductInfo(id)
        del admin
        return prodinfo

    # Vars
    ordernum = get_next_order_id()
    spid = session['userInfo']['properties']['selectedSponsor'][0]
    convert = get_point_value(spid)

    data = request.get_data().decode("utf-8").split("&")
    sponsor = data[0].split("=")[1]
    user = data[1].split("=")[1]
    search = data[2].split("=")[1].replace("+", " ")
    driver = Driver()
    driver.populate(user)
    uid = driver.getID()

    item_id = product_search(search, spid, "None", "priceup")[0]['id']

    amount = int((getProductInfo(item_id)[1]) / convert)
    if amount > driver.getPoints(spid):
        flash("Insufficient Points")
    else:
        sponsor = Sponsor()
        name = getSponsorTitle(spid)
        sponsor.populate(name)

        # Subtract the points
        sponsor.add_points(uid, -amount)
        amount = getProductInfo(item_id)[1]
        add_new_order(uid, item_id, '3', spid, amount, ordernum)
        del sponsor
        flash("Purchase Successful")
    del driver
    return redirect(url_for('sponsorViewDriver'))

# IMPORTANT: Route becoming deprecated
# Evan: I changed the location of the edit button to use updateAccount so that it can be shared by
# both the admins and the sponsors
'''
@app.route("/updateDriver/<username>", methods=["GET","POST"])
def updateDriver(username):
    """ Render page for a sponsor to update their drivers. Driver to be updated is the endpoint of the URL.
        Provides an endpoint for AJAX calls as well. Expects a JSON object with keys corresponding to driver
        attributes in database"""
    dl = Driver().get_users()
    driver = list(filter(lambda d: d[3] == username, dl))[0]
    driverObj = Driver()
    driverObj.populate(username)
    if request.method == 'POST':
        data = request.json
        if 'addPoints' in data.keys():
            add_points_to_driver(username, 0, data['addPoints'])
            return json.dumps({'status': 'OK', 'ptsAdded': data['addPoints']})

        # Data should be formatted in the way update_info expects
        driverObj.update_info(data)
        flash("Information updated!")
        return json.dumps({'status': 'OK', 'user': username})

    return render_template("sponsor/sponsorEditDriver.html", user=driverObj)
'''

@app.route('/updateAccount/<username>', methods=['GET','POST'])
def updateAccount(username):
    """ Route for an admin to update any user account. Figures out role from table and generates a template
        accordingly
    """
    def posted(username, user):
        if request.method == 'POST':
            data = request.json
            if 'pwd' in data.keys():
                data['pwd'] = generate_password_hash(data['pwd'], 'sha256')
            # Sorry Evan...
            if 'sponsor' in data.keys():
                admin = Admin()
                driver = Driver()
                driver.populate(username)
                admin.add_to_sponsor(driver.getID(), data['sponsor'])
                del admin, driver, data['sponsor']
            else:
                # Data should be formatted in the way update_info expects
                user.update_info(data)
            return json.dumps({'status': 'OK', 'user': username})
        else:
            return None

    sessRole = session['userInfo']['properties']['role']

    if sessRole == 'admin':
        uid, role = get_table_id(username)
        user = None
        if role == 'driver':
            user = Driver()
        elif role == 'sponsor':
            user = Sponsor()
        else:
            user = Admin()
        user.populate(username)
        out = posted(username, user)
        if out:
            print(out)
            return out
        
        return render_template('admin/adminUpdateAccount.html', user=user, role=role)

    elif sessRole == 'sponsor':
        allDrivers = userInfo.view_drivers()
        driver = list(filter(lambda d: d[3] == username, allDrivers))

        if driver:
            user = Driver()
            user.populate(username)
            posted(username, user)

            return render_template('sponsor/sponsorEditDriver.html', user=user, sponsor=session['userInfo']['properties']['user'], points=driver[0][4])
        else:
            flash('Driver not in your list!')
            return redirect(url_for('sponsorViewDriver'))
        
    else:
        flash('Please login before trying to edit accounts')
        return redirect(url_for('home'))


# Sponsor Catalog Additions Search
@app.route('/sponsorSearch', methods=['GET', 'POST'])
def sponsorSearch():
    if request.method == 'POST':
        search = request.form['search']
        limit = int(request.form['limit'])

        # Send query to Etsy Controller
        cont = EtsyController(os.getenv("ETSY_API_KEY"))
        cont.limit = limit
        results = cont.get_products_keywords(search)
        return render_template('sponsor/sponsorResults.html', results=results) 

# Sponsor view of catalog
@app.route('/catalog', methods=['GET','POST'])
def sponsorCatalog():
    print(session['userInfo']['properties'])
    if session['userInfo']['properties']['role'] == 'sponsor':
        cont = CatalogController()
        etsyCont = EtsyController(os.getenv('ETSY_API_KEY'))
        search = None
        if request.method == 'POST':
            if request.json:
                data = request.json
                listing = data['listing_id']
                val = cont.remove(session['userInfo']['properties']['id'], listing)
                del cont
                message = {'message': 'Item removed' if val else 'Item not removed'}
                return json.dumps(message)
            else:
                search = request.form['search']

        items = cont.fetch_catalog_items(session['userInfo']['properties']['id'], search)
        items['items'] = list(map(lambda elem: dict((*elem.items(), ('url', etsyCont.get_url(elem['listing_id'])))), items['items']))
        print(items)
        del cont
        del etsyCont
        rate = session['userInfo']['properties']['point_value'] or 0.01
        return render_template('sponsor/sponsorCatalog.html', results=items['items'], conversion=rate)
    else:
        flash('Access not allowed')
        return redirect(url_for('home'))

# Admin view sponsor catalog
@app.route('/catalog/<sponsor>', methods=['GET', 'POST'])
def catalog(sponsor):
    if session['userInfo']['properties']['role'] == 'admin':
        sid, role = get_table_id(sponsor)
        if role != 'sponsor':
            return redirect(url_for('home'))
        cont = CatalogController()

        search = None

        if request.method == 'POST':
            if request.json:
                data = request.json
                listing = data['listing_id']
                val = cont.remove(sid, listing)
                del cont
                message = {'message': 'Item removed' if val else 'Item not removed'}
                return json.dumps(message)

            else:
                search = request.form['search']

        items = cont.fetch_catalog_items(sid, search)
        del cont
        return render_template('admin/adminViewCatalog.html', results=items['items'], sponsor=sponsor)
        
    else:
        flash('Access not allowed')
        return redirect(url_for('home'))

# Download report view
@app.route('/reports', methods=['GET','POST'])
def reports():
    role = session['userInfo']['properties']['role']
    templateName = '{}/{}Reports.html'.format(role, role)

    if not session['logged_in']: 
        return redirect(url_for('home'))

    if role == 'admin':
        sponsorList = Sponsor().get_users()

        # Get list of all sponsor names from sponsor tuples
        sponsorNames = list(map(lambda elem: elem[0], sponsorList))
        sponsorIds = list(map(lambda elem: elem[1], sponsorList))

        if request.method == 'POST':

            cont = ReportController()

            startDate = request.form['startdate'].split('-')
            startDate = datetime.datetime(int(startDate[0]), int(startDate[1]), 1)

            endDate = request.form['enddate'].split('-')
            endDate = datetime.datetime(int(endDate[0]), int(endDate[1]), calendar.monthrange(int(endDate[0]), int(endDate[1]))[1])


            fname = ""
            if request.form['reporttype'] == 'Sales over time':
                # Report of sales over time

                # Get number of each user type
                numDrivers = cont.number_users('driver')
                numSponsors = cont.number_users('sponsor')
                numAdmins = cont.number_users('admin')
                metaHeaders = ('# of Drivers', '# of Sponsors', '# of Admins')

                cont.write(metaHeaders)
                cont.write((numDrivers, numSponsors, numAdmins))
                cont.write(())
                sales = cont.total_sales((startDate, endDate))

                cont.write(('Month','Sales'))

                # Function to write each month into report over sales
                def func(month):
                    cont.write( (datetime.datetime(startDate.year, month[0], 1).strftime("%m"), round(float(month[1]), 2)) )
                    return month

                sales = dict(map(func, sales.items()))
                fname = "{}-total-sales-report.csv".format(2020)

            else: 
                # Elements are all named sponsor, so this grabs the whole list of them

                sponsors = request.form.getlist('sponsor')

                if not sponsors:
                    flash('No sponsor selected!')
                    return render_template('admin/adminReports.html', sponsors=sponsorNames)

                if request.form['reporttype'] == 'Sales by sponsor':
                # Report of sales by sponsor, summarized by month
                    sponsorHeaders = ('Month','Sponsor', 'Purchases Total', 'Expenses')
                    cont.write(sponsorHeaders)

                    def sponsTot(s):
                        return (s[0], cont.sponsor_stats(s[1], (startDate, endDate)))

                    sponsorIds = list(filter(lambda elem: elem[0] in sponsors, zip(sponsorNames, sponsorIds)))
                    sponsorTotals = dict(map(sponsTot, sponsorIds))
                    print(sponsorTotals)


                    for i in range(startDate.month, endDate.month+1):
                        cont.write( (datetime.datetime(startDate.year, i, 1).strftime("%B"), ) )
                        for j in sponsorTotals:
                            purchase = round(float(sponsorTotals[j][i]), 2)
                            cont.write( ('', j, purchase, purchase * .01) )

                    fname = "{}-sponsor-sales-report.csv".format('-'.join([startDate.strftime("%m-%d"), endDate.strftime("%m-%d")]))
                else:
                    # Report of purchases by driver, summarized by sponsor
                    sponsorHeaders = ('Sponsor','Driver','Purchases')
                    cont.write(sponsorHeaders)

                    def driverAgg(s):
                        return (s[0], cont.driver_purchases(s[1]))

                    sponsorIds = list(filter(lambda elem: elem[0] in sponsors, zip(sponsorNames, sponsorIds)))
                    sponsorSumms = dict(map(driverAgg, sponsorIds))

                    for sp in sponsorSumms.keys():
                        cont.write((sp, ''))
                        print(sponsorSumms[sp])
                        for dr in sponsorSumms[sp]:
                            cont.write(('', dr)) 
                            for purchase in sponsorSumms[sp][dr]:
                                cont.write(('', '', purchase))
                    fname = "{}-driver-summary-report.csv".format(date.today().strftime('%m-%d'))


            # Serve report file
            mem = cont.get_file()
            del cont

            now = date.today()
            return send_file(mem, as_attachment=True, attachment_filename=fname, mimetype='text/csv')
        return render_template(templateName, sponsors=sponsorNames)
    elif role == 'sponsor':
        return render_template(templateName)
    else:
        return redirect(url_for('home'))

@app.route('/sponsorList', methods=['POST'])
def sponList():
    """ AJAX endpoint for getting list of sponsors and their ids """
    if session['userInfo']['properties']['role'] == 'admin':
        sponsors = Sponsor().get_users()
        cont = ReportController()
        now = date.today()
        startDate = datetime.datetime(now.year, 1, 1)
        endDate = datetime.datetime(now.year, 12, 31)
        sponsors = list(map(lambda x: (x[0], x[1]), sponsors))
        results = list(map(lambda x: cont.sponsor_stats(x[1], (startDate, endDate)), sponsors))
        results = list(map(lambda x: dict(map(lambda y: (y[0], int(y[1])), x.items())), results))
        output = list(map(lambda x: {'info': x[0], 'results': x[1]}, zip(sponsors, results)))
        print(output)
        del sponsors
        del cont
        return json.dumps(output)
    else:
        return json.dumps({})

@app.context_processor
def sponsorTitle():
    def getSponsorTit(id):
        return getSponsorTitle(id)
    return dict(getSponsorTitle=getSponsorTit)
