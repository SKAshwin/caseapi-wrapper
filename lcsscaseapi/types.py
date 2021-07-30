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
        # be careful with this - if some key's values should be hidden in a future change make sure to change this method
        return json.dumps(self.__dict__, sort_keys=True)
    
    def __repr__(self):
        return "CaseMeta Object: " + str(self)

    @classmethod
    def from_dict(self, **fields):
        cm = self()
        cm.case_id = fields["case_id"]
        cm.case_name = fields["case_name"]
        cm.title = fields["title"]
        cm.doc_title = fields["doc_title"]
        cm.doc_id = fields["doc_id"]
        cm.doc_type = fields["doc_type"]
        cm.docket_number = fields["docket_number"]
        cm.outcome = fields["outcome"]
        return cm