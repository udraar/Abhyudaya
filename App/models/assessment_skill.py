from db import db
from models.subject import SubjectModel
from models.assessment_category import AssessmentCategoryModel


class AssessmentSkillModel(db.Model):
    __tablename__ = "assessment_skill"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_name = db.Column(db.String(200))
    skill_code = db.Column(db.String(200))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    category_id = db.Column(db.Integer,
                                       db.ForeignKey('assessment_category.id'))
    isactive = db.Column(db.Integer)

    def __init__(self, skill_name, skill_code, subject_id,
                 category_id, isactive=1):
        self.skill_name = skill_name
        self.skill_code = skill_code
        self.subject_id = subject_id
        self.category_id = category_id
        self.isactive = isactive

    def json(self):
        return {'skill_id': self.id, 'skill_name': self.skill_name,
                'skill_code': self.skill_code,
                'subject_id': self.subject_id,
                'subject_name':
                    SubjectModel.find_by_subject_id(self.subject_id).subject_name,
                'category_id': self.category_id,
                'category_name': AssessmentCategoryModel.find_by_category_id(
                    self.category_id).category_name,
                'isactive': self.isactive}

    @classmethod
    def find_by_skill_id(cls, skill_id):
        return cls.query.filter_by(id=skill_id).first()

    @classmethod
    def find_by_skill_name(cls, skill_name):
        return cls.query.filter_by(skill_name=skill_name).first()

    @classmethod
    def find_by_category_id(cls, category_id):
        return cls.query.filter_by(category_id=category_id).first()

    @classmethod
    def find_assessment_skill_by_any(cls, **kwargs):
        cols = ['skill_name', 'skill_code', 'subject_id', 'subject_name'
                'category_id', 'isactive']
        filter_str = 'cls.query'
        if 'skill_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(skill_name="' + str(
                kwargs['skill_name']) + '")'
        if 'skill_code' in kwargs.keys():
            filter_str = filter_str + '.filter_by(skill_code="' + str(
                kwargs['skill_code']) + '")'
        if 'subject_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(subject_id="' + str(
                kwargs['subject_id']) + '")'
        if 'category_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(category_id="' + str(
                kwargs['category_id']) + '")'
        if 'isactive' in kwargs.keys():
            filter_str = filter_str + '.filter_by(isactive="' + str(
                kwargs['isactive']) + '")'
        if 'subject_name' in kwargs.keys():
            subject = SubjectModel.find_by_subject_name(kwargs["subject_name"])
            if subject:
                subject_id = subject.id
                filter_str = filter_str + '.filter_by(subject_id="'\
                             + str(subject_id) + '")'
        if 'category_name' in kwargs.keys():
            assessment_category = AssessmentCategoryModel.find_by_category_name(
                kwargs['category_name'])
            if assessment_category:
                assessment_category_id = assessment_category.id
                filter_str = filter_str + '.filter_by(category_id="' + str(category_id) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    def set_attribute(self, payload):
        cols = ['skill_name', 'skill_code', 'subject_id', 'category_id','isactive']
        for col in cols:
            if col in payload.keys():
                setattr(self, col, payload[col])
        if 'subject_name' in payload.keys():
            subjects = SubjectModel.find_by_subject_name(payload["subject_name"])
            if subjects:
                self.subject_id = subjects[0].id
        if 'category_name' in payload.keys():
            data = {'category_name': payload["category_name"]}
            assessment_categories = AssessmentCategoryModel.find_assessment_category_by_any(
                **data)
            if assessment_categories:
                self.assessment_category_id = assessment_categories[0].id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
