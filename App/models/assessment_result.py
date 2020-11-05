from db import db
from models.subject import SubjectModel
from models.student import StudentModel
from models.assessment_skill import AssessmentSkillModel
from models.assessment_period import AssessmentPeriodModel
from models.assessment_category import AssessmentCategoryModel
from models.kalika_kendra import KalikaKendraModel
from models.cluster import ClusterModel


class AssessmentResultModel(db.Model):
    __tablename__ = "assessment_result"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attempt_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('assessment_category.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('assessment_skill.id'))
    period_id = db.Column(db.Integer, db.ForeignKey('assessment_period.id'))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    session = db.Column(db.String(200))
    score = db.Column(db.Integer)
    full_score = db.Column(db.Integer)
    grade = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)
    modified_by = db.Column(db.String(200))

    def __init__(self, **kwargs):
        cols = ['attempt_id', 'student_id', 'subject_id',
                'category_id', 'skill_id', 'period_id',
                'year', 'month', 'day', 'session',
                'score', 'full_score', 'grade',
                'creation_date', 'modified_date', 'modified_by']
        for col in cols:
            setattr(self, col, None)
        for col in kwargs.keys():
            if col in cols:
                setattr(self, col, kwargs[col])
        return None

    def json(self):
        student = StudentModel.find_by_student_id(self.student_id)
        cluster = ClusterModel.find_by_cluster_id(student.cluster_id)
        kalika_kendra = KalikaKendraModel.find_by_kalika_kendra_id(student.kalika_kendra_id)
        return {'result_id': self.id, 'attempt_id': self.attempt_id,
                'student_id': self.student_id,
                'student_name': student.student_name if student else None,
                'cluster_id': cluster.id if cluster else None,
                'cluster_name': cluster.cluster_name if cluster else None,
                'kalika_kendra_id': kalika_kendra.id if kalika_kendra else None,
                'kalika_kendra_name': kalika_kendra.kalika_kendra_name if kalika_kendra else None,
                'subject_id': self.subject_id,
                'subject_name':
                    SubjectModel.find_by_subject_id(self.subject_id).subject_name,
                'assessment_category_id': self.category_id,
                'assessment_category_name': AssessmentCategoryModel.find_by_category_id(
                    self.category_id).category_name,
                'assessment_skill_id': self.skill_id,
                'assessment_skill_name': AssessmentSkillModel.find_by_skill_id(self.skill_id).skill_name if AssessmentSkillModel.find_by_skill_id(self.skill_id) else None,
                'assessment_period_id': self.period_id,
                'assessment_year': self.year,
                'assessment_month': self.month,
                'assessment_day': self.day,
                'assessment_session': self.session,
                'assessment_score': self.score,
                'assessment_full_score': self.full_score,
                'assessment_grade': self.grade,
                'creation_date': str(self.creation_date),
                'modified_date': str(self.modified_date),
                'modified_by': self.modified_by}

    @classmethod
    def find_by_result_id(cls, result_id):
        return cls.query.filter_by(id=result_id).first()

    @classmethod
    def find_by_student_ids(cls, student_id_list):
        # print(student_id_list)
        return cls.query.filter(cls.student_id.in_(student_id_list)).first()

    @classmethod
    def find_by_kalika_kendra_id(cls, kalika_kendra_id):
        return cls.query.filter_by(kalika_kendra_id=kalika_kendra_id).first()

    @classmethod
    def find_assessment_result_by_any(cls, **kwargs):
        cols = ['attempt_id', 'student_id', 'subject_id', 'assessment_category_id',
                'assessment_skill_id', 'assessment_period_id', 'assessment_year', 'assessment_month', 'assessment_day', 'assessment_session',
                'assessment_score', 'assessment_full_score', 'assessment_grade', 'creation_date',
                'modified_date', 'modified_by']
        filter_str = 'cls.query'
        if 'result_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(id="' + str(
                kwargs['result_id']) + '")'
        if 'attempt_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(attempt_id="' + str(
                kwargs['attempt_id']) + '")'
        if 'student_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(student_id="' + str(
                kwargs['student_id']) + '")'
        if 'subject_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(subject_id="' + str(
                kwargs['subject_id']) + '")'
        if 'category_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(category_id="' + str(
                kwargs['category_id']) + '")'
        if 'skill_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(skill_id="' + str(
                kwargs['skill_id']) + '")'
        if 'period_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(period_id="' + str(
                kwargs['period_id']) + '")'
        if 'year' in kwargs.keys():
            filter_str = filter_str + '.filter_by(year="' + str(
                kwargs['year']) + '")'
        if 'month' in kwargs.keys():
            filter_str = filter_str + '.filter_by(month="' + str(
                kwargs['month']) + '")'
        if 'day' in kwargs.keys():
            filter_str = filter_str + '.filter_by(day="' + str(
                kwargs['day']) + '")'
        if 'session' in kwargs.keys():
            filter_str = filter_str + '.filter_by(session="' + str(
                kwargs['session']) + '")'
        if 'score' in kwargs.keys():
            filter_str = filter_str + '.filter_by(score="' + str(
                kwargs['score']) + '")'
        if 'full_score' in kwargs.keys():
            filter_str = filter_str + '.filter_by(full_score="' + str(
                kwargs['full_score']) + '")'
        if 'grade' in kwargs.keys():
            filter_str = filter_str + '.filter_by(grade="' + str(
                kwargs['grade']) + '")'
        if 'creation_date' in kwargs.keys():
            filter_str = filter_str + '.filter_by(creation_date="' + str(
                kwargs['creation_date']) + '")'
        if 'modified_date' in kwargs.keys():
            filter_str = filter_str + '.filter_by(modified_date="' + str(
                kwargs['modified_date']) + '")'
        if 'modified_by' in kwargs.keys():
            filter_str = filter_str + '.filter_by(modified_by="' + str(
                kwargs['modified_by']) + '")'
        if 'subject_name' in kwargs.keys():
            subject = SubjectModel.find_by_subject_name(kwargs['subject_name'])
            if subject:
                subject_id = subject.id
                filter_str = filter_str + '.filter_by(subject_id="'\
                             + str(subject_id) + '")'
        if 'category_name' in kwargs.keys():
            assessment_category = AssessmentCategoryModel.find_by_category_name(kwargs['category_name'])
            if assessment_category:
                category_id = assessment_category.id
                filter_str = filter_str + '.filter_by(category_id="' + str(category_id) + '")'
        if 'student_name' in kwargs.keys():
            student = StudentModel.find_by_student_name(kwargs['student_name'])
            if student:
                student_id = student.id
                filter_str = filter_str + '.filter_by(student_id="' + str(
                    student_id) + '")'
        if 'skill_name' in kwargs.keys():
            skill = AssessmentSkillModel.find_by_skill_name(kwargs['skill_name'])
            if skill:
                skill_id = skill.id
                filter_str = filter_str + '.filter_by(skill_id="' + str(skill_id) + '")'
        if 'cluster_id' in kwargs.keys():
            payload = {"cluster_id": kwargs["cluster_id"]}
            students = StudentModel.find_by_student_by_any(**payload)
            if students:
                student_ids = [s.id for s in students]
                # print(student_ids)
                filter_str = filter_str + '.filter(cls.student_id.in_(' + str(student_ids) + '))'
        if 'kalika_kendra_id' in kwargs.keys():
            payload = {"kalika_kendra_id": kwargs["kalika_kendra_id"]}
            students = StudentModel.find_by_student_by_any(**payload)
            if students:
                student_ids = [s.id for s in students]
                filter_str = filter_str + '.filter(cls.student_id.in_(' + str(student_ids) + '))'
        if 'cluster_name' in kwargs.keys():
            payload = {"cluster_name": kwargs["cluster_name"]}
            students = StudentModel.find_by_student_by_any(**payload)
            if students:
                student_ids = [s.id for s in students]
                filter_str = filter_str + '.filter(cls.student_id.in_(' + str(student_ids) + '))'
        if 'kalika_kendra_name' in kwargs.keys():
            payload = {"kalika_kendra_name": kwargs["kalika_kendra_name"]}
            students = StudentModel.find_by_student_by_any(**payload)
            if students:
                student_ids = [s.id for s in students]
                filter_str = filter_str + '.filter(cls.student_id.in_(' + str(student_ids) + '))'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    def set_attribute(self, payload):
        cols = ['attempt_id', 'student_id', 'subject_id',
                'category_id', 'skill_id', 'period_id',
                'year', 'month', 'day', 'session',
                'score', 'full_score', 'grade',
                'creation_date', 'modified_date', 'modified_by']
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
                self.category_id = assessment_categories[0].id
        if 'skill_name' in payload.keys():
            # data = {'skill_name': payload["skill_name"]}
            assessment_skill = AssessmentSkillModel.find_by_skill_name(payload["skill_name"])
            if assessment_skill:
                self.skill_id = assessment_skill.id
        if 'subject_name' in payload.keys():
            data = {'category_name': payload["subject_name"]}
            subject = StudentModel.find_by_student_name(payload["subject_name"])
            if subject:
                self.subject_id = subject.id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
