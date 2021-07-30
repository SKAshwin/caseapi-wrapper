import json

class CaseMeta:
    def __init__(self, case_id = "", case_name = "", title = "", doc_title = "", doc_id = "", doc_type = "", docket_number = "", outcome = ""):
        self.case_id = case_id
        self.case_name = case_name
        self.title = title
        self.doc_title = doc_title
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.docket_number = docket_number
        self.outcome = outcome
    
    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, CaseMeta):
            return NotImplemented
        
        return str(self) == str(other)

    def __neq__(self, other):
            return not str(self) == str(other)
    
    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True)

    @classmethod
    def from_dict(self, **fields):
        cm = self()
        cm.__dict__.update(fields)
        return cm