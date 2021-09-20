def test_jr_constructor():
    # test that missing fields set to None
    # test that judge_id and case_id fields are mandatory
    pass

def test_jr_constructor_invalid_vote():
    # votes can only be concurring or dissenting
    pass

def test_jr_vote_setter():
    # again, votes can only be set to concurring or dissenting
    pass

def test_jr_eq():
    pass

def test_jr_str():
    pass

def test_jr_repr():
    pass

def test_jr_to_json_dict():
    pass

def test_jr_from_json_dict():
    pass

def test_jr_from_json_dict_missing_fields():
    # check that trying to create a jr with no `case` or `judge` field fails
    # missing any other field should not pose an issue
    pass

def test_jr_from_json_dict_incorrect_vote():
    # check, again that votes meet validation requirements
    pass

def test_jr_from_json_dict_extra_fields():
    # extra fields should be simply ignored
    pass