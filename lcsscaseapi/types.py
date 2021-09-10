import json
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder


class CaseMeta:
    def __init__(self, case_id = None, case_name = None, title = None, doc_title = None, doc_id = None, doc_type = None, docket_number = None, outcome = None,
                    self_cite = None, tags = [], date = None):
        self.case_id = case_id
        self.case_name = case_name
        self.title = title
        self.doc_title = doc_title
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.docket_number = docket_number
        self.outcome = outcome
        self.self_cite = self_cite
        self.date = date
        self.tags = tags
        self.tags.sort()
    
    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, CaseMeta):
            return NotImplemented
        
        self.tags.sort()
        other.tags.sort()
        return str(self) == str(other)

    def __neq__(self, other):
            return not self.__eq__(other)
    
    def __str__(self):
        # be careful with this - if some key's values should be hidden in a future change make sure to change this method
        return json.dumps(self.__dict__, sort_keys=True, cls=DjangoJSONEncoder)
    
    def __repr__(self):
        return "CaseMeta Object: " + str(self)

    @classmethod
    def from_json_dict(self, fields):
        cm = self()
        cm.case_id = fields.get("case_id", None)
        cm.case_name = fields.get("case_name", None)
        cm.title = fields.get("title", None)
        cm.doc_title = fields.get("doc_title", None)
        cm.doc_id = fields.get("doc_id", None)
        cm.doc_type = fields.get("doc_type", None)
        cm.docket_number = fields.get("docket_number", None)
        cm.outcome = fields.get("outcome", None)
        cm.self_cite = fields.get("self_cite", None)
        cm.tags = fields.get("tags", [])
        datestring = fields.get("date", None)
        if datestring != None:
            print(datestring)
            print(fields)
            cm.date = datetime.strptime(datestring, '%Y-%m-%d').date()
        else:
            cm.date = None
        return cm


class USCircuitCaseMeta(CaseMeta):
    FED_CIRCUIT = "Federal Circuit"
    FIRST_CIRCUIT = "1st Circuit"
    SECOND_CIRCUIT = "2nd Circuit"
    THIRD_CIRCUIT = "3rd Circuit"
    FOURTH_CIRCUIT = "4th Circuit"
    FIFTH_CIRCUIT = "5th Circuit"
    SIXTH_CIRCUIT = "6th Circuit"
    SEVENTH_CIRCUIT = "7th Circuit"
    EIGHTH_CIRCUIT = "8th Circuit"
    NINTH_CIRCUIT = "9th Circuit"
    TENTH_CIRCUIT = "10th Circuit"
    ELEVENTH_CIRCUIT = "11th Circuit"
    DC_CIRCUIT = "DC Circuit"
    CIRCUITS = [FED_CIRCUIT, FIRST_CIRCUIT, SECOND_CIRCUIT, THIRD_CIRCUIT, FOURTH_CIRCUIT, FIFTH_CIRCUIT, SIXTH_CIRCUIT, SEVENTH_CIRCUIT, 
                EIGHTH_CIRCUIT, NINTH_CIRCUIT, TENTH_CIRCUIT, ELEVENTH_CIRCUIT, DC_CIRCUIT]
    def __init__(self, case_id = None, case_name = None, title = None, doc_title = None, doc_id = None, doc_type = None, docket_number = None, outcome = None,
                    self_cite = None, tags = [], date = None, circuit_name = None):
        super().__init__(case_id, case_name, title, doc_title, doc_id, doc_type, docket_number, outcome, self_cite, tags, date)
        self.circuit_name = circuit_name

    @property
    def circuit_name(self):
        return self._circuit_name
    
    @circuit_name.setter
    def circuit_name(self, val):
        if val not in USCircuitCaseMeta.CIRCUITS and val != None:
            raise Exception("circuit_name is not a valid circuit name or None. Valid names must be one of the following (or a None): " 
                                        + ", ".join(USCircuitCaseMeta.CIRCUITS))
        self._circuit_name = val

    # Returns the circuit of this case as a number
    # The Federal circuit is returned as 0
    # The DC circuit is returned as 12
    # If no circuit is associated with this case, None is returned
    def circuit_num(self):
        if self.circuit_name == None:
            return None
        return USCircuitCaseMeta.CIRCUITS.index(self.circuit_name)

    # converts this object to a dictionary, correcting the _circuit_name
    def to_json_dict(self):
        data_dict = dict(self.__dict__) # make a copy, so as to not edit the original copy
        # print(data_dict)
        data_dict["circuit_name"] = data_dict["_circuit_name"]
        data_dict["tags"].sort()
        del data_dict["_circuit_name"]
        if data_dict["date"] != None:
            data_dict["date"] = json.dumps(data_dict["date"], cls=DjangoJSONEncoder).strip('\"')
        return data_dict

    # overriding this suffices to change behavior of eq and neq as well
    def __str__(self):
        return json.dumps(self.to_json_dict(), sort_keys=True, cls=DjangoJSONEncoder)
        
    @classmethod
    def from_json_dict(self, fields):
        case_meta = super().from_json_dict(fields)
        us_case = USCircuitCaseMeta()
        us_case.__dict__ = case_meta.__dict__ # copy over all attributes from the casemeta object
        us_case.circuit_name = fields.get("circuit_name", None)

        return us_case
        

class Judge:
    MALE = "Male"
    FEMALE = "Female"
    GENDERS = [MALE, FEMALE]
    def __init__(self, id=None, gender=None, name = None, orig_name=None):
        self.id = id
        self.judge_gender = gender
        self.judge_name = name
        self.judge_orig_name = orig_name

    @property
    def judge_gender(self):
        return self._judge_gender
    
    @judge_gender.setter
    def judge_gender(self, val):
        if val not in Judge.GENDERS and val != None:
            raise Exception("Gender must be Male, Female or None")
        self._judge_gender = val

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, CaseMeta):
            return NotImplemented
     
        return str(self) == str(other)

    def __neq__(self, other):
            return not self.__eq__(other)
    
    def __str__(self):
        # be careful with this - if some key's values should be hidden in a future change make sure to change this method
        return json.dumps(self.to_json_dict(), sort_keys=True, cls=DjangoJSONEncoder) # DjangoJSONEncoder makes sure dates are handled in the right format
    
    def __repr__(self):
        return "Judge Object: " + str(self)
    
      # converts this object to a dictionary, correcting the _judge_gender
    def to_json_dict(self):
        data_dict = dict(self.__dict__) # make a copy, so as to not edit the original dict
        data_dict["judge_gender"] = data_dict["_judge_gender"]
        del data_dict["_judge_gender"]
        return data_dict

    @classmethod
    def from_json_dict(self, fields):
        judge = self()
        judge.id = fields.id
        judge.judge_gender = fields.judge_gender
        judge.judge_name = fields.judge_name 
        judge.judge_orig_name = fields.judge_orig_name