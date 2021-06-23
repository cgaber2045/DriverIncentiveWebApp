try:
    from .db_connection import *
    from .db_functions import *
except Exception:
    from app.database.db_connection import *
    from app.database.db_functions import *

import os
from abc import ABC
from abc import abstractmethod
from werkzeug.security import check_password_hash

config = {'host': os.getenv('DB_HOST'), 'database': os.getenv('DB_NAME'), 'user': os.getenv('DB_USER'), 'password': os.getenv('DB_PASS'), 'autocommit': True}
global pool1
pool1 = ConnectionPool(size = 5, name = 'pool1', **config )

def getConnection(ex=0):
    global pool1
    if ex == 1:
        pool1.__del__()
        pool1 = ConnectionPool(size = 5, name = 'pool1', **config )
    else:
        print(pool1.size())
        return pool1.get_connection()

'''
def getNewConnection():
    return pool1.get_connection()
'''
def isActive(username):
    conn = getConnection()
    sql = 'SELECT Driver_ID, Sponsor_ID, Admin_ID FROM users WHERE UserName = \'{}\''.format(username)
    id = conn.exec(sql)
    if id[0][0] != None:
        query = "SELECT active FROM driver WHERE user = \'{}\'".format(username)
    elif id[0][1] != None:
        query = "SELECT active FROM sponsor_logins WHERE username = \'{}\'".format(username)
    else:
        query = "SELECT active FROM admin WHERE user = \'{}\'".format(username)
    active = conn.exec(query)
    conn.close()
    return active[0][0] == 1

class AbsUser(ABC):
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')

    def __init__(self):
        self.database = getConnection()

    @abstractmethod
    def add_user(self) -> None:
        """ Adds a user to the database """
        pass
    @abstractmethod
    def check_password(self, pwd_hash: str) -> bool:
        """ Checks if a user's password matches the one in the database"""
        pass
    @abstractmethod
    def check_username_available(self, username: str) -> bool:
        """ checkUsernameAvailable = True iff username not in db"""
        pass
    @abstractmethod
    def get_next_id(self) -> int:
        """ Returns the next available userID """
        pass
    @abstractmethod
    def get_users(self) -> list:
        """ Returns a list of all users in the DB """
        pass

    @abstractmethod
    def update_info(self) -> None:
        """ Updates a user's account info, e.g password, email, etc."""
        pass

    @abstractmethod
    def add_to_users(self):
        """adds to the user table"""

    @abstractmethod
    def get_user_data(self):
        """returns the user's data as a 2D array"""

    @abstractmethod
    def getUsername(self) -> str:
        """ Returns the username"""

    @abstractmethod
    def getRole(self) -> str:
        """ Returns the role"""

    @abstractmethod
    def getPoints(self) -> int:
        """ Returns points"""

    @abstractmethod
    def populate(self, username: str):
        """ populates the class with the data from the database"""

    @abstractmethod
    def delete(self):
        """ Deletes the user from the database """

class Admin(AbsUser):
    def __init__(self, fname='NULL', mname='NULL', lname='NULL', user='NULL', 
                 phone='NULL', email='NULL', pwd='NULL', image='NULL'):
        self.properties = {}
        self.properties['fname'] = fname
        self.properties['mname'] = mname
        self.properties['lname'] = lname
        self.properties['user'] = user
        self.properties['id'] = 0
        self.properties['phone'] = phone
        self.properties['email'] = email
        self.properties['pwd'] = pwd
        self.properties['image'] = image
        self.properties['date_join'] = 'NULL'
        self.properties['suspension'] = False
        self.properties['role'] = 'admin'
        self.properties['selectedSponsor'] = [1, 99999999]

        self.database = getConnection()

    def setLogIn(self, loggedIn):
        self.loggedIn = loggedIn

    # gets the next id from the database
    def get_next_id(self):
        query = 'SELECT MAX(admin_id) FROM admin'
        rows = self.database.exec(query)
        #self.database.close()
        
        if rows[0][0] == None:
            return 1
        else:
            return rows[0][0] + 1

    #adds the user to the database
    def add_user(self):
        self.properties['id'] = self.get_next_id()
        self.properties['END'] = 'NULL'
        self.properties['active'] = 1
        query = 'INSERT INTO admin VALUES (\'{fname}\', \'{mname}\', \'{lname}\', \'{user}\', \'{id}\', \'{phone}\', \'{email}\', \'{pwd}\', NOW(), \'{END}\', \'{active}\')'.format(**self.properties)
        
        
        try:
            self.database.exec(query)
            self.add_to_users()
            #self.database.close()

        except Exception as e:
            raise Exception(e)

    #compares the pwd_hash with the password in the database
    def check_password(self, pwd_hash):
        query = "SELECT pwd FROM admin WHERE user=%s"
        db_pwd = self.database.exec(query, self.properties['user'])
        #self.database.close()

        return check_password_hash(pwd_hash, db_pwd)

    #checks to see if the user name is available
    def check_username_available(self):
        query = "SELECT COUNT(*) FROM users WHERE UserName=\"{}\"".format(self.properties['user'])

        out = self.database.exec(query)
        #self.database.close()
        return out[0][0] == 0 or out == None

    #updates the info of the admin in the database. 
    def update_info(self, data: dict):
        
        query = "UPDATE admin SET "

        q_list = []
        for key in data.keys():
            q_list.append("{} = %s".format(key))

        query += ", ".join(q_list) + " WHERE user=\"{}\"".format(self.properties['user'])

        try:
            self.database.exec(query, args=tuple(data.values()))
            #self.database.close()

        except Exception as e:
            raise Exception(e)

    def get_users(self):
        query = "SELECT * FROM admin WHERE active = 1"

        try:
            out = self.database.exec(query)
            #self.database.close()
        except Exception as e:
            raise Exception(e)
        if out:
            return out
        else:
            return []

    # returns user data as a 2D array in the following format
    # [0][0] = first name
    # [0][1] = middle name
    # [0][2] = last name
    # [0][3] = username
    # [0][4] = id number
    # [0][5] = phone
    # [0][6] = email
    # [0][7] = image which should be null
    # [0][8] = date_join
    def get_user_data(self):
        query = 'SELECT first_name, mid_name, last_name, user, admin_id, phone, email, image, date_join FROM admin WHERE user = %s'
        val = (self.properties['user'], )


        try:
            data = self.database.exec(query, val)
            #self.database.close()
            return data

        except Exception as e:
            raise Exception(e)
    
    def add_to_users(self):

        query = 'INSERT INTO users (Username, {}, last_in) VALUES (\'{}\', {}, CURRENT_TIMESTAMP())'
        query = query.format('Admin_ID', self.properties['user'], self.properties['id'])
        self.database.exec(query)
        self.database.commit()

    def getUsername(self):
        return self.properties['user']
    
    def getRole(self):
        return self.properties['role']

    def getPoints(self):
        return self.properties['points']

    def populate(self, username: str):
        #self.database = getNewConnection()
        query = 'SELECT first_name, mid_name, last_name, user, admin_id, phone, email, date_join FROM admin WHERE user = %s'
        vals = (username, )

        try:
            data = self.database.exec(query, vals)
            #self.database.close()

        except Exception as e:
            raise Exception(e)

        if data:
            self.properties['fname'] = data[0][0]
            self.properties['mname'] = data[0][1]
            self.properties['lname'] = data[0][2]
            self.properties['user'] = data[0][3]
            self.properties['id'] = data[0][4]
            self.properties['phone'] = data[0][5]
            self.properties['email'] = data[0][6]
            self.properties['pwd'] = 'NULL'
            self.properties['date_join'] = data[0][7]

    #this function returns true if a driver is currently suspended
    def is_suspended(self):
        
        sql = 'SELECT user FROM suspend WHERE user = %s'
        val = (self.properties['user'], )

        
        #this will remove suspended driver's whos suspensions are over
        try:
            self.database.exec('DELETE from suspend WHERE date_return <= NOW()')
            suspended_user = self.database.exec(sql, val)
        except Exception as e:
            raise Exception(e)
        
        if suspended_user == None:
            return False
        else:
            return True

    #this function adds a driver to a suspension list and their length of suspension
    def suspend_user(self, username, year, month, day):


        #change the time into a string
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)

        year = str(year)
        day = str(day)
        
        str_date = year + '-' + month + '-' + day

        query = 'INSERT INTO suspend VALUES (%s, %s)'
        vals = (username, str_date)
        try:
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def edit_suspension(self, username, year, month, day):       
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)

        year = str(year)
        day = str(day)
        
        str_date = year + '-' + month + '-' + day
        query = 'UPDATE suspend SET date_return = %s WHERE user = %s'
        vals = (str_date, username)
        try:
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def get_suspended_users(self):
        try:
            sus = self.database.exec('SELECT user FROM suspend')
            #self.database.close()
        except Exception as e:
            raise Exception(e)
        sus_list = []
    
        if sus:
            for s in sus:
                sus_list.append(s[0])
        return sus_list

    def cancel_suspension(self, username):

        #self.database = getNewConnection()
        query = 'DELETE FROM suspend WHERE user = %s'
        vals = (username, )
        try:
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)
        

    def remove_user(self, username):

        #self.database = getNewConnection()
        username = str(username).strip()

        #if username is sponsor title
        title = self.database.exec('SELECT title from sponsor')
        title_list = []
        for x in title:
            title_list.append(x[0])
        if username in title_list:
            username = self.database.exec('SELECT username from sponsor_logins where sponsor_id = (SELECT sponsor_id from sponsor WHERE title = %s)', (username, ))[0][0]

        sql = 'SELECT Driver_ID, Sponsor_ID FROM users WHERE UserName = \'{}\''.format(username)
        id = self.database.exec(sql)
        if id[0][0] != None:
            role = 'driver'
        elif id[0][1] != None:
            role = 'sponsor'
        else:
            role = 'admin'

        query = 'UPDATE ' + role + ' SET active = 0 WHERE user = %s'
        val = (username, )
        if role == 'sponsor':
            query = 'UPDATE sponsor_logins SET active = 0 where sponsor_id = %s'
            val = (id[0][1], )
        
        try:
            self.database.exec('DELETE FROM suspend WHERE user = %s', (username, ))
            self.database.exec(query, val)
            #self.database.close()
        except Exception as e:
            raise Exception(e)


    #add a driver to a sponsor, takes in their id numbers
    def add_to_sponsor(self, driver_id, sponsor_id):
        bridge_query = 'INSERT INTO driver_bridge VALUES (%s, %s, 0, 0)'
        points_query = 'INSERT INTO points_leaderboard VALUES (%s, %s, 0)'
        vals = (driver_id, sponsor_id)
    
        try:
            self.database.exec(bridge_query, vals)
            self.database.exec(points_query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def get_sponsorless_drivers(self):
        sql = 'SELECT driver.user, driver.first_name, driver.last_name, driver.driver_id, driver.date_join FROM driver JOIN driver_bridge USING(driver_id) JOIN sponsor_logins USING(sponsor_id) WHERE ((SELECT COUNT(*) FROM sponsor_logins WHERE active = 0 AND sponsor_id = driver_bridge.sponsor_id) > 0) union SELECT driver.user, driver.first_name, driver.last_name, driver.driver_id, driver.date_join FROM driver WHERE driver.driver_id NOT IN (SELECT driver.driver_id FROM driver INNER JOIN driver_bridge WHERE driver.driver_id = driver_bridge.driver_id AND driver_bridge.apply=0) AND active = 1'
        
        try:
            data = self.database.exec(sql)
            #self.database.close()
        except Exception as e:
            raise Exception(e)
        if data:
            return data
        else:
            return []

    def get_disabled_drivers(self):
        sql = 'select user, first_name, last_name, driver_id, date_join FROM driver WHERE active = 0'
        
        try:
            data = self.database.exec(sql)
            #self.database.close()
        except Exception as e:
            raise Exception(e)
        if data:
            return data
        else:
            return []
    
    def get_disabled_sponsors(self):
        sql = 'select sponsor_logins.username, title, sponsor_id, sponsor_logins.date_join FROM sponsor join sponsor_logins USING(sponsor_id) WHERE sponsor_logins.active = 0'
        
        try:
            data = self.database.exec(sql)
            #self.database.close()
        except Exception as e:
            raise Exception(e)
        if data:
            return data
        else:
            return []

    def get_disabled_admins(self):
        sql = 'select user, first_name, last_name, admin_id, date_join FROM admin WHERE active = 0'
        
        try:
            data = self.database.exec(sql)
            #self.database.close()
        except Exception as e:
            raise Exception(e)
        if data:
            return data
        else:
            return []

    def reactivate_user(self, username):
        sql = 'SELECT Driver_ID, Sponsor_ID, Admin_ID FROM users WHERE UserName = \'{}\''.format(username)
        id = self.database.exec(sql)
        if id[0][0] != None:
            role =  'driver'
        elif id[0][1] != None:
            role =  'sponsor'
        else:
            role = 'admin'
        
        query = 'UPDATE ' + role + ' SET active = 1 WHERE user = \'{}\''.format(username)
        if role == 'sponsor':
            query = "UPDATE sponsor_logins SET active = 1 WHERE sponsor_id = {}".format(id[0][1])
        try:
            data = self.database.exec(query)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    #gets a list of current users that this user has a messsage from
    def get_inbox_list(self):
        #select all message that have not yet been read that involve this user
        message_query = 'SELECT * FROM messages WHERE (target = %s AND seent = 0) OR (sender = %s AND seens = 0) '
        vals = (self.properties['user'], self.properties['user'])

        try:
            #do some awesome database magic
            data = self.database.exec(message_query, vals)
        except Exception as e:
            raise Exception(e)

        user_list = []
        #if there is any data from the database
        if data:
            #loop through every message it returns
            for d in data:
                #if the TARGET is not already in the list AND it is not this user, add to the list
                if (d[0] not in user_list) and (d[0] != self.properties['user']):
                    user_list.append(d[0])
                #if the SENDER is not already in the list AND it is not this user, add to the list
                elif (d[1] not in user_list) and (d[1] != self.properties['user']):                       
                    user_list.append(d[1])

        return user_list
    #mark messages as aseen
    def messages_are_seen(self, user):
        #flag in case the user wants to mark all as seen
        if user == "MARK_ALL":
            query = 'UPDATE messages SET seens = 1 WHERE sender = %s'
            query2 = 'UPDATE messages SET seent = 1 WHERE target = %s'
            val = (self.properties['user'], )
            try:
                self.database.exec(query, val)
                self.database.exec(query2, val)
                #self.database.close()
            except Exception as e:
                raise Exception(e)
        else:
            #set the flags where the sender and target (that is this user) has seen the conversation
            query = 'UPDATE messages SET seent = 1 WHERE (target = %s AND sender = %s)'
            query2 = 'UPDATE messages SET seens = 1 WHERE (target = %s AND sender = %s)'
            val1 = (self.properties['user'], user)
            val2 = (user, self.properties['user'])
            try:
                self.database.exec(query, val1)
                self.database.exec(query2, val2)
                #self.database.close()
            except Exception as e:
                raise Exception(e)

    #get info of the other user in the conversation
    def get_msg_info(self, user):
        sql = 'SELECT Driver_ID, Sponsor_ID, Admin_ID FROM users WHERE UserName = %s'
        val = (user, )
        id = self.database.exec(sql, val)
        if id[0][0] != None:
            role =  'driver'
        elif id[0][1] != None:
            role =  'sponsor'
        else:
            role = 'admin'
        
        if role == 'driver' or role == 'admin':
            query = 'SELECT first_name, last_name, active FROM ' + role + ' WHERE user = %s'
        else:
            query = 'SELECT sponsor.title, sponsor_logins.active FROM sponsor join sponsor_logins using(sponsor_id) WHERE sponsor_logins.username = %s'
        val = (user, )
        
        try:
            data = self.database.exec(query, val)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        data_list = list(data[0])
        data_list.insert(0, role)
        return data_list

    # return a list of lists with each list being a new message with the sender, msg, and timestamp being in each list
    #the first list will contain info about the other user in the convo
    def view_messages(self):
        message_query = 'SELECT * FROM messages WHERE target = %s OR sender = %s ORDER BY time DESC'
        vals = (self.properties['user'], self.properties['user'])

        try:
            data = self.database.exec(message_query, vals)
        except Exception as e:
            raise Exception(e)

        message_dict = {}

        if data:
            #for each message this user has
            for d in data:
                #the list is currently the keys of our message dictionary
                user_list = list(message_dict.keys())
                #if the target is not in the list and is not the user
                if (d[0] not in user_list) and (d[0] != self.properties['user']):

                    #make a new key in the dictionary 
                    message_dict[d[0]] = []

                    #get info about user from database
                    info = self.get_msg_info(d[0])

                    #if user is inactive add disabled tag to their last name and remove the tag from the list
                    if info[len(info) - 1] == 0:
                        info[len(info) - 2] += '(Disabled)'
                    info.pop(len(info) - 1)

                    #add their info to the dictionary
                    message_dict[d[0]].append(info)

                    #flag for appending will user later
                    user = 0

                #if the sender is not in the list and is not the user
                elif (d[1] not in user_list) and (d[1] != self.properties['user']):

                    #make a new key in the dictionary 
                    message_dict[d[1]] = []

                    #get info about user from database
                    info = self.get_msg_info(d[1])

                    #if user is inactive add disabled tag to their last name and remove the tag from the list
                    if info[len(info) - 1] == 0:
                        info[len(info) - 2] += '(Disabled)'
                    info.pop(len(info) - 1)

                    #add their info to the dictionary
                    message_dict[d[1]].append(info)

                    #flag for appending will user later
                    user = 1
                #if the user is us so we can talk to ourselves :)
                elif(d[0] == self.properties['user'] and d[1] == self.properties['user'] and d[0] not in user_list):
                    message_dict[d[0]] = []
                    info = self.get_msg_info(d[0])
                    if info[len(info) - 1] == 0:
                        info[len(info) - 2] += '(Disabled)'
                    info.pop(len(info) - 1)
                    message_dict[d[0]].append(info)
                    user = 0
                else:
                    if d[0] != self.properties['user']:
                        user = 0
                    else:
                        user = 1
                #add the message to the dictionary, insert into the first spot (most recent message) with d[user] being their name
                #d[1] being the sender in the convo, d[2] the message, and d[3] the timestamp
                message_dict[d[user]].insert(1, (d[1], d[2], d[3]))
        
        return message_dict

    #send a message to another user
    #the target is the username of the user you want to send a message to
    #the message is what you're getting them for dinner
    #....lol jk
    def send_message(self, target, message):
        time = 'SET time_zone = \'{}\''.format("America/New_York")
        query = 'INSERT INTO messages VALUES (%s, %s, %s, NOW(), 0, 1)'
        vals = (target, self.properties['user'], message)

        try:
            self.database.exec(time)
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)
    
    def getProductInfo(self, id):
        query = 'SELECT name, price, img_url FROM product WHERE product_id = %s'
        val = (id)

        try:
            data = self.database.exec(query, val)
        except Exception as e:
            raise Exception(e)

        datalist = list(data[0])
        return datalist

    def upload_image(self, tempf):
        with open(tempf, 'rb') as file:
            image = file.read()

        sql = 'UPDATE driver SET image = %s WHERE user = %s'
        vals = (image, self.properties['user'])

        try:
            self.database.exec(sql, vals)
            self.properties['image'] = image
            #self.database.close()
        except Exception as e:
            raise Exception(e)


    def download_image(self, tempf):
        with open(tempf, 'wb') as file:
            file.write(self.properties['image'])

        return file

    def change_password(self, new_pwd):
        query = 'UPDATE admin SET pwd = %s WHERE user = %s'
        vals = (new_pwd, self.properties['user'])

        try:
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def delete(self):
        """ Disables an admin """
        

        query = "UPDATE admin SET active = 0 WHERE admin_id=%s"
        vals = (self.properties['id'], )
        try:
            self.database.exec(user_query, user_vals)
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def __del__(self):
        global pool1
        self.database.close()
        ##print(pool1.size())
        

class Sponsor(AbsUser):
    def __init__(self, title='NULL', user='NULL', address='NULL', phone='NULL', 
                    email='NULL', pwd='NULL', image='NULL'):
        self.properties = {}
        self.properties['title'] = title
        self.properties['user'] = user
        self.properties['address'] = address
        self.properties['phone'] = phone
        self.properties['email'] = email
        self.properties['pwd'] = pwd
        self.properties['image'] = image
        self.properties['id'] = 0
        self.properties['date_join'] = 'NULL'
        self.properties['suspension'] = False
        self.properties['role'] = 'sponsor'
        self.properties['points'] = 99999999
        self.properties['selectedSponsor'] = [1, 9999999]
        self.properties['point_value'] = 0.01
        self.database = getConnection()

    def setLogIn(self, loggedIn):
        self.loggedIn = loggedIn

    def get_next_id(self):
        query = 'SELECT MAX(sponsor_id) FROM sponsor'
        rows = self.database.exec(query)
        #self.database.close()
        
        if rows[0][0] == None:
            return 1
        else:
            return rows[0][0] + 1
    
    def add_user(self):
        self.properties['id'] = self.get_next_id()
        self.properties['active'] = 1
        self.properties['END'] = 'NULL'
        query = 'INSERT INTO sponsor VALUES (\'{title}\', \'{id}\', \'{address}\', \'{phone}\', \'{email}\', \'{image}\', NOW(), \'{END}\', 0.01)'.format(**self.properties)

        # Filter properties to be all except selectedSponsor because list issue
        #params = dict(filter(lambda x: x[0] != 'selectedSponsor', self.properties.items()))
        try:
            self.database.exec(query)
            self.add_new_sponsor_login(self.properties['user'], self.properties['pwd'])
            #self.database.close()

        except Exception as e:
            raise Exception(e)

    def check_password(self, pwd_hash):
        query = "SELECT password FROM sponsor_logins WHERE username=%s"
        db_pwd = self.database.exec(query, self.properties['user'])
        #self.database.close()

        return check_password_hash(pwd_hash, db_pwd)


    def check_username_available(self):
        query = "SELECT COUNT(*) FROM users WHERE UserName=\"{}\"".format(self.properties['user'])

        out = self.database.exec(query) 
        #self.database.close()
        return out[0][0] == 0 or out == None

    def update_info(self, data: dict):
        
        query = "UPDATE sponsor SET "

        q_list = []
        for key in data.keys():
            if key != 'pwd':
                q_list.append("{} = %s".format(key))

        query += ", ".join(q_list) + " WHERE sponsor_id=\"{}\"".format(self.properties['id'])

        if 'pwd' in data.keys():
            val = data['pwd']
            del data['pwd']
            q = "UPDATE sponsor_logins SET password = %s WHERE username = %s"
            vals = (val, self.properties['user'])
            self.database.exec(q, vals)

        try:
            if data:
                self.database.exec(query, args=tuple(data.values()))
            #self.database.close()

        except Exception as e:
            raise Exception(e)

    def get_users(self):
        query = "SELECT title, sponsor_id, address, phone, email, image, sponsor_logins.date_join, sponsor_logins.username FROM sponsor inner join sponsor_logins using(sponsor_id) WHERE sponsor_logins.active = 1"

        try:
            out = self.database.exec(query)
            #self.database.close()
        except Exception as e:
            raise Exception(e)
        if out:
            return out
        else:
            return []

    # returns user data as a 2D array in the following formart
    # [0][0] = title
    # [0][1] = username
    # [0][2] = id number
    # [0][3] = address
    # [0][4] = phone
    # [0][5] = email
    # [0][6] = image should be null for now
    # [0][7] = date that was join
    def get_user_data(self):
        query = 'SELECT title, user, sponsor_id, address, phone, email, image, date_join FROM sponsor WHERE user = %s'
        val = (self.properties['user'], )


        try:
            data = self.database.exec(query, val)
            #self.database.close()
            return data

        except Exception as e:
            raise Exception(e)

    #here to satisfy interface, can't use because I need to pass in variables
    def add_to_users(self):
        pass
        query = 'INSERT INTO users (Username, Sponsor_ID, last_in) VALUES (\'{}\', {}, CURRENT_TIMESTAMP())'
        query = query.format(self.properties['user'], self.properties['id'])
        self.database.exec(query)
        #self.database.close()

    def add_new_sponsor_login(self, username, pwd):
        query = 'INSERT INTO users (Username, Sponsor_ID, last_in) VALUES (\'{}\', {}, CURRENT_TIMESTAMP())'.format(username, self.properties['id'])
        q_login = 'INSERT INTO sponsor_logins VALUES (%s, %s, %s, %s, NOW())'
        q_vals = (username, pwd, self.properties['id'], 1)
        try:
            self.database.exec(query)
            self.database.exec(q_login, q_vals)
        except Exception as e:
            raise Exception(e)

    def getUsername(self):
        return self.properties['user']
    
    def getRole(self):
        return  self.properties['role']

    def getPoints(self):
        return 999999

    def username_from_id(self, id):
        sql = "SELECT title FROM sponsor WHERE sponsor_id = %s"
        val = (id, )

        try:
            data = self.database.exec(sql, val)
            #self.database.close()
        except Exception as e:
            raise Exception(e)
        
        return data[0][0]

    def populate(self, username: str):
        #self.database = getNewConnection()
        #if passing in title as name, pick the first username of that sponsor to populate
        title = self.database.exec('SELECT title from sponsor')
        title_list = []
        for x in title:
            title_list.append(x[0])
        if username in title_list:
            username = self.database.exec('SELECT username from sponsor_logins where sponsor_id = (SELECT sponsor_id from sponsor WHERE title = %s)', (username, ))[0][0]

        query = 'SELECT title, sponsor_logins.username, sponsor_id, address, phone, email, image, sponsor_logins.date_join, point_value FROM sponsor JOIN sponsor_logins USING(sponsor_id) WHERE sponsor_logins.username = %s'
        vals = (username, )

        try:
            data = self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)


        if data:
            self.properties['title'] = data[0][0]
            self.properties['user'] = data[0][1]
            self.properties['id'] = data[0][2]
            self.properties['address'] = data[0][3]
            self.properties['phone'] = data[0][4]
            self.properties['email'] = data[0][5]
            self.properties['pwd'] = 'NULL'
            self.properties['image'] = data[0][6]
            self.properties['date_join'] = data[0][7]
            self.properties['point_value'] = data[0][8]

    def is_suspended(self):
        
        sql = 'SELECT user FROM suspend WHERE user = %s'
        val = (self.properties['user'], )

        try:
            #this will remove suspended driver's whos suspensions are over
            self.database.exec('DELETE from suspend WHERE date_return <= NOW()')
            suspended_user = self.database.exec(sql, val)
            #self.database.close()
        except Exception as e:
            raise Exception(e)
        
        if suspended_user == None:
            return False
        else:
            return True

    def edit_suspension(self, username, year, month, day):       
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)

        year = str(year)
        day = str(day)
        
        str_date = year + '-' + month + '-' + day
        query = 'UPDATE suspend SET date_return = %s WHERE user = %s'
        vals = (str_date, username)
        try:
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def get_suspended_users(self):
        #self.database = getNewConnection()
        sus = self.database.exec('SELECT user FROM suspend')
        sus_list = []
        
        for s in sus:
            sus_list.append(s[0])
        return sus_list

    def cancel_suspension(self, username):
        query = 'DELETE FROM suspend WHERE user = %s'
        vals = (username, )
        try:
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def view_applications(self):
        query = 'SELECT driver.user, driver.first_name, driver.last_name, driver.driver_id FROM driver INNER JOIN driver_bridge ON driver.driver_id = driver_bridge.driver_id WHERE driver_bridge.sponsor_id = %s AND apply = 1 AND active = 1'
        vals = (self.properties['id'], )

        try: 
            apps = self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        return apps


    def view_drivers(self):
        query = 'SELECT driver.first_name, driver.mid_name, driver.last_name, driver.user, driver_bridge.points, driver.date_join FROM driver INNER JOIN driver_bridge ON driver.driver_id = driver_bridge.driver_id WHERE driver_bridge.sponsor_id = %s AND apply = 0 AND active = 1 ORDER BY driver_bridge.points DESC'
        vals = (self.properties['id'], )

        try: 
            drivers = self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        return drivers


    def accept_application(self, driver_id):
        bridge = 'UPDATE driver_bridge SET apply = 0 WHERE driver_id = %s AND sponsor_id = %s'
        leader = 'INSERT INTO points_leaderboard VALUES (%s, %s, 0)'
        vals = (driver_id, self.properties['id'])

        try: 
            self.database.exec(bridge, vals)
            self.database.exec(leader, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        #send a message to the driver
        query = 'select user from driver where driver_id = %s'
        val = (driver_id, )
        username = self.database.exec(query, val)[0][0]
        system = Admin()
        system.populate('System')
        system.send_message(username, 'Congratulations your sponsor application has been reviewed and accepted by {}!'.format(self.properties['user']))

    def decline_application(self, driver_id):
        query = 'DELETE FROM driver_bridge WHERE driver_id = %s AND sponsor_id = %s'
        vals = (driver_id, self.properties['id'])

        try: 
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        #send a message to the driver
        query = 'select user from driver where driver_id = %s'
        val = (driver_id, )
        username = self.database.exec(query, val)[0][0]
        system = Admin().populate('System')
        system.send_message(username, '{} has reviewed and denied your request.'.format(self.properties['user']))

    #add points to the driver, enter their driver_id and amount of points you want to give them
    # IF NEGATIVE POINTS ARE GREATER THAN CURRENT POINTS (basically they don't have enough points for the purchase) THIS FUNCTION WILL RETURN FALSE
    def add_points(self, driver_id, add_points):

        #get the driver's points
        data = self.database.exec('SELECT points FROM driver_bridge WHERE driver_id = %s AND sponsor_id = %s AND apply = 0', (driver_id, self.properties['id']))
        current_points = data[0][0]

        #add the points to the current points
        new_point_value = current_points + add_points

        #evaluate the points. if they don't have enough points and want an issue notificiation. send it. 
        if new_point_value < 0:
            query = 'select notification.user, notification.issue from notification inner join driver on notification.user = driver.user where driver.driver_id = %s'
            val = (driver_id, )
            data = self.database.exec(query, val)
            username = data[0][0]
            issue_noti = data[0][1]
            #if they want notifications for points added/subtracted, tell em
            if issue_noti == 1:
                system = Admin()
                system.populate('System')
                msg = 'ERROR: You have in sufficient points for a purchase for sponsor {}. Current points: {}  Purchase Price: {}'.format(self.properties['title'], current_points, abs(add_points))
                system.send_message(username, msg)
            return False

        else:
            #update their new point value
            query = 'UPDATE driver_bridge SET points = %s WHERE driver_id = %s AND sponsor_id = %s'
            vals = (new_point_value, driver_id, self.properties['id'])
            try: 
                self.database.exec(query, vals)
            except Exception as e:
                raise Exception(e)
             
             #get their leaderboard points
            data = self.database.exec('SELECT points FROM points_leaderboard WHERE driver_id = %s AND sponsor_id = %s', (driver_id, self.properties['id']))
            leader_points = data[0][0]
            #only update the leaderboard points if they are gaining points
            if add_points > 0:
                leader_points += add_points
                leader = 'UPDATE points_leaderboard SET points = %s WHERE driver_id = %s AND sponsor_id = %s'
                vals = (leader_points, driver_id, self.properties['id'])
                try: 
                    self.database.exec(leader, vals)
                except Exception as e:
                    raise Exception(e)
            #send message to user
            #get username and points notification
            query = 'select notification.user, notification.points from notification inner join driver on notification.user = driver.user where driver.driver_id = %s'
            val = (driver_id, )
            data = self.database.exec(query, val)
            username = data[0][0]
            points_noti = data[0][1]
            #if they want notifications for points added/subtracted, tell em
            if points_noti == 1:
                system = Admin()
                system.populate('System')
                if add_points > 0:
                    msg = 'You have gained {} points for sponsor {}. Your total is now: {}'.format(add_points, self.properties['user'], new_point_value)
                else:
                    msg = 'You have lost {} points for sponsor {}. Your total is now {}'.format(add_points, self.properties['user'], new_point_value)
                system.send_message(username, msg)
            

    def view_leaderboard(self):
        query = 'SELECT driver.first_name, driver.mid_name, driver.last_name, driver.user, points_leaderboard.points FROM driver INNER JOIN points_leaderboard ON driver.driver_id = points_leaderboard.driver_id WHERE sponsor_id = %s  AND active = 1 ORDER BY points_leaderboard.points DESC'
        val = (self.properties['id'], )

        try: 
            leaders = self.database.exec(query, val)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        return leaders


    def remove_driver(self, driver_id):
        query = 'DELETE FROM driver_bridge WHERE driver_id = %s AND sponsor_id = %s'
        remove_leader = 'DELETE FROM points_leaderboard WHERE driver_id = %s and sponsor_id = %s'
        vals = (driver_id, self.properties['id'])

        try: 
            self.database.exec(query, vals)
            self.database.exec(remove_leader, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        #send message to driver
        query = 'select user from driver where driver_id = %s'
        val = (driver_id, )
        username = self.database.exec(query, val)[0][0]
        system = Admin()
        system.populate('System')
        system.send_message(username, 'You have been removed as a driver from {}!'.format(self.properties['user']))

    #gets a list of current users that this user has a messsage from
    def get_inbox_list(self):
        #select all message that have not yet been read that involve this user
        message_query = 'SELECT * FROM messages WHERE (target = %s AND seent = 0) OR (sender = %s AND seens = 0) '
        vals = (self.properties['user'], self.properties['user'])

        try:
            #do some awesome database magic
            data = self.database.exec(message_query, vals)
        except Exception as e:
            raise Exception(e)

        user_list = []
        #if there is any data from the database
        if data:
            #loop through every message it returns
            for d in data:
                #if the TARGET is not already in the list AND it is not this user, add to the list
                if (d[0] not in user_list) and (d[0] != self.properties['user']):
                    user_list.append(d[0])
                #if the SENDER is not already in the list AND it is not this user, add to the list
                elif (d[1] not in user_list) and (d[1] != self.properties['user']):                       
                    user_list.append(d[1])

        return user_list
    #mark messages as aseen
    def messages_are_seen(self, user):
        #flag in case the user wants to mark all as seen
        if user == "MARK_ALL":
            query = 'UPDATE messages SET seens = 1 WHERE sender = %s'
            query2 = 'UPDATE messages SET seent = 1 WHERE target = %s'
            val = (self.properties['user'], )
            try:
                self.database.exec(query, val)
                self.database.exec(query2, val)
                #self.database.close()
            except Exception as e:
                raise Exception(e)
        else:
            #set the flags where the sender and target (that is this user) has seen the conversation
            query = 'UPDATE messages SET seent = 1 WHERE (target = %s AND sender = %s)'
            query2 = 'UPDATE messages SET seens = 1 WHERE (target = %s AND sender = %s)'
            val1 = (self.properties['user'], user)
            val2 = (user, self.properties['user'])
            try:
                self.database.exec(query, val1)
                self.database.exec(query2, val2)
                #self.database.close()
            except Exception as e:
                raise Exception(e)

    #get info of the other user in the conversation
    def get_msg_info(self, user):
        sql = 'SELECT Driver_ID, Sponsor_ID, Admin_ID FROM users WHERE UserName = %s'
        val = (user, )
        id = self.database.exec(sql, val)
        if id[0][0] != None:
            role =  'driver'
        elif id[0][1] != None:
            role =  'sponsor'
        else:
            role = 'admin'
        
        if role == 'driver' or role == 'admin':
            query = 'SELECT first_name, last_name, active FROM ' + role + ' WHERE user = %s'
        else:
            query = 'SELECT sponsor.title, sponsor_logins.active FROM sponsor join sponsor_logins using(sponsor_id) WHERE sponsor_logins.username = %s'
        val = (user, )
        
        try:
            data = self.database.exec(query, val)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        data_list = list(data[0])
        data_list.insert(0, role)
        return data_list

    # return a list of lists with each list being a new message with the sender, msg, and timestamp being in each list
    #the first list will contain info about the other user in the convo
    def view_messages(self):
        message_query = 'SELECT * FROM messages WHERE target = %s OR sender = %s ORDER BY time DESC'
        vals = (self.properties['user'], self.properties['user'])

        try:
            data = self.database.exec(message_query, vals)
        except Exception as e:
            raise Exception(e)

        message_dict = {}

        if data:
            #for each message this user has
            for d in data:
                #the list is currently the keys of our message dictionary
                user_list = list(message_dict.keys())
                #if the target is not in the list and is not the user
                if (d[0] not in user_list) and (d[0] != self.properties['user']):

                    #make a new key in the dictionary 
                    message_dict[d[0]] = []

                    #get info about user from database
                    info = self.get_msg_info(d[0])

                    #if user is inactive add disabled tag to their last name and remove the tag from the list
                    if info[len(info) - 1] == 0:
                        info[len(info) - 2] += '(Disabled)'
                    info.pop(len(info) - 1)

                    #add their info to the dictionary
                    message_dict[d[0]].append(info)

                    #flag for appending will user later
                    user = 0

                #if the sender is not in the list and is not the user
                elif (d[1] not in user_list) and (d[1] != self.properties['user']):

                    #make a new key in the dictionary 
                    message_dict[d[1]] = []

                    #get info about user from database
                    info = self.get_msg_info(d[1])

                    #if user is inactive add disabled tag to their last name and remove the tag from the list
                    if info[len(info) - 1] == 0:
                        info[len(info) - 2] += '(Disabled)'
                    info.pop(len(info) - 1)

                    #add their info to the dictionary
                    message_dict[d[1]].append(info)

                    #flag for appending will user later
                    user = 1
                #if the user is us so we can talk to ourselves :)
                elif(d[0] == self.properties['user'] and d[1] == self.properties['user'] and d[0] not in user_list):
                    message_dict[d[0]] = []
                    info = self.get_msg_info(d[0])
                    if info[len(info) - 1] == 0:
                        info[len(info) - 2] += '(Disabled)'
                    info.pop(len(info) - 1)
                    message_dict[d[0]].append(info)
                    user = 0
                else:
                    if d[0] != self.properties['user']:
                        user = 0
                    else:
                        user = 1
                #add the message to the dictionary, insert into the first spot (most recent message) with d[user] being their name
                #d[1] being the sender in the convo, d[2] the message, and d[3] the timestamp
                message_dict[d[user]].insert(1, (d[1], d[2], d[3]))
        
        return message_dict

    #send a message to another user
    #the target is the username of the user you want to send a message to
    #the message is what you're getting them for dinner
    #....lol jk
    def send_message(self, target, message):
        time = 'SET time_zone = \'{}\''.format("America/New_York")
        query = 'INSERT INTO messages VALUES (%s, %s, %s, NOW(), 0, 1)'
        vals = (target, self.properties['user'], message)

        try:
            self.database.exec(time)
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    
    def upload_image(self, tempf):
        with open(tempf, 'rb') as file:
            image = file.read()

        sql = 'UPDATE driver SET image = %s WHERE user = %s'
        vals = (image, self.properties['user'])

        try:
            self.database.exec(sql, vals)
            #self.database.close()
            self.properties['image'] = image
        except Exception as e:
            raise Exception(e)

    def download_image(self, tempf):
        with open(tempf, 'wb') as file:
            file.write(self.properties['image'])

        return file
        
    #this function adds a driver to a suspension list and their length of suspension
    def suspend_user(self, username, year, month, day):

        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)

        year = str(year)
        day = str(day)
        
        str_date = year + '-' + month + '-' + day

        query = 'INSERT INTO suspend VALUES (%s, %s)'
        vals = (username, str_date)
        try:
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def change_password(self, new_pwd):
        query = 'UPDATE sponsor SET pwd = %s WHERE user = %s'
        vals = (new_pwd, self.properties['user'])

        try:
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)


    def delete(self):
        """ Deletes a sponsor from the users table and from the sponsor table """

        query = "UPDATE sponsor SET active = 0 WHERE sponsor_id=%s"
        vals = (self.properties['id'], )
        try:
            self.database.exec(user_query, user_vals)
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def __del__(self):
        global pool1
        self.database.close()
        ##print(pool1.size())
        


class Driver(AbsUser):
    def __init__(self, fname='NULL', mname='NULL', lname='NULL', user='NULL', 
                 address='NULL', phone='NULL', email='NULL', pwd='NULL', image='NULL'):
        # Dictionary to keep track of driver data
        self.properties = {}
        self.properties['fname'] = fname
        self.properties['mname'] = mname
        self.properties['lname'] = lname
        self.properties['user'] = user
        self.properties['id'] = 0
        self.properties['sponsors'] = {}
        self.properties['address'] = address
        self.properties['phone'] = phone
        self.properties['email'] = email
        self.properties['pwd'] = pwd
        self.properties['image'] = image
        self.properties['date_join'] = 'NULL'
        self.properties['suspension'] = False
        self.properties['role'] = 'driver'
        self.properties['selectedSponsor'] = None

        self.database = getConnection()

    def setLogIn(self, loggedIn):
        self.loggedIn = loggedIn
        
    def get_next_id(self):
        query = 'SELECT MAX(driver_id) FROM driver'
        rows = self.database.exec(query)
        
        if rows[0][0] == None:
            return 1
        else:
            return rows[0][0] + 1

    def add_user(self):
        self.properties['id'] = self.get_next_id()
        self.properties['END'] = 'NULL'
        self.properties['active'] = 1
        query = 'INSERT INTO driver VALUES (\'{fname}\', \'{mname}\', \'{lname}\', \'{user}\', \'{id}\', \'{address}\', \'{phone}\', \'{email}\', \'{pwd}\', NOW(), \'{END}\', \'{image}\', \'{active}\')'.format(**self.properties)
        noti = 'INSERT INTO notification VALUES (\'{}\', 1, 1, 1)'.format(self.properties['user'])

        try:
            self.database.exec(query)
            self.database.exec(noti)
            self.add_to_users()
            #self.database.close()

        except Exception as e:
            raise Exception(e)

    def check_password(self, pwd_hash):
        query = "SELECT pwd FROM driver WHERE user=%s"
        db_pwd = self.database.exec(query, self.properties['user'])
        #self.database.close()
        return check_password_hash(pwd_hash, db_pwd)

    def check_username_available(self):
        query = "SELECT COUNT(*) FROM users WHERE UserName=\"{}\"".format(self.properties['user'])

        out = self.database.exec(query) 
        #self.database.close()
        return out[0][0] == 0 or out == None

    def get_current_id(self):
        query = "SELECT driver_id FROM driver WHERE email=\"{}\" AND user=\"{}\""
        query = query.format(self.properties['email'], self.properties['user'])

        try:
            d_id = self.database.exec(query)
            #self.database.close()
            if not d_id:
                return None

            return d_id
        except Exception as e:
            raise Exception(e)

    def update_info(self, data: dict):
        """ Updates user info using current state of user 
            data expects a dictionary in the following format:
                each key is a named attribute of driver, and is followed by a key that is not None"""
     
        
        query = "UPDATE driver SET "

    # Generate list of items to update in query
        q_list = []
        for key in data.keys():
            q_list.append("{} = %s".format(key))

        username = self.properties['user']
    # Add items to update in query and add in WHERE to find correct user
        query += ", ".join(q_list) + " WHERE user=\"{}\"".format(username)

        try:
            self.database.exec(query, args=tuple(data.values()))
            #self.database.close()

        except Exception as e:
            raise Exception(e)

    def get_users(self):
        main_query = "SELECT first_name, mid_name, last_name, user, date_join, driver_id FROM driver where active = 1"
        try:
            out = self.database.exec(main_query)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        final_list = []

        for driver in out:
            sponsors = 'SELECT sponsor_id, points FROM driver_bridge WHERE driver_id = %s and apply = 0'
            val = (driver[5], )
            try:
                sponsor = self.database.exec(sponsors, val)
                #self.database.close()
            except Exception as e:
                raise Exception(e)
            
            sponsor_dict = {}
            for s in sponsor:
                sponsor_id = '{}'.format(s[0])
                sponsor_dict[sponsor_id] = s[1]

            driver = list(driver)
            driver[5] = sponsor_dict
            final_list.append(driver)

        return final_list

    def view_sponsors(self):
        query = 'SELECT sponsor_id, points FROM driver_bridge WHERE driver_id = %s AND apply = 0'
        val = (self.properties['id'], )
        try:
            username = self.database.exec(query, val)
            #self.database.close()

        except Exception as e:
                raise Exception(e)

        spon_list = []
        for user in username:
            spon_list.append(user)

        return spon_list
    
    # returns user data as a 2D array in the following formart
    # [0][0] = first name
    # [0][1] = middle name
    # [0][2] = last name
    # [0][3] = username
    # [0][4] = id number
    # [0][5] = sponsor id number
    # [0][6] = points
    # [0][7] = addresss
    # [0][8] = phone
    # [0][9] = email
    # [0][10] = image which should be null
    # [0][11] = date_join
    def get_user_data(self):
        query = 'SELECT first_name, mid_name, last_name, user, driver_id, sponsor_id, points, address, phone, email, image, date_join FROM driver WHERE user = %s'
        val = (self.properties['user'], )

        try:
            data = self.database.exec(query, val)
            #self.database.close()
            return data

        except Exception as e:
            raise Exception(e)

    def add_to_users(self):
        query = 'INSERT INTO users (Username, {}, last_in) VALUES (\'{}\', {}, CURRENT_TIMESTAMP())'
        query = query.format("Driver_ID", self.properties['user'], self.properties['id'])
        self.database.exec(query)
        #self.database.close()

    def getSponsorView(self):
        return self.properties['selectedSponsor']

    def setSponsorView(self, view):
        self.properties['selectedSponsor'] = view

    def getUsername(self):
        return self.properties['user']
    
    def getRole(self):
        return self.properties['role']

    def getPoints(self, spid):
        return self.properties['sponsors'].get(str(spid))
    
    def getID(self):
        return self.properties['id']

    #def isActive(self):

    def is_suspended(self):
        
        sql = 'SELECT user FROM suspend WHERE user = %s'
        val = (self.properties['user'], )

        try:
            #this will remove suspended driver's whos suspensions are over
            self.database.exec('DELETE from suspend WHERE date_return <= NOW()')
            suspended_user = self.database.exec(sql, val)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        if suspended_user == None:
            return False
        else:
            return True


    def populate(self, username: str):
        #Connection()
        query = 'SELECT first_name, mid_name, last_name, user, driver_id, address, phone, email, image, date_join FROM driver WHERE user = %s'
        vals = (username, )

        try:
            data = self.database.exec(query, vals)
            #self.database.close()

        except Exception as e:
            raise Exception(e)

        if data:
            self.properties['fname'] = data[0][0]
            self.properties['mname'] = data[0][1]
            self.properties['lname'] = data[0][2]
            self.properties['user'] = data[0][3]
            self.properties['id'] = data[0][4]
            self.properties['address'] = data[0][5]
            self.properties['phone'] = data[0][6]
            self.properties['email'] = data[0][7]
            self.properties['pwd'] = 'NULL'
            self.properties['image'] = data[0][8]
            self.properties['date_join'] = data[0][9]
            spon_list = self.view_sponsors()
            if not spon_list:
                sponsorid = None
                points = None
            else:
                sponsorid = spon_list[0][0]
                points = spon_list[0][1]

            if sponsorid:
                self.properties['selectedSponsor'] = [sponsorid, points]
            else:
                self.properties['selectedSponsor'] = None

            query = 'SELECT sponsor_id, points FROM driver_bridge WHERE driver_id = %s AND apply = 0'
            vals = (self.properties['id'], )

            try:
                data = self.database.exec(query, vals)
                #self.database.close()
            except Exception as e:
                raise Exception(e)

            for d in data:
                sponsor_id = '{}'.format(d[0])
                self.properties['sponsors'][sponsor_id] = d[1] 

            if self.properties['selectedSponsor'] is not None:
                id = next(iter(self.properties['sponsors']))
                points = self.properties['sponsors'].get(id)
                self.properties['selectedSponsor'] = [id, points]
                


    def apply_to_sponsor(self, sponsor_id):
        query = 'INSERT INTO driver_bridge VALUES (%s, %s, %s, %s)'
        vals = (self.properties['id'], sponsor_id, 0, 1)

        try:
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    #gets a list of current users that this user has a messsage from
    def get_inbox_list(self):
        #select all message that have not yet been read that involve this user
        message_query = 'SELECT * FROM messages WHERE (target = %s AND seent = 0) OR (sender = %s AND seens = 0) '
        vals = (self.properties['user'], self.properties['user'])

        try:
            #do some awesome database magic
            data = self.database.exec(message_query, vals)
        except Exception as e:
            raise Exception(e)

        user_list = []
        #if there is any data from the database
        if data:
            #loop through every message it returns
            for d in data:
                #if the TARGET is not already in the list AND it is not this user, add to the list
                if (d[0] not in user_list) and (d[0] != self.properties['user']):
                    user_list.append(d[0])
                #if the SENDER is not already in the list AND it is not this user, add to the list
                elif (d[1] not in user_list) and (d[1] != self.properties['user']):                       
                    user_list.append(d[1])

        return user_list
    #mark messages as aseen
    def messages_are_seen(self, user):
        #flag in case the user wants to mark all as seen
        if user == "MARK_ALL":
            query = 'UPDATE messages SET seens = 1 WHERE sender = %s'
            query2 = 'UPDATE messages SET seent = 1 WHERE target = %s'
            val = (self.properties['user'], )
            try:
                self.database.exec(query, val)
                self.database.exec(query2, val)
                #self.database.close()
            except Exception as e:
                raise Exception(e)
        else:
            #set the flags where the sender and target (that is this user) has seen the conversation
            query = 'UPDATE messages SET seent = 1 WHERE (target = %s AND sender = %s)'
            query2 = 'UPDATE messages SET seens = 1 WHERE (target = %s AND sender = %s)'
            val1 = (self.properties['user'], user)
            val2 = (user, self.properties['user'])
            try:
                self.database.exec(query, val1)
                self.database.exec(query2, val2)
                #self.database.close()
            except Exception as e:
                raise Exception(e)

    #get info of the other user in the conversation
    def get_msg_info(self, user):
        sql = 'SELECT Driver_ID, Sponsor_ID, Admin_ID FROM users WHERE UserName = %s'
        val = (user, )
        id = self.database.exec(sql, val)
        if id[0][0] != None:
            role =  'driver'
        elif id[0][1] != None:
            role =  'sponsor'
        else:
            role = 'admin'
        
        if role == 'driver' or role == 'admin':
            query = 'SELECT first_name, last_name, active FROM ' + role + ' WHERE user = %s'
        else:
            query = 'SELECT sponsor.title, sponsor_logins.active FROM sponsor join sponsor_logins using(sponsor_id) WHERE sponsor_logins.username = %s'
        val = (user, )
        
        try:
            data = self.database.exec(query, val)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

        data_list = list(data[0])
        data_list.insert(0, role)
        return data_list

    # return a list of lists with each list being a new message with the sender, msg, and timestamp being in each list
    #the first list will contain info about the other user in the convo
    def view_messages(self):
        message_query = 'SELECT * FROM messages WHERE target = %s OR sender = %s ORDER BY time DESC'
        vals = (self.properties['user'], self.properties['user'])

        try:
            data = self.database.exec(message_query, vals)
        except Exception as e:
            raise Exception(e)

        message_dict = {}

        if data:
            #for each message this user has
            for d in data:
                #the list is currently the keys of our message dictionary
                user_list = list(message_dict.keys())
                #if the target is not in the list and is not the user
                if (d[0] not in user_list) and (d[0] != self.properties['user']):

                    #make a new key in the dictionary 
                    message_dict[d[0]] = []

                    #get info about user from database
                    info = self.get_msg_info(d[0])

                    #if user is inactive add disabled tag to their last name and remove the tag from the list
                    if info[len(info) - 1] == 0:
                        info[len(info) - 2] += '(Disabled)'
                    info.pop(len(info) - 1)

                    #add their info to the dictionary
                    message_dict[d[0]].append(info)

                    #flag for appending will user later
                    user = 0

                #if the sender is not in the list and is not the user
                elif (d[1] not in user_list) and (d[1] != self.properties['user']):

                    #make a new key in the dictionary 
                    message_dict[d[1]] = []

                    #get info about user from database
                    info = self.get_msg_info(d[1])

                    #if user is inactive add disabled tag to their last name and remove the tag from the list
                    if info[len(info) - 1] == 0:
                        info[len(info) - 2] += '(Disabled)'
                    info.pop(len(info) - 1)

                    #add their info to the dictionary
                    message_dict[d[1]].append(info)

                    #flag for appending will user later
                    user = 1
                #if the user is us so we can talk to ourselves :)
                elif(d[0] == self.properties['user'] and d[1] == self.properties['user'] and d[0] not in user_list):
                    message_dict[d[0]] = []
                    info = self.get_msg_info(d[0])
                    if info[len(info) - 1] == 0:
                        info[len(info) - 2] += '(Disabled)'
                    info.pop(len(info) - 1)
                    message_dict[d[0]].append(info)
                    user = 0
                else:
                    if d[0] != self.properties['user']:
                        user = 0
                    else:
                        user = 1
                #add the message to the dictionary, insert into the first spot (most recent message) with d[user] being their name
                #d[1] being the sender in the convo, d[2] the message, and d[3] the timestamp
                message_dict[d[user]].insert(1, (d[1], d[2], d[3]))
        
        return message_dict

    #send a message to another user
    #the target is the username of the user you want to send a message to
    #the message is what you're getting them for dinner
    #....lol jk
    def send_message(self, target, message):
        time = 'SET time_zone = \'{}\''.format("America/New_York")
        query = 'INSERT INTO messages VALUES (%s, %s, %s, NOW(), 0, 1)'
        vals = (target, self.properties['user'], message)

        try:
            self.database.exec(time)
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    #send user message of order if their notis are on
    def send_order_info(self, msg):
        query = 'select notification.user, notification.orders from notification inner join driver on notification.user = driver.user where driver.driver_id = {}'.format(self.properties['driver_id'])
        data = self.database.exec(query)
        username = data[0][0]
        orders_noti = data[0][1]
        if orders_noti == 1:
            system = Admin()
            system.populate('System')
            system.send_message(self.populate['user'], msg)

    #send issue of the order if their notis are on
    def send_issue_info(self, msg):
        query = 'select notification.user, notification.issue from notification inner join driver on notification.user = driver.user where driver.driver_id = {}'.format(self.properties['driver_id'])
        data = self.database.exec(query)
        username = data[0][0]
        issue_noti = data[0][1]
        if issue_noti == 1:
            system = Admin()
            system.populate('System')
            system.send_message(self.populate['user'], msg)

    #update the drivers notification settings
    #pass in dictionary where keys are 'points', 'orders', 'issue' and value is 1 if they want noti or 0 if not
    def update_noti(self, notis: dict):
        #create update string
        query = 'UPDATE notification SET '
        q_list = []
        #set for each key
        for key in notis.keys():
            q_list.append("{} = {}".format(key, notis[key]))

        #join each part of q_list and add where clause
        username = self.properties['user']
        query += ", ".join(q_list) + " WHERE user=\"{}\"".format(username)

        try:
            self.database.exec(query)
        except Exception as e:
            raise Exception(e)

    #get notification settings for user
    #returns a dict with keys 'points', 'orders', 'issue' and vals 1 if true, 0 if false
    def get_notifications(self):
        query = 'SELECT * from notification WHERE user = \"{}\"'.format(self.properties['user'])
        try:
            data = self.database.exec(query)
        except Exception as e:
            raise Exception(e)
        noti_dict = {}
        noti_dict['points'] = data[0][1]
        noti_dict['orders'] = data[0][2]
        noti_dict['issue'] = data[0][3]

        return noti_dict


    
    def upload_image(self, tempf):
        with open(tempf, 'rb') as file:
            image = file.read()

        sql = 'UPDATE driver SET image = %s WHERE user = %s'
        vals = (image, self.properties['user'])

        try:
            self.database.exec(sql, vals)
            #self.database.close()
            self.properties['image'] = image
        except Exception as e:
            raise Exception(e)

    def download_image(self, tempf):
        with open(tempf, 'wb') as file:
            file.write(self.properties['image'])

        return file

    def change_password(self, new_pwd):
        query = 'UPDATE driver SET pwd = %s WHERE user = %s'
        vals = (new_pwd, self.properties['user'])

        try:
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def delete(self):
        """ Deletes a driver from the users table and from the driver table """

        query = "UPDATE driver SET active = 0 WHERE driver_id=%s"
        vals = (self.properties['id'], )
        try:
            self.database.exec(user_query, user_vals)
            self.database.exec(query, vals)
            #self.database.close()
        except Exception as e:
            raise Exception(e)

    def __del__(self):
        global pool1
        self.database.close()
        ##print(pool1.size())
        


