from lcsscaseapi.types import CaseMeta, USCircuitCaseMeta
import datetime
import pytest

def test_eq():
    obj1 = USCircuitCaseMeta(
        case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        circuit_name = USCircuitCaseMeta.FIFTH_CIRCUIT
    )

    obj2 = USCircuitCaseMeta(
        case_id = "blah",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        circuit_name = USCircuitCaseMeta.FIFTH_CIRCUIT
    )

    obj2.case_id = "X44DV3"

    assert obj1 == obj2

def test_eq_order():
    # check that ordering of the fields doesn't affect equality
    obj1 = USCircuitCaseMeta(
        case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        circuit_name = USCircuitCaseMeta.FIFTH_CIRCUIT
    )

    obj2 = USCircuitCaseMeta(
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        case_id = "blah",
        case_name = "Barker v. United States",
        circuit_name = USCircuitCaseMeta.FIFTH_CIRCUIT
    )

    obj2.case_id = "X44DV3"

    assert obj1 == obj2

def test_eq_tag_order():
    # check that ordering of the tags doesn't affect equality
    obj1 = USCircuitCaseMeta(
        case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        tags = ["WORLD", "HELLO"],
        circuit_name = USCircuitCaseMeta.SIXTH_CIRCUIT
    )

    obj2 = USCircuitCaseMeta(
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        case_id = "blah",
        case_name = "Barker v. United States",
        circuit_name = USCircuitCaseMeta.SIXTH_CIRCUIT,
        tags = ["HELLO", "WORLD"]
    )

    obj2.case_id = "X44DV3"

    assert obj1 == obj2

def test_neq():
    obj1 = USCircuitCaseMeta(
        case_id = "X44DV3",
        case_name = "Barker v. United States",
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        tags = ["WORLD", "HELLO"],
        circuit_name = USCircuitCaseMeta.SIXTH_CIRCUIT
    )

    obj2 = USCircuitCaseMeta(
        title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        case_id = "blah",
        case_name = "Barker v. United States",
        circuit_name = USCircuitCaseMeta.EIGHTH_CIRCUIT,
        tags = ["HELLO", "WORLD"]
    )

    obj2.case_id = "X44DV3"

    assert obj1 != obj2

def test_invalid_circuit_constructor():
    # check that supplying an invalid circuit name triggers an exception with the right message
    with pytest.raises(Exception) as e:
        obj1 = USCircuitCaseMeta(
            case_id = "X44DV3",
            case_name = "Barker v. United States",
            title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
            doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
            tags = ["WORLD", "HELLO"],
            circuit_name = "12th Circuit"
        )
    assert str(e.value) == "circuit_name is not a valid circuit name or None. Valid names must be one of the following (or a None): Federal Circuit, 1st Circuit, 2nd Circuit, 3rd Circuit, 4th Circuit, 5th Circuit, 6th Circuit, 7th Circuit, 8th Circuit, 9th Circuit, 10th Circuit, 11th Circuit, DC Circuit"

def test_circuit_setter():
    # check that the circuit_name setter only accepts certain valid options
    obj1 = USCircuitCaseMeta(
            case_id = "X44DV3",
            case_name = "Barker v. United States",
            title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
            doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
            tags = ["WORLD", "HELLO"]
        )

    obj1.circuit_name = USCircuitCaseMeta.TENTH_CIRCUIT

    assert obj1.circuit_name == USCircuitCaseMeta.TENTH_CIRCUIT

    with pytest.raises(Exception) as e:
        obj1.circuit_name = "13th Circuit"
    
    assert str(e.value) == "circuit_name is not a valid circuit name or None. Valid names must be one of the following (or a None): Federal Circuit, 1st Circuit, 2nd Circuit, 3rd Circuit, 4th Circuit, 5th Circuit, 6th Circuit, 7th Circuit, 8th Circuit, 9th Circuit, 10th Circuit, 11th Circuit, DC Circuit"

    obj1.circuit_name = None
    assert obj1.circuit_name == None

def test_circuit_num():
    # test that the circuit_num method works as expected
    obj1 = USCircuitCaseMeta(
            case_id = "X44DV3",
            case_name = "Barker v. United States",
            title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
            doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
            tags = ["WORLD", "HELLO"],
            circuit_name = USCircuitCaseMeta.ELEVENTH_CIRCUIT
        )

    assert obj1.circuit_num() == 11

    obj1.circuit_name = USCircuitCaseMeta.FIRST_CIRCUIT

    assert obj1.circuit_num() == 1

    obj1.circuit_name = None
    assert obj1.circuit_num() == None

def test_from_json_dict():
    data = {
        'case_id': 'X1111',
        'circuit_name': USCircuitCaseMeta.THIRD_CIRCUIT,
        'outcome': 'Affirmed (In Part)',
        'date': '1972-03-01',
        'self_cite': None
    }

    ucm  = USCircuitCaseMeta.from_json_dict(data)
    
    assert ucm == USCircuitCaseMeta(
        case_id= "X1111",
        circuit_name =  USCircuitCaseMeta.THIRD_CIRCUIT,
        outcome = "Affirmed (In Part)",
        date = datetime.date(1972,3,1),
        self_cite = None
    )

def test_from_json_dict_invalid_circuit():
    data = {
        'case_id': 'X1111',
        'circuit_name': 'Twelfth Court',
        'outcome': 'Affirmed (In Part)'
    }

    with pytest.raises(Exception) as e:
        USCircuitCaseMeta.from_json_dict(data)
     
    assert str(e.value) == "circuit_name is not a valid circuit name or None. Valid names must be one of the following (or a None): Federal Circuit, 1st Circuit, 2nd Circuit, 3rd Circuit, 4th Circuit, 5th Circuit, 6th Circuit, 7th Circuit, 8th Circuit, 9th Circuit, 10th Circuit, 11th Circuit, DC Circuit"

def test_from_json_dict_no_circuit():
    data = {
        'case_id': 'X1111',
        'circuit_name': None,
        'outcome': 'Affirmed (In Part)',
        'date': '1972-03-01',
        'self_cite': None
    }

    ucm  = USCircuitCaseMeta.from_json_dict(data)
    
    assert ucm == USCircuitCaseMeta(
        case_id= "X1111",
        circuit_name =  None,
        outcome = "Affirmed (In Part)",
        date = datetime.date(1972,3,1),
        self_cite = None
    )

def test_to_json_dict():
    ucm  = USCircuitCaseMeta(
            case_id = "X44DV3",
            case_name = "Barker v. United States",
            title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
            doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
            tags = ["WORLD", "HELLO"],
            circuit_name = USCircuitCaseMeta.ELEVENTH_CIRCUIT,
            date = datetime.date(1984,8,5)
        )

    # tags should be sorted alphabetically, so the same object always produces the same dictionary
    data = {
        'case_id' : "X44DV3",
        'case_name' : "Barker v. United States",
        'title' : "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        'doc_title' : "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        'tags' : ["HELLO", "WORLD"],
        'circuit_name' : USCircuitCaseMeta.ELEVENTH_CIRCUIT,
        'doc_id': '',
        'doc_type': '',
        'docket_number': '',
        'outcome': '',
        'self_cite': '',
        'date': '1984-08-05'
    }

    assert ucm.to_json_dict() == data

def test_to_json_dict_no_date():
    ucm  = USCircuitCaseMeta(
            case_id = "X44DV3",
            case_name = "Barker v. United States",
            title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
            doc_title = "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
            tags = ["WORLD", "HELLO"],
            circuit_name = USCircuitCaseMeta.ELEVENTH_CIRCUIT,
            self_cite = None
        )

    # tags should be sorted alphabetically, so the same object always produces the same dictionary
    data = {
        'case_id' : "X44DV3",
        'case_name' : "Barker v. United States",
        'title' : "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        'doc_title' : "Barker v. United States, 198 F.2d 932 (9th Cir. 1952), Court Opinion",
        'tags' : ["HELLO", "WORLD"],
        'circuit_name' : USCircuitCaseMeta.ELEVENTH_CIRCUIT,
        'doc_id': '',
        'doc_type': '',
        'docket_number': '',
        'outcome': '',
        'self_cite': None,
        'date': None
    }

    assert ucm.to_json_dict() == data
    