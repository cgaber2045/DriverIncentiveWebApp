import mysql.connector
from datetime import datetime


#Grab Connector
database = mysql.connector.connect(
    host = 'cpsc4910.crxd6v3fbudk.us-east-1.rds.amazonaws.com',
    user = 'admin',
    password = 'cpsc4910',
    database = 'website'
)


#See if we connected
print("Connected to mySQL")

cursor = database.cursor()

print("Enter your UserName")
Name = input()

#Grab info
cursor.execute("SELECT EXISTS(SELECT * FROM users WHERE UserName='"+Name+"')")


myinfo = cursor.fetchall()
print(myinfo[0][0])

if(myinfo[0][0]):
    print("You are in the System!")
    cursor.execute("SELECT EXISTS( SELECT UserName, last_in FROM users WHERE last_in >(NOW() - INTERVAL 1 DAY) AND UserName = '"+Name+"');")
    last_info = cursor.fetchall()
    if(last_info[0][0]):
        print("You have logged in in the past 24 hours, you may continue!")
        cursor.execute("SELECT driver_id FROM users WHERE UserName = '"+Name+"'")
        fetched = cursor.fetchall()
        ID = str(fetched[0][0])
        print(ID) 

        print("Hey look at all this info I have on you! Creepy ya?")
        cursor.execute("SELECT * FROM driver WHERE driver_id ="+ID)
        last_info = cursor.fetchall()
        print(last_info)
    else:
        print("It has been 24 since you last logged in, you need to log in again")
      
else:
    print("You need to sign up.")




#close cursor
cursor.close()
#close connection
database.close()

