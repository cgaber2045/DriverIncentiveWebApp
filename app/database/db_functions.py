import datetime
from .db_users import getConnection



def test():
    conn = getConnection()
    conn.exec("Select concat('KILL ',id) , time from information_schema.processlist where user != 'event_scheduler' and user != 'rdsadmin' and time > 500 order by time desc;")
    conn.close()
#checks to see if the password entered by the user matches password with that username
#searches through user table for username and role
#uses role to search through specific table for username and password
#returns true if the password entered mathches the one in the table
def pwd_check(user = 'NULL', pwd = 'NULL'):
    if( user == 'NULL' or pwd == 'NULL'):
        return False

    id, table = get_table_id(user)
    
    sql = 'SELECT pwd FROM ' + table + ' WHERE user = %s'
    val = (user, )
    cursor = getConnection()
    current_password = cursor.exec(sql, val)
    cursor.close()

    if pwd == current_password[0]:
        return True
    else: 
        return False

#changes the password for a user
#any username of any role can be passed into this function
def change_password(user, pwd):
    id, table = get_table_id(user)

    sql = 'UPDATE ' + table + ' SET pwd = %s WHERE user = %s'
    val = (pwd, user)
    cursor = getConnection()
    cursor.exec(sql, val)
    cursor.close()

# Returns password hash for a user
def get_password(user='NULL'):
    if( user == 'NULL'):
        return ''

    id, table = get_table_id(user)
    
    sql = 'SELECT pwd FROM ' + table + ' WHERE user = %s'
    if table == 'sponsor':
        sql = 'SELECT password FROM sponsor_logins WHERE username = %s'
    val = (user, )
    conn = getConnection()
    current_password = conn.exec(sql, val)
    conn.close()

    return current_password[0][0]

# Determines if username is in the table
# returns true if username is in user table
# false if it isn't
def username_exist(user = 'NULL'):
    if( user == 'NULL' ):
        return False

    sql = "SELECT * FROM users WHERE UserName = %s"
    val = (user, )
    conn = getConnection()
    row = conn.exec(sql, val)
    conn.close()
    
    return row

#returns id and table that the user is in
def get_table_id(user):
    sql = 'SELECT Driver_ID, Sponsor_ID, Admin_ID FROM users WHERE UserName = %s'
    val = (user, )
    conn = getConnection()
    id = conn.exec(sql, val)
    conn.close()
    if id[0][0] != None:
        return id[0][0], 'driver'
    elif id[0][1] != None:
        return id[0][1], 'sponsor'
    else:
        return id[0][2], 'admin'

# Takes in a sponsor id and gets their title
def getSponsorTitle(ident):
    try:
        cursor = getConnection()
        title =  cursor.exec("SELECT title FROM sponsor WHERE sponsor_id = %s" % ident)[0][0]
        cursor.close()
        return title
    except Exception as e:
            raise Exception(e)

#Clean search and translate into sql search
def product_search(search, spon_id, mylist, order):

    # Query to get matching products
    multigenrelong = "SELECT name, price, rating, description, img_url, product_id FROM product WHERE available = 1 AND name REGEXP(%s)"
    # Checking for selected genre
    if mylist != "None":
        multigenrelong += " AND Genre = %s" % mylist
    # Checking for selected sponsor
    if(str(spon_id) != 'Any'):
        multigenrelong += " AND sponsor_id= %s" % spon_id

    # Sorting by order
    if order == "priceup":
         multigenrelong += " ORDER BY price ASC"
    elif order == "ratingup":
         multigenrelong += " ORDER BY rating ASC"
    elif order == "pricedown":
         multigenrelong += " ORDER BY price DESC"
    elif order == "ratingdown":
         multigenrelong += " ORDER BY rating DESC"

    vals = (search,)

    try:
        cursor = getConnection()
        data = cursor.exec(multigenrelong, vals)
        cursor.close()
    except Exception as e:
        raise Exception(e)

    # Getting all products and storing them as a list of dictionaries 
    # [item1 dict, item2 dict]
    # each dict item contains name, price, rating, description, img_url, and id
    products = []
    for item in data:
        prod = {"name":item[0], "price":item[1], "rating":item[2], "description":item[3], "img_url":item[4], "id":item[5]}
        products.append(prod)

    return products

#gets the next available order id, returns 1 if no orders exist
def get_next_order_id():
    cursor = getConnection()
    num = cursor.exec("SELECT MAX(Order_ID) FROM Product_Orders")
    cursor.close()

    if( num[0][0] == None ):
        return 1
    else:
        return num[0][0] + 1

#add a new order to the product_orders table
def add_new_order(uid, pid, rating, spid, amount, oid):
    query = 'INSERT INTO Product_Orders (Driver_ID, Product_ID, rating, TimeStamp, Sponsor_ID, amount, Order_ID, canceled) VALUES ({}, {}, {}, CURRENT_TIMESTAMP, {}, {}, {}, false)'
    query = query.format(uid, pid, rating, spid, amount, oid)
    try:
        cursor = getConnection()
        cursor.exec(query)
        cursor.close()
    except Exception as e:
            raise Exception(e)

#ability to mark an order as canceled
def cancel_order(order):
    query = 'UPDATE Product_Orders SET canceled = true WHERE Order_ID = %s' % order
    try:
        cursor = getConnection()
        cursor.exec(query)
        cursor.close()
    except Exception as e:
            raise Exception(e)

# ability to get order info
def get_order_info(order):
    query = 'SELECT Product_ID, rating, TimeStamp, Sponsor_ID, amount, canceled FROM Product_Orders WHERE Order_ID = %s' % order
    try:
        cursor = getConnection()
        data =  cursor.exec(query)
        cursor.close()
        return data
    except Exception as e:
            raise Exception(e)

#get all orders from a certain driver
def get_orders_by_driver(uid):
    query = 'SELECT Order_ID, Product_ID, rating, TimeStamp, Sponsor_ID, amount, canceled FROM Product_Orders WHERE Driver_ID = %s ORDER BY Order_ID DESC' % uid

    try:
        cursor = getConnection()
        orders = cursor.exec(query)
        cursor.close()

    except Exception as e:
            raise Exception(e)
    
    orderDict = {}
    for order in orders:
        orderlist = list(order[1:])
        if order[0] in orderDict:
            orderDict[order[0]].append(orderlist)
        else:
            orderDict[order[0]] = [orderlist]

    return orderDict


def updateproductorder(uid, pid, rating):
    try:
        cursor = getConnection()
        cursor.exec("INSERT INTO Product_Orders (Driver_ID, Product_ID, rating, TimeStamp) VALUES ('"+str(uid)+"', '"+str(pid)+"','"+str(rating)+"' , CURRENT_TIMESTAMP)")
        cursor.close()
    except Exception as e:
            raise Exception(e)

# Return a list of all genres
def getgenres():
    try:
        cursor = getConnection()
        returngenre = cursor.exec("SELECT DISTINCT Genre FROM product")
        cursor.close()
    except Exception as e:
            raise Exception(e)

    return list(map(lambda x: x[0], returngenre))

# Get how many products a sponsor has
def getnumproducts(spon_id):
    query = "SELECT COUNT(sponsor_id) FROM product WHERE available = 1 AND sponsor_id = %s"
    val = (spon_id,)

    try:
        cursor = getConnection()
        returnnum = cursor.exec(query, val)

    except Exception as e:
        raise Exception(e)
    
    # Removed shady string manipulation
    num = 0
    if returnnum:
        num = returnnum[0][0]
    cursor.close()
    return num


#Just totally restarting cause jesus that was a mess
"""
IDEA: 
Grab latest product from current user
    If no products have been bought, return a ' ' value
Grab the user who bought that same product most recently
Return the product that the second user bought most recently, excluding the current product

"""
def recommend(userid, sid):
    cursor = getConnection()
    #Select a tuple list of all the products ordered by most recent
    OGproducttup = cursor.exec("SELECT product_id FROM Product_Orders WHERE Sponsor_ID = '"+str(sid)+"' AND Driver_ID ='"+str(userid)+"' ORDER BY TimeStamp DESC")
    #Return nothing if the user hasn't bought anything
    if(len(OGproducttup) < 1 ):
        cursor.close()
        return ' '
#   We only need the first element
    OGproductstr = ''.join(map(str, OGproducttup[0]))
#    print(OGproductstr)
#   Now select the most recent driver who has also bought the same item most recently AND has bought more than 1 time
#God that took awhile
    otherdriveridtup = cursor.exec("SELECT Driver_ID FROM Product_Orders WHERE Driver_ID !='"+str(userid)+"' AND product_id = '"+OGproductstr+"' AND Driver_ID IN (SELECT Driver_ID FROM Product_Orders GROUP BY Driver_ID HAVING COUNT(*) >1) ORDER BY TimeStamp Desc")
#    print(otherdriveridtup)
    if(len(otherdriveridtup) < 1):
        cursor.close()
        return ' '
    otherdriveridstr = ''.join(map(str, otherdriveridtup[0]))
#    print(otherdriveridstr)
    #Grap the most recent purchase from the other driver that isn't the OG product
    otherproducttup = cursor.exec("SELECT Product_ID FROM Product_Orders WHERE Sponsor_ID = '"+str(sid)+"' AND Product_ID != '"+OGproductstr+"' AND Driver_ID = '"+otherdriveridstr+"' ORDER BY TimeStamp DESC")
    if(len(otherproducttup) <1 ):
        cursor.close()
        return ' '
    otherproductstr = ''.join(map(str, otherproducttup[0]))
#    print(otherproductstr)
    #return the productID
    finalproductnametup = cursor.exec("SELECT name FROM product WHERE product_id = '"+otherproductstr+"'")
    finalproductnamestr = ''.join(map(str, finalproductnametup[0]))
    #print(product_search(finalproductnamestr, "Any", "None", "priceup"))
    cursor.close()
    return product_search(finalproductnamestr, "Any", "None", "priceup")
    

"""
No longer needed if using Sponsor remove points, keeping code in case of breakage
def Davidsubpoints(userna, amount, spon_id):
    cursor.exec("UPDATE driver_bridge SET points = points - "+str(amount)+" WHERE driver_id = '"+str(userna)+"' AND sponsor_id = '"+str(spon_id)+"'")
    return ''
"""

def getprodinfo(pid):
    try:
        cursor = getConnection()
        prodinfo = cursor.exec("SELECT name, price, img_url FROM product WHERE product_id = %s" % pid)[0]
        cursor.close()
        return prodinfo
    except Exception as e:
        raise Exception(e)

#Trashed this and redoing based on sponsor catalogues only
def getpopitems(sponid):
#Grab a list of the most popular items in DESC order for the current sponsor
    cursor = getConnection()
    TopThreeTup = cursor.exec("SELECT Product_ID FROM Product_Orders WHERE Sponsor_ID = '"+str(sponid)+"' GROUP BY Product_ID ORDER BY COUNT(*) DESC")
#    print(TopThreeTup)
    TopThreeStr = []
    for i in range(0, 3):
        if(i >= len(TopThreeTup)):
            break
        TopThreeStr.append(''.join(map(str, TopThreeTup[i])))
#    print(TopThreeStr)
    for i in range(0, 3):
        if i >= len(TopThreeStr):
            break
        nametup = cursor.exec("SELECT name FROM product WHERE product_id = '"+TopThreeStr[i]+"'")
        TopThreeStr[i] = ''.join(map(str, nametup[0]))
    #Got the names of the top three
#    print(TopThreeStr)
    finallist = [' '] * 3
    for i in range(0,3):
        if(i >= len(TopThreeStr)):
            break
        temp = (product_search(TopThreeStr[i], sponid, "None", "priceup"))
        if len(temp) > 0:
            finallist[i] = temp[0]

#    print("Printing final list")
#    print(finallist)
#    print("End print")
    cursor.close()
    if(finallist[0] == ' '):
        return ' '
    return finallist

# Gets a list of products from all sponsors based on search
def get_products_by_name(search, id="ANY"):
    cursor = getConnection()
    if id == "ANY":
        query = "SELECT name FROM product WHERE name REGEXP(%s) and available=1"
        val = cursor.exec(query, (search, ))
    else:
        query = "SELECT name FROM product WHERE name REGEXP(%s) and sponsor_id=%s and available=1"
        val = cursor.exec(query, (search, id, ))
    matches = list(map(lambda x: x[0], val))
    cursor.close()
    return matches

# Updates the point conversion rate for a sponsor
def update_sponsor_rate(sponsor_id, rate):
    cursor = getConnection()
    sql = "UPDATE sponsor SET point_value=%s WHERE sponsor_id=%s"
    cursor.exec(sql, (rate, sponsor_id))
    cursor.close()

def get_point_value(sponsor_id):
    cursor = getConnection()
    sql = "SELECT point_value FROM sponsor WHERE sponsor_id=%s"
    result = cursor.exec(sql, (sponsor_id, ))

    # Return conversion rate if sponsor exists, otherwise, None
    cursor.close()
    if result:
        return result[0][0]
    else:
        return None

#main used to test functions
if __name__ == "__main__":
    """
    cancel_suspension('wsherre')
    if username_exist('krod'):
        add_driver('Kevin', 'NULL', 'Rodgers', 'krod', 'address', 5, 'email', 'cool', 'Null')
    if username_exist('bean'):
        add_driver('Bean', 'NULL', 'Rodgers', 'bean', 'address', 5, 'email', 'cool', 'Null')
    print(is_suspended('krod'))
    add_sponsor('Sponsor', 'spon', 'add', 0, 'email', 'pwd', '')
    add_admin('Admin', '', 'Cool', 'admin', 0, 'email', 'pwd', '')
    print(username_exist('krod'))
    get_users()
     print(admin_view_users())
    spons = [1,2,3]
 #   getnumproducts(3)    

    print("David recoo\n")
    recommend("testdrive")
    getpopitems()
    product_search(" ", "3", "None", "pricedown")


    """
#    addCart("socks")
#    getprodinfo(10)
#    getpopitems(3)
    recommend(17)
    """
    print("David Search\n")
    search = "Bike Tool: car: Luxury: sponge priceup"
    product_search(search) 
   
    drivers = sponsorless_drivers()
    for row in drivers:
        print(str(row[3]) +' is sponsorless')
    assign_driver_to_sponsor('krod', 1)
    assign_driver_to_sponsor('bean', 1)
    
    add_points_to_driver('krod', 1, 50)
    add_points_to_driver('bean', 1, 100)
    drivers = view_point_leaders(1)
    print(str(drivers[0][3]) + ': ' + str(drivers[0][5]))
    print(str(drivers[1][3]) + ': ' + str(drivers[1][5]))

    print("Add 200 to bean for being in top place, 100 to krod for second")

    add_points_for_leading_drivers(1, 200, 100, 50)
    drivers = view_point_leaders(1)
    print(str(drivers[0][3]) + ': ' + str(drivers[0][5]))
    print(str(drivers[1][3]) + ': ' + str(drivers[1][5]))
    

    print('krod\'s password \"cool\": ' + str(pwd_check('krod', 'cool')))
    print('spon\'s password \"password\": ' + str(pwd_check('spon', 'password')))
    print('admin\'s password \"pwd\": ' + str(pwd_check('admin', 'pwd')))

    change_password('krod', 'kool')
    print('krod\'s new password \"kool\": ' + str(pwd_check('krod', 'kool')))
    print("Suspending krod...")
    #suspend_driver('krod', 2020, 11, 30)
    print('Is krod suspended: ' + str(is_suspended('krod')))
    print("suspending spon...")
    #suspend_sponsor('spon', 2020, 12, 25)
    print("Is spon suspended: " + str(is_suspended('spon')))
    print(get_suspended_users())
    edit_suspension('krod', 2020, 11, 12)
    print(get_suspended_users())
    cancel_suspension('krod')
    print(get_suspended_users())
    print(if_username_exist('remove'))
    """
    


