from db import db

class SubjectModel(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(200))
    subject_code = db.Column(db.String(200))
    isactive = db.Column(db.Integer)

    def __init__(self, subject_name, subject_code, isactive=1):
        self.subject_name = subject_name
        self.subject_code = subject_code
        self.isactive = isactive

    def json(self):
        return {'subject_id': self.id,'subject_name': self.subject_name, 'subject_code': self.subject_code, 'isactive': self.isactive}

    @classmethod
    def find_by_subject_id(cls, subject_id):
        return cls.query.filter_by(id=subject_id).first()

    @classmethod
    def find_by_subject_name(cls, subject_name):
        return cls.query.filter_by(subject_name=subject_name).first()

    @classmethod
    def find_by_subject_code(cls, subject_code):
        return cls.query.filter_by(subject_code=subject_code).first()

    @classmethod
    def find_by_any(cls, **kwargs):
        filter_str = 'cls.query'
        cols = ['isactive', 'subject_name', 'subject_code']
        if 'isactive' in kwargs.keys():
            filter_str = filter_str + '.filter_by(isactive="' + str(
                kwargs['isactive']) + '")'
        if 'subject_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(subject_name="' + str(
                kwargs['subject_name']) + '")'
        if 'subject_code' in kwargs.keys():
            filter_str = filter_str + '.filter_by(subject_code="' + str(
                kwargs['subject_code']) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    def set_attribute(self, payload):
        cols = ['isactive', 'isdeprecated', 'subject_name', 'subject_code']
        for col in cols:
            if col in payload.keys():
                setattr(self, col, payload[col])

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()