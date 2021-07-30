from .context import lcsscaseapi
from lcsscaseapi.client import LCSSClient
from lcsscaseapi.types import CaseMeta
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

def test_search_cases(requests_mock):
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    returnjson = [
        {
            "case_id": "X44DT7",
            "case_name": "Courtney v. Custer County Bank",
            "title": "Courtney v. Custer County Bank, 198 F.2d 828 (9th Cir. 1952), Court Opinion",
            "doc_title": "Courtney v. Custer County Bank, 198 F.2d 828 (9th Cir. 1952), Court Opinion",
            "doc_id": "X44DT7",
            "doc_type": "OPINIONS",
            "docket_number": "13085",
            "outcome": "Judgment Affirmed"
        },
        {
            "case_id": "X44CJ7",
            "case_name": "Jefferson v. Stockholders Publishing Co.",
            "title": "Jefferson v. Stockholders Publishing Co., 194 F.2d 281 (9th Cir. 1952), Court Opinion",
            "doc_title": "Jefferson v. Stockholders Publishing Co., 194 F.2d 281 (9th Cir. 1952), Court Opinion",
            "doc_id": "X44CJ7",
            "doc_type": "OPINIONS",
            "docket_number": "12879",
            "outcome": "Judgment Reversed"
        }
    ]
    returncasemeta = [CaseMeta.from_dict(**x) for x in returnjson]
    requests_mock.get('https://' + constants.DOMAIN_NAME + constants.CIRCUIT_CASE_ENDPOINT, json = returnjson, status_code=200)
    cases = client.search_cases(title="9th Cir.")

    assert cases == returncasemeta