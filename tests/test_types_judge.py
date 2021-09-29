from lcsscaseapi.types import Judge
import pytest

def test_judge_constructor():
    judge = Judge(id=1, gender = Judge.MALE)
    
    assert judge.id == 1
    assert judge.judge_gender == Judge.MALE
    assert judge.judge_name == None # unset fields should be set to None
    assert judge.judge_orig_name == None

    judge = Judge() # unset fields should be set to None
    assert judge.id == None
    assert judge.judge_gender == None
    assert judge.judge_name == None 
    assert judge.judge_orig_name == None

def test_judge_constructor_invalid_gender():
    with pytest.raises(Exception) as e1: # Empty string isn't allowed - has to be none!
        Judge(gender = "")
    assert str(e1.value) == "Gender must be Male, Female or None"
    
    with pytest.raises(Exception) as e2:
        Judge(gender = "Something")
    assert str(e2.value) == "Gender must be Male, Female or None"
    

def test_judge_gender_setter():
    judge = Judge()
    judge.judge_gender = Judge.FEMALE
    assert judge.judge_gender == Judge.FEMALE
    judge.judge_gender = None
    assert judge.judge_gender == None

    with pytest.raises(Exception) as e:
        judge.judge_gender = "Smale"  
    assert str(e.value) == "Gender must be Male, Female or None"

def test_judge_eq():
    judge1 = Judge(name="Hello World", orig_name="Hello", gender=Judge.MALE)
    judge2 =Judge(name="Hello World", orig_name="Hello", gender=Judge.FEMALE)
    assert judge2 != judge1
    
    judge2.judge_gender = Judge.MALE
    assert judge2 == judge1

def test_judge_hash():
    judge1 = Judge(name="Hello World", orig_name="Hello", gender=Judge.MALE)
    judge2 =Judge(name="Hello World", orig_name="Hello", gender=Judge.FEMALE)
    assert judge2.__hash__() != judge1.__hash__()
    
    s = set()
    s.add(judge1)
    assert judge2 not in s

    judge2.judge_gender = Judge.MALE
    assert judge2.__hash__() == judge1.__hash__()
    assert judge2 in s

def test_judge_str():
    judge = Judge(name="Hello World", gender=Judge.MALE)
    assert str(judge) == r'{"id": null, "judge_gender": "Male", "judge_name": "Hello World", "judge_orig_name": null}'

def test_judge_to_json_dict():
    judge = Judge(name="Hello World", id=2)

    # empty fields should be Nones in the dictionary, not missing entries
    judge_dict = {
        "judge_name": "Hello World",
        "id": 2,
        "judge_gender": None,
        "judge_orig_name": None
    }
    assert judge.to_json_dict() == judge_dict

    judge = Judge()
    judge_dict = {
        "judge_name": None,
        "id": None,
        "judge_gender": None,
        "judge_orig_name": None
    }
    assert judge.to_json_dict() == judge_dict

def test_judge_from_json_dict():
    judge_dict = {
        "judge_name": "Byelection",
        "id": 10,
        "judge_gender": None,
        "judge_orig_name": "Hi"
    }
    judge = Judge(name = "Byelection", orig_name="Hi", id = 10)
    assert judge == Judge.from_json_dict(judge_dict)

def test_judge_from_json_dict_missing_fields():
    # missing fields should be correctly read as None
    judge_dict = {
        "judge_name": "Byelection",
        "id": 10,
        "judge_gender": None
    }
    judge = Judge(name = "Byelection", orig_name=None, id = 10)
    assert judge == Judge.from_json_dict(judge_dict)

def test_judge_from_json_dict_irrelevant_fields():
    # irrelevant fields should be ignored
    judge_dict = {
        "judge_name": "Byelection",
        "judge_gender": Judge.FEMALE,
        "judge_orig_name": "Hi",
        "something":"okay"
    }
    judge = Judge(name = "Byelection", orig_name="Hi", gender= Judge.FEMALE)
    assert judge == Judge.from_json_dict(judge_dict)

def test_judge_from_json_dict_invalid_gender():
    # gender validation should still proceed correctly
    judge_dict = {
        "judge_name": "Byelection",
        "id": 10,
        "judge_gender": "Hello",
        "judge_orig_name": "Hi"
    }
    with pytest.raises(Exception) as e:
        Judge.from_json_dict(judge_dict)
    assert str(e.value) == "Gender must be Male, Female or None"

def test_judge_repr():
    judge = Judge(name = "Byelection", orig_name="Hi", gender= Judge.FEMALE)

    assert judge.__repr__() == "Judge Object: " + str(judge)