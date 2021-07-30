from .context import lcsscaseapi
from lcsscaseapi.types import CaseMeta

def test_eq():
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

def test_neq():
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
        case_id = "blah",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_id = "X44DV3",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed"
    )

    assert obj1 != obj2

def test_from_dict():
    # intentionally out of the usual order
    case_info = {
        "doc_type": "OPINIONS",
        "docket_number": "13181",
        "outcome": "Judgment Affirmed",
        "case_id": "X44DV3",
        "case_name": "Barker v. United States",
        "title": "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        "doc_title": "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        "doc_id": "X44DV3"
    }
    cm = CaseMeta.from_dict(**case_info)
    expected = CaseMeta(
         case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_id = "X44DV3",
        doc_type = "OPINIONS",
        docket_number = "13181",
        outcome = "Judgment Affirmed"
    )
    print(str(cm))
    print(str(expected))
    assert str(cm) == str(expected)