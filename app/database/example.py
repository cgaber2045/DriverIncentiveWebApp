import mysql.connector

#establish connection
database = mysql.connector.connect(
    host = 'cpsc4910.crxd6v3fbudk.us-east-1.rds.amazonaws.com',
    user = 'admin',
    password = 'cpsc4910',
    database = 'website'
)

#shows we have successfully connected to the database
print("Connected to database")

#cursor
cursor = database.cursor()

#execute query
cursor.execute("INSERT INTO driver VALUES ('Evan', \
                                            NULL, \
                                            'Hastings', \
                                            2, \
                                            1, \
                                            2, \
                                            '123 clemson boulevard', \
                                            5555555555, \
                                            'eh@email.com', \
                                            NULL,  \
                                            NULL, \
                                            NOW(), \
                                            NULL)")


#  .commit()  commits the execute to the database (saves it)
#  without .commit() you can still view what it would look like and view as if it was in the database
#  however it will not save to the database
database.commit() 

#execute query
cursor.execute("SELECT * FROM driver")

#get data from database stored in map
rows = cursor.fetchall()

#loop through all of the rows that are returned and display them (will be a tuple)
for r in rows:
        print(r)

#close cursor
cursor.close()
#close connection
database.close()


# for good practice go do the tutorials in this website https://www.w3schools.com/python/python_mysql_getstarted.asp