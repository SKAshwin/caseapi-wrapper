from .context import lcsscaseapi
from lcsscaseapi.client import LCSSClient
from lcsscaseapi.types import CaseMeta, USCircuitCaseMeta, USJudge
from lcsscaseapi import constants
import pytest
import datetime

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
    returncasemeta = [CaseMeta.from_json_dict(x) for x in returnjson]
    requests_mock.get('https://' + constants.DOMAIN_NAME + constants.CASE_ENDPOINT, json = returnjson, status_code=200)
    cases = client.search_cases(title="9th Cir.")

    assert cases == returncasemeta
    assert requests_mock.request_history[-1].qs == {"title":["9th cir."]} # notice: search terms are case insensitive

def test_search_cases_multiple_args(requests_mock):
    # test that multiple search arguments load correctly
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
    returncasemeta = [CaseMeta.from_json_dict(x) for x in returnjson]
    requests_mock.get('https://' + constants.DOMAIN_NAME + constants.CASE_ENDPOINT, json = returnjson, status_code=200)
    cases = client.search_cases(title="9th Cir.", doc_id="X44")

    assert cases == returncasemeta
    assert requests_mock.request_history[-1].qs == {"title":["9th cir."], "doc_id":["x44"]} # notice: search terms are case insensitive

def test_search_cases_no_result(requests_mock):
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    requests_mock.get('https://' + constants.DOMAIN_NAME + constants.CASE_ENDPOINT, json = [], status_code=200)
    cases = client.search_cases(title="9th Cir.", some_made_up_field="123") # searching by a field that doesn't exist should not trigger an error

    assert len(cases) == 0
    assert requests_mock.request_history[-1].qs == {"title":["9th cir."], "some_made_up_field":["123"]} # notice: search terms are case insensitive

def test_search_cases_error(requests_mock):
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    requests_mock.get('https://' + constants.DOMAIN_NAME + constants.CASE_ENDPOINT, status_code=500)
    with pytest.raises(Exception, match="Unknown error.*"):
        client.search_cases(title="9th Cir.", some_made_up_field="123")

def test_upload_us_cases(requests_mock):
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    new_cases = [USCircuitCaseMeta(case_id="X1111", date = datetime.date(1964, 10, 20)), USCircuitCaseMeta(case_id="X2222", tags = ["HELLO", "WORLD"])]
    new_cases_json = [
        {
            "case_id":"X1111",
            "date": "1964-10-20"
        },
        {
            "case_id":"X2222",
            "tags": ["HELLO", "WORLD"]
        }
    ]
    requests_mock.post("https://" + constants.DOMAIN_NAME + constants.CIRCUIT_CASE_ENDPOINT, json = new_cases_json, status_code = 201)
    cases = client.upload_us_cases(new_cases)

    assert cases == new_cases
    assert requests_mock.request_history[-1].headers["Authorization"] == "Token validtoken"
    assert [USCircuitCaseMeta.from_json_dict(case_json) for case_json in requests_mock.request_history[-1].json()] == new_cases
    assert requests_mock.request_history[-1].headers["Content-Type"] == "application/json"

def test_upload_us_cases_non_admin(requests_mock):
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    new_cases = [USCircuitCaseMeta(case_id="X1111"), USCircuitCaseMeta(case_id="X2222", tags = ["HELLO", "WORLD"])]
    requests_mock.post("https://" + constants.DOMAIN_NAME + constants.CIRCUIT_CASE_ENDPOINT, status_code = 403)
    with pytest.raises(Exception, match="Need admin credentials to upload new USCircuitCaseMeta:*"):
        client.upload_us_cases(new_cases)
    assert requests_mock.request_history[-1].headers["Authorization"] == "Token validtoken"

def test_upload_us_cases_bad_case(requests_mock):
    # server might return 400 if the case has tags that don't exist or a duplicate case ID etc
    # this should be handled gracefully
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    new_cases = [USCircuitCaseMeta(case_id="X1111"), USCircuitCaseMeta(case_id="X2222", tags = ["HELLO", "WORLD"])]
    requests_mock.post("https://" + constants.DOMAIN_NAME + constants.CIRCUIT_CASE_ENDPOINT, status_code = 400)
    with pytest.raises(Exception, match="Invalid USCircuitCaseMeta object, see:*"):
        client.upload_us_cases(new_cases)
    assert requests_mock.request_history[-1].headers["Authorization"] == "Token validtoken"

def test_upload_us_cases_unknown_error(requests_mock):
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    new_cases = [USCircuitCaseMeta(case_id="X1111"), USCircuitCaseMeta(case_id="X2222", tags = ["HELLO", "WORLD"])]
    requests_mock.post("https://" + constants.DOMAIN_NAME + constants.CIRCUIT_CASE_ENDPOINT, status_code = 500)
    with pytest.raises(Exception, match="Unknown error, see response from server:*"):
        client.upload_us_cases(new_cases)
    assert requests_mock.request_history[-1].headers["Authorization"] == "Token validtoken"

def test_upload_us_judges(requests_mock):
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    new_judges = [USJudge(name="Hello", gender= USJudge.MALE),USJudge(name="julio", gender= USJudge.FEMALE)]
    new_judges_JSON = [
        {
            "id": 1,
            "judge_name": "Hello",
            "judge_gender": USJudge.MALE
        },
        {
            "id": 2,
            "judge_name": "julio",
            "judge_gender": USJudge.FEMALE
        }
    ]
    requests_mock.post("https://" + constants.DOMAIN_NAME + constants.US_JUDGE_ENDPOINT, json = new_judges_JSON, status_code = 201)
    judges = client.upload_us_judges(new_judges) # the cases you get back will come with their numeric ID, which cannot be set in the upload


    assert [USJudge.from_json_dict(judge_json) for judge_json in requests_mock.request_history[-1].json()] == new_judges
    assert requests_mock.request_history[-1].headers["Authorization"] == "Token validtoken"
    assert requests_mock.request_history[-1].headers["Content-Type"] == "application/json"

    # note that the returned judges, unlike the created ones, have an ID field, so check for this
    new_judges[0].id = 1 
    new_judges[1].id = 2
    assert judges == new_judges

def test_upload_us_judges_non_admin(requests_mock):
    response_json = {
        "detail": "You do not have permission to perform this action."
    }

    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    new_judges = [USJudge(name="Hello", gender= USJudge.MALE),USJudge(name="julio", gender= USJudge.FEMALE)]
    requests_mock.post("https://" + constants.DOMAIN_NAME + constants.US_JUDGE_ENDPOINT, json = response_json, status_code = 403)
    with pytest.raises(Exception, match = "Need admin credentials to upload new USJudge.*You do not have permission to perform this action.*"):
        client.upload_us_judges(new_judges)
    assert requests_mock.request_history[-1].headers["Authorization"] == "Token validtoken"
    assert requests_mock.request_history[-1].headers["Content-Type"] == "application/json"

def test_upload_us_judges_bad_judge(requests_mock):
    # at the moment not actually possible to upload a bad judge because sufficient validation is performed by the judge class already
    # may not hold into the future
    response_json = [{
        "some_field": "blah is not a valid choice for this field."
    },
    {}
    ]

    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    new_judges = [USJudge(name="Hello", party=USJudge.DEMOCRAT),USJudge(name="julio", gender= USJudge.FEMALE)]
    requests_mock.post("https://" + constants.DOMAIN_NAME + constants.US_JUDGE_ENDPOINT, json = response_json, status_code = 400)
    with pytest.raises(Exception, match = "Invalid USJudge object, see.*blah is not a valid choice for this field.*"):
        client.upload_us_judges(new_judges)
    assert requests_mock.request_history[-1].headers["Authorization"] == "Token validtoken"
    assert requests_mock.request_history[-1].headers["Content-Type"] == "application/json"

def test_upload_us_judges_unknown_error(requests_mock):
    response_json = {"whatever":"contents of error message"}
    requests_mock.post('https://' + constants.DOMAIN_NAME + constants.AUTH_ENDPOINT, json = {"token": "validtoken"})
    client = LCSSClient(username="testing", password="123")
    new_judges = [USJudge(name="Hello", party=USJudge.DEMOCRAT),USJudge(name="julio", gender= USJudge.FEMALE)]
    requests_mock.post("https://" + constants.DOMAIN_NAME + constants.US_JUDGE_ENDPOINT, json = response_json, status_code = 500)
    with pytest.raises(Exception, match = "Unknown error, see response from server.*contents of error message.*"):
        client.upload_us_judges(new_judges)
    assert requests_mock.request_history[-1].headers["Authorization"] == "Token validtoken"
    assert requests_mock.request_history[-1].headers["Content-Type"] == "application/json"