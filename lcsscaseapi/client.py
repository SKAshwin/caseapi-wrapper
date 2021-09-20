from lcsscaseapi import constants
from lcsscaseapi.types import CaseMeta, USCircuitCaseMeta, USJudge
import requests
import json

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
        
    def get_cases(self, **kwargs):
        response = requests.get('https://' + constants.DOMAIN_NAME + constants.CASE_ENDPOINT, params=kwargs, 
                            headers={"Authorization":"Token " + self._token})
        if response.status_code == 200:
            cases_dict = response.json() # the json array of case objects will be converted to an array of dictionaries
            cases = [CaseMeta.from_json_dict(case_json) for case_json in cases_dict]
            return cases
        else:
            raise Exception("Unknown error, see response from server: " + str(response.content))
    
    def get_us_judges(self, **kwargs):
        pass

    def upload_us_cases(self, cases):
        return self._upload_generic_object(cases, constants.CIRCUIT_CASE_ENDPOINT, USCircuitCaseMeta)
        
    def upload_us_judges(self, judges):
        return self._upload_generic_object(judges, constants.US_JUDGE_ENDPOINT, USJudge)


    # For internal use only
    # a bunch of the upload-x objects are basically identical, so they each call this internal function
    def _upload_generic_object(self, objects, endpoint, class_object):
        json_data = [object.to_json_dict() for object in objects]
        response = requests.post('https://' + constants.DOMAIN_NAME + endpoint, 
                        headers={"Authorization":"Token " + self._token},
                        json = json_data)
        if response.status_code == 201:
            objects_dict = response.json() # the json array of case objects will be converted to an array of dictionaries
            objects_response = [class_object.from_json_dict(case_json) for case_json in objects_dict] # json response reutrns the cases just created
            return objects_response
        elif response.status_code == 403:
            raise Exception("Need admin credentials to upload new " + class_object.__name__ + ": " + str(response.content))
        elif response.status_code == 400:
            raise Exception("Invalid " + class_object.__name__  + " object, see: " + str(response.content))
        else:
            raise Exception("Unknown error, see response from server: " + str(response.content))
        