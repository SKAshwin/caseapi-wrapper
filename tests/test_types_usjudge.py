from lcsscaseapi.types import USJudge, Judge
import pytest


def test_usjudge_constructor():
    uj = USJudge()
    for _, val in uj.__dict__.items():
        assert val == None # check that all values set to None, not empty string etc, if no fields initialized
    
    uj = USJudge(gender = USJudge.FEMALE, party = USJudge.DEMOCRAT, senior = False, name = "Hello")

    assert uj.id == None
    assert uj.judge_gender == Judge.FEMALE
    assert uj.party == USJudge.DEMOCRAT
    assert uj.judge_name == "Hello"
    assert uj.judge_orig_name == None
    assert uj.senior == False

def test_usjudge_constructor_invalid_gender():
    with pytest.raises(Exception) as e:
        USJudge(id = 3, gender = "mAlE")
    assert str(e.value) == "Gender must be Male, Female or None"

def test_usjudge_constructor_invalid_party():
    with pytest.raises(Exception) as e:
        USJudge(gender = USJudge.MALE, party = "Libertarian")
    assert str(e.value) == "Party must be Democrat, Republican or None"

def test_usjudge_eq_neq():
    uj1 = USJudge(name = "Bob", party = USJudge.DEMOCRAT)
    uj2 = USJudge(name = "Bob", party = USJudge.REPUBLICAN)
    assert uj1 != uj2

    uj2.party = USJudge.DEMOCRAT
    assert uj1 == uj2

def test_usjudge_from_json():
    uj_dict = {
        "id": 5,
        "party": USJudge.REPUBLICAN,
        "senior": True  # notice this is a bool not a string
    }
    uj = USJudge(id = 5, party = USJudge.REPUBLICAN, senior = True)
    assert uj == USJudge.from_json_dict(uj_dict)

    # try again with missing field - shouldn't cause any issues
    uj_dict = {
        "id": 5,
        "senior": True  # notice this is a bool not a string
    }
    uj = USJudge(id = 5, senior = True)
    assert uj == USJudge.from_json_dict(uj_dict)

def test_usjudge_from_json_extra_fields():
    # extra fields should be ignored
    uj_dict = {
        "id": 5,
        "party": USJudge.REPUBLICAN,
        "senior": True, 
        "unrelated": False
    }
    uj = USJudge(id = 5, party = USJudge.REPUBLICAN, senior = True)
    assert uj == USJudge.from_json_dict(uj_dict)

def test_usjudge_from_json_invalid_gender():
    uj_dict = {
        "id": 5,
        "party": USJudge.REPUBLICAN,
        "senior": True,
        "judge_gender": "somethingElse"
    }
    with pytest.raises(Exception) as e:
        USJudge.from_json_dict(uj_dict)

    assert str(e.value) == "Gender must be Male, Female or None"

def test_usjudge_from_json_invalid_party():
    uj_dict = {
        "id": 5,
        "party": True,
        "senior": True,
        "judge_gender": USJudge.MALE,
    }
    with pytest.raises(Exception) as e:
        USJudge.from_json_dict(uj_dict)

    assert str(e.value) == "Party must be Democrat, Republican or None"

def test_usjudge_to_json():
    uj_dict = {
        "id": None,
        "judge_gender": None,
        "judge_name": "Bob Wood",
        "judge_orig_name" : "Wood",
        "party": USJudge.DEMOCRAT,
        "senior": False
    }
    uj = USJudge(name = "Bob Wood", orig_name = "Wood", party = USJudge.DEMOCRAT, senior=False)

    assert uj.to_json_dict() == uj_dict

def test_usjudge_repr():
    uj = USJudge(name = "Bob Wood", orig_name = "Wood", party = USJudge.DEMOCRAT, senior=False)
    assert uj.__repr__() == r'USJudge Object: {"id": null, "judge_gender": null, "judge_name": "Bob Wood", "judge_orig_name": "Wood", "party": "' + USJudge.DEMOCRAT + r'", "senior": false}'

def test_usjudge_string():
    uj = USJudge(name = "Bob Wood", orig_name = "Wood", party = USJudge.DEMOCRAT, senior=False)
    assert str(uj) == '{"id": null, "judge_gender": null, "judge_name": "Bob Wood", "judge_orig_name": "Wood", "party": "' + USJudge.DEMOCRAT + r'", "senior": false}'
