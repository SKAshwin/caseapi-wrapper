import constants
import requests

class LCSSClient:
    def __init__(self, username, password):
        response = requests.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, 
                     data = {'username': username, 'password': password})
        self._token = response.json()["token"]