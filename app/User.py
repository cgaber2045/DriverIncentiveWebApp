# Legacy User Class
from app.database.db_functions import *

class User:
    def __init__(self):
        self.username = ""
        self.suspension = False
        self.role = "NULL"
        self.points = 0
        self.sandbox = "None"

    def populate(self, username):
        self.username = username
        self.suspension = is_driver_suspended(username)
        id, self.role = get_table_id(username)
        if (self.role == "driver"):
            self.points = 0
        else:
            self.points = 9999999
        self.sandbox = "None"

    def setSandbox(self, sandbox):
        self.sandbox = sandbox

    def getSandbox(self):
        return self.sandbox

    def getUsername(self):
        return self.username
        
    def getRole(self):
        return self.role 

    def getPoints(self):
        return self.points
    
    def suspendDriver(self):
        today = datetime.today()
        suspend_driver(username, today.year, today.month, today.day)
