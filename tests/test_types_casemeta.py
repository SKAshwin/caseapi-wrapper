from .context import lcsscaseapi
from lcsscaseapi.types import CaseMeta
import datetime

def test_eq():
    obj1 = CaseMeta(
         case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_id = "X44DV3",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed",
        date = datetime.date(1952, 10, 12)
    )

    obj2 = CaseMeta(
         case_id = "blah",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_id = "X44DV3",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed"
    )

    obj2.case_id = "X44DV3"
    obj2.date = datetime.date(1952, 10, 12)

    assert obj1 == obj2

def test_eq_order():
    # checking that equality is not sensitive to the ordering of the variables

    obj1 = CaseMeta(
         case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_id = "X44DV3",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed"
    )

    obj2 = CaseMeta(
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_id = "X44DV3",
        doc_type = "OPINIONS",
        docket_number = "13181",
        case_id = "blah",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        outcome = "Judgment Affirmed"
    )

    obj2.case_id = "X44DV3"

    assert obj1 == obj2

def test_eq_tag_order():
    # checking that equality is not sensitive to the ordering of the tags in the array

    obj1 = CaseMeta(
        case_id = "X44DV3",
        tags = ["HELLO", "WORLD"]
    )

    obj2 = CaseMeta(
        case_id = "blah",
        tags = ["WORLD", "HELLO"]
    )

    obj2.case_id = "X44DV3"

    assert obj1 == obj2
    
    obj2.tags = ["WORLD", "HELLO"]

    assert obj1 == obj2

def test_neq():
    obj1 = CaseMeta(
        case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_id = "X44DV3",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed",
        date = datetime.date(1968, 12, 12)
    )

    obj2 = CaseMeta(
        case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_id = "X44DV3",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed",
        date = datetime.date(1965, 12, 10)
    )

    assert obj1 != obj2

def test_from_json_dict():
    # intentionally out of the usual order
    case_info = {
        "doc_type": "OPINIONS",
        "docket_number": "13181",
        "outcome": "Judgment Affirmed",
        "case_id": "X44DV3",
        "case_name": "Barker v. United States",
        "title": "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        "doc_title": "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        "doc_id": "X44DV3",
        "date": "1965-12-10"
    }
    cm = CaseMeta.from_json_dict(case_info)
    expected = CaseMeta(
         case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_id = "X44DV3",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed",
        date = datetime.date(1965, 12, 10)
    )
    assert cm == expected

def test_from_json_dict_irrelevant_fields():
    # tests that irrelevant fields are ignored when supplied in a dictionary to from_json_dict

     # intentionally out of the usual order
    case_info = {
        "doc_type": "OPINIONS",
        "docket_number": "13181",
        "outcome": "Judgment Affirmed",
        "case_id": "X44DV3",
        "case_name": "Barker v. United States",
        "title": "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        "doc_title": "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        "doc_id": "X44DV3",
        "something_else": "shouldn't be here",
        "date": "1965-12-10"
    }
    cm = CaseMeta.from_json_dict(case_info)
    expected = CaseMeta(
        case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_id = "X44DV3",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed",
        date = datetime.date(1965, 12, 10)
    )
    assert cm == expected
    assert not hasattr(cm, 'something_else')

def test_from_json_dict_missing_fields():
    # tests that leaving some fields out doesn't trigger an error

    case_info = {
        "doc_type": "OPINIONS",
        "docket_number": "13181",
        "outcome": "Judgment Affirmed",
        "case_id": "X44DV3",
        "case_name": "Barker v. United States",
        "doc_title": "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        "something_else": "shouldn't be here"
    }
    cm = CaseMeta.from_json_dict(case_info)
    expected = CaseMeta(
        case_id = "X44DV3",
        case_name = "Barker v. United States",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed"
    )
    assert cm == expected

def test_repr():
    cm = CaseMeta(
        case_id = "X44DV3",
        case_name = "Barker v. United States",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed"
    )

    assert cm.__repr__() == "CaseMeta Object: " + str(cm)