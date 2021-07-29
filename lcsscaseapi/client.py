from lcsscaseapi import constants
import requests

class LCSSClient:
    def __init__(self, username, password):
        response = requests.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, 
                     data = {'username': username, 'password': password})
        if response.status_code == 200:
            self._token = response.json()["token"]
        elif response.status_code == 400:
            if "Unable to log in with provided credentials" in str(response.content):
                raise Exception("Incorrect log-in credentials")
            elif "may not be blank" in str(response.content):
                raise Exception("Incorrect log-in credentials: empty username or password")
            else:
                raise Exception("Unknown bad request, see response from server: " + str(response.content))
        else:
            raise Exception("Unknown error, see response from server: " + str(response.content))
        
        