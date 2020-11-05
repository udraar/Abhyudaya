from db import db
from models.subject import SubjectModel


class AssessmentCategoryModel(db.Model):
    __tablename__ = "assessment_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(200))
    category_code = db.Column(db.Integer)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    isactive = db.Column(db.Integer)

    def __init__(self, category_name, category_code, subject_id, isactive=1):
        self.category_name = category_name
        self.category_code = category_code
        self.subject_id = subject_id
        self.isactive = isactive

    def json(self):
        return {'category_id': self.id, 'category_name': self.category_name,
                'category_code': self.category_code,
                'subject_id': self.subject_id,
                'subject_name': SubjectModel.find_by_subject_id(self.subject_id).subject_name,
                'isactive': self.isactive}

    @classmethod
    def find_by_category_id(cls, category_id):
        return cls.query.filter_by(id=category_id).first()

    @classmethod
    def find_by_category_name(cls, category_name):
        return cls.query.filter_by(category_name=category_name).first()

    @classmethod
    def find_assessment_category_by_any(cls, **kwargs):
        cols = ['category_name', 'category_code', 'subject_id', 'isactive']
        filter_str = 'cls.query'
        if 'category_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(category_name="' + str(
                kwargs['category_name']) + '")'
        if 'category_code' in kwargs.keys():
            filter_str = filter_str + '.filter_by(category_code="' + str(
                kwargs['category_code']) + '")'
        if 'subject_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(subject_id="' + str(
                kwargs['subject_id']) + '")'
        if 'isactive' in kwargs.keys():
            filter_str = filter_str + '.filter_by(isactive="' + str(
                kwargs['isactive']) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    @classmethod
    def find_by_subject_name(cls, subject_name):
        subject = SubjectModel.find_by_subject_name(subject_name)
        if subject:
            subject_id = subject.id
            return cls.query.filter_by(subject_id=subject_id).first()
        else:
            return None

    def set_attribute(self, payload):
        cols = ['category_name', 'category_code', 'subject_id', 'isactive']
        for col in cols:
            if col in payload.keys():
                setattr(self, col, payload[col])
        if 'subject_name' in payload.keys():
            subject = SubjectModel.find_by_subject_name(payload["subject_name"])
            if subject:
                self.subject_id = subject.id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
