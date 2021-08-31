from lcsscaseapi.types import USCircuitCaseMeta
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
    assert str(e.value) == "circuit_name is not a valid circuit name or empty string. Valid names must be one of the following (or an empty string): Federal Circuit, 1st Circuit, 2nd Circuit, 3rd Circuit, 4th Circuit, 5th Circuit, 6th Circuit, 7th Circuit, 8th Circuit, 9th Circuit, 10th Circuit, 11th Circuit, DC Circuit"

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
    
    assert str(e.value) == "circuit_name is not a valid circuit name or empty string. Valid names must be one of the following (or an empty string): Federal Circuit, 1st Circuit, 2nd Circuit, 3rd Circuit, 4th Circuit, 5th Circuit, 6th Circuit, 7th Circuit, 8th Circuit, 9th Circuit, 10th Circuit, 11th Circuit, DC Circuit"

    obj1.circuit_name = ""
    assert obj1.circuit_name == ""

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

    obj1.circuit_name = ""
    assert obj1.circuit_num() == None

