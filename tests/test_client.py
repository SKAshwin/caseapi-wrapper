from .context import lcsscaseapi
from lcsscaseapi.client import LCSSClient
from lcsscaseapi import constants
import pytest

def test_init_successful(requests_mock):
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "hi"})
    client = LCSSClient(username="testing", password="123")
    assert client._token == "hi"

def test_init_wrong_login(requests_mock):
    response_json = {
        "non_field_errors": [
            "Unable to log in with provided credentials."
        ]
    }
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = response_json, status_code = 400)
    with pytest.raises(Exception, match="Incorrect log-in credentials"):
        client = LCSSClient(username="testing", password="123")

def test_missing_login(requests_mock):
    response_json = {
        "username": [
            "This field may not be blank."
        ],
        "password": [
            "This field may not be blank."
        ]
    }
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = response_json, status_code = 400)
    with pytest.raises(Exception, match="Incorrect log-in credentials: empty username or password"):
        client = LCSSClient(username="testing", password="123")

def test_generic_badrequest_login(requests_mock):
    response_json = {"whatever":"contents of error message"}
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = response_json, status_code = 400)
    with pytest.raises(Exception, match="Unknown bad request.*contents of error message"):
        client = LCSSClient(username="testing", password="123")

def test_generic_error_login(requests_mock):
    response_json = {"whatever":"contents of error message"}
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = response_json, status_code = 500)
    with pytest.raises(Exception, match="Unknown error.*contents of error message"):
        client = LCSSClient(username="testing", password="123")