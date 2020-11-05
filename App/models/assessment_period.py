from db import db


class AssessmentPeriodModel(db.Model):
    __tablename__ = "assessment_period"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_year = db.Column(db.Integer)
    assessment_month = db.Column(db.Integer)
    assessment_day = db.Column(db.Integer)
    session = db.Column(db.String(200))
    period = db.Column(db.String(200))

    def __init__(self, session, period, assessment_year=None,
                 assessment_month=None, assessment_day=None):
        self.session = session
        self.period = period
        self.assessment_year = assessment_year
        self.assessment_month = assessment_month
        self.assessment_day = assessment_day

    def json(self):
        return {'assessment_period_id': self.id, 'session': self.session,
                'period': self.period,
                'assessment_year': self.assessment_year,
                'assessment_month': self.assessment_month,
                'assessment_day': self.assessment_day}

    @classmethod
    def find_assessment_period_by_any(cls, **kwargs):
        cols = ['session', 'period', 'assessment_year', 'assessment_month',
                'assessment_day']
        filter_str = 'cls.query'
        if 'session' in kwargs.keys():
            filter_str = filter_str + '.filter_by(session="' + str(
                kwargs['session']) + '")'
        if 'period' in kwargs.keys():
            filter_str = filter_str + '.filter_by(period="' + str(
                kwargs['period']) + '")'
        if 'assessment_year' in kwargs.keys():
            filter_str = filter_str + '.filter_by(assessment_year="' + str(
                kwargs['assessment_year']) + '")'
        if 'assessment_month' in kwargs.keys():
            filter_str = filter_str + '.filter_by(assessment_month="' + str(
                kwargs['assessment_month']) + '")'
        if 'assessment_day' in kwargs.keys():
            filter_str = filter_str + '.filter_by(assessment_day="' + str(
                kwargs['assessment_day']) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    @classmethod
    def find_by_assessment_period_id(cls, assessment_period_id):
        return cls.query.filter_by(id=assessment_period_id).first()

    def set_attribute(self, payload):
        cols = ['session', 'period', 'assessment_year', 'assessment_month',
                'assessment_day']
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
