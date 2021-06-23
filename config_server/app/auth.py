from werkzeug.security import check_password_hash
import requests as r
import os

class AdminAuth():
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd

    def __enter__(self):
        self.url = os.getenv('API_URL')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        
    def check_credentials(self):
        data = {'username': self.user, 'password': self.pwd}
        response = r.post(self.url, json=data)

        try:
            ret = response.json()
            if ret['message'] == 'success':
                return ret['content']['token']
            else:
                return None
        except ValueError:
            print("Error loading JSON")
