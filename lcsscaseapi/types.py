import json

class CaseMeta:
    def __init__(self, case_id = "", case_name = "", title = "", doc_title = "", doc_id = "", doc_type = "", docket_number = "", outcome = "",
                    self_cite = "", tags = []):
        self.case_id = case_id
        self.case_name = case_name
        self.title = title
        self.doc_title = doc_title
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.docket_number = docket_number
        self.outcome = outcome
        self.self_cite = self_cite
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
            return not str(self) == str(other)
    
    def __str__(self):
        # be careful with this - if some key's values should be hidden in a future change make sure to change this method
        return json.dumps(self.__dict__, sort_keys=True)
    
    def __repr__(self):
        return "CaseMeta Object: " + str(self)

    @classmethod
    def from_dict(self, **fields):
        cm = self()
        cm.case_id = fields.get("case_id", "")
        cm.case_name = fields.get("case_name", "")
        cm.title = fields.get("title", "")
        cm.doc_title = fields.get("doc_title", "")
        cm.doc_id = fields.get("doc_id", "")
        cm.doc_type = fields.get("doc_type", "")
        cm.docket_number = fields.get("docket_number", "")
        cm.outcome = fields.get("outcome", "")
        cm.self_cite = fields.get("self_cite", "")
        cm.tags = fields.get("tags", [])
        return cm