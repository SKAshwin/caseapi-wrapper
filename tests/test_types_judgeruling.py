from lcsscaseapi.types import Judge, JudgeRuling
import pytest


def test_jr_constructor():
    # test that missing fields set to None
    # test that judge_id and case_id fields are mandatory

    jr = JudgeRuling(case_id="X1111", judge_id=35)

    assert jr.vote == None
    assert jr.author == None
    assert jr.id == None

    jr = JudgeRuling(case_id="X1111", judge_id=35, vote = JudgeRuling.DISSENTING, author=False, id = 10)

    assert jr.case == "X1111"
    assert jr.judge == 35
    assert jr.vote == JudgeRuling.DISSENTING
    assert jr.author == False
    assert jr.id == 10

    with pytest.raises(Exception):
        jr = JudgeRuling()
    with pytest.raises(Exception):
        jr = JudgeRuling(case_id="X1111")
    with pytest.raises(Exception):
        jr = JudgeRuling(judge_id=22)

def test_jr_constructor_invalid_vote():
    # votes can only be concurring or dissenting
    with pytest.raises(Exception, match="vote must be Concurring, Dissenting or None"):
        JudgeRuling(case_id="W1212", judge_id=22, vote="Hello")

def test_jr_vote_setter():
    # again, votes can only be set to concurring or dissenting
    jr = JudgeRuling(case_id="W1212", judge_id=22, vote = JudgeRuling.CONCURRING)
    jr.vote = None
    assert jr.vote == None
    
    jr.vote = JudgeRuling.DISSENTING
    assert jr.vote == JudgeRuling.DISSENTING
    
    with pytest.raises(Exception, match="vote must be Concurring, Dissenting or None"):
        jr.vote = "Agree"

def test_jr_eq():
    jr1 = JudgeRuling(case_id="W1212", judge_id=22, vote = JudgeRuling.CONCURRING)
    jr2 = JudgeRuling(case_id="W1212", judge_id=22, vote = JudgeRuling.CONCURRING, author = True)

    assert jr1 != jr2
    jr1.author = True
    assert jr1 == jr2

def test_jr_str():
    jr = JudgeRuling(case_id="V1234", judge_id=8, vote = JudgeRuling.CONCURRING, author = False)
    assert str(jr) == r'{"author": false, "case": "V1234", "id": null, "judge": 8, "vote": "Concurring"}'

def test_jr_repr():
    jr = JudgeRuling(case_id="V1234", judge_id=22, vote = None, author = True)
    assert jr.__repr__() == "JudgeRuling Object: " + str(jr)

def test_jr_to_json_dict():
    jr = JudgeRuling(case_id="X3462", judge_id=8, id=12, author = False)
    json_dict = {
        "case": "X3462",
        "judge": 8,
        "id": 12,
        "author": False,
        "vote": None
    }
    assert jr.to_json_dict() == json_dict

def test_jr_from_json_dict():
    json_dict = {
        "case": "T5673",
        "judge": 103,
        "id": None,
        "author": True,
        "vote": JudgeRuling.CONCURRING
    }
    jr = JudgeRuling(case_id = "T5673", judge_id = 103, author = True, vote = JudgeRuling.CONCURRING)

    assert JudgeRuling.from_json_dict(json_dict) == jr

def test_jr_from_json_dict_missing_fields():
    # check that trying to create a jr with no `case` or `judge` field fails
    # missing any other field should not pose an issue

    json_dict = {
        "case": "T5673",
        "judge": 103,
        "id": None,
    }
    jr = JudgeRuling(case_id = "T5673", judge_id = 103)
    assert JudgeRuling.from_json_dict(json_dict) == jr

    json_dict = {
        "case": "T5673",
        "id": 10,
    }
    with pytest.raises(Exception, match = "Cannot have JudgeRuling without 'case' field or without 'judge' field"):
        JudgeRuling.from_json_dict(json_dict)

    json_dict = {
        "judge": 11,
        "vote": JudgeRuling.DISSENTING,
        "id": 10
    }
    with pytest.raises(Exception, match = "Cannot have JudgeRuling without 'case' field or without 'judge' field"):
        JudgeRuling.from_json_dict(json_dict)    

def test_jr_from_json_dict_incorrect_vote():
    json_dict = {
        "case": "T5673",
        "judge": 103,
        "id": 5,
        "vote": "hello"
    }
    with pytest.raises(Exception, match = "vote must be Concurring, Dissenting or None"):
        JudgeRuling.from_json_dict(json_dict)  

def test_jr_from_json_dict_extra_fields():
    json_dict = {
        "case": "T5673",
        "judge": 103,
        "id": None,
        "irrelevant": True
    }
    jr = JudgeRuling(case_id = "T5673", judge_id = 103)
    assert JudgeRuling.from_json_dict(json_dict) == jr