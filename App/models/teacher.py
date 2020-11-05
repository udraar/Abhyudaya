from datetime import datetime

from db import db
from models.cluster import ClusterModel
from models.kalika_kendra import KalikaKendraModel


class TeacherModel(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_name = db.Column(db.String(200))
    teacher_code = db.Column(db.String(200))
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
    kalika_kendra_id = db.Column(db.Integer, db.ForeignKey('kalika_kendra.id'))
    isactive = db.Column(db.Integer, default='1')
    bank_account_no = db.Column(db.String(20))
    bank_name = db.Column(db.String(200))
    ifsc = db.Column(db.String(20))
    teacher_category = db.Column(db.String(20))
    creation_date = db.Column(db.DateTime, nullable=False,
                              default=datetime.now())
    modified_date = db.Column(db.DateTime, nullable=False,
                              default=datetime.now())

    def __init__(self, **kwargs):
        cols = ['teacher_name', 'teacher_code', 'isactive', 'bank_account_no',
                'bank_name', 'ifsc', 'teacher_category', 'creation_date', 'modified_date']
        for col in cols:
            setattr(self, col, None)
        for col in kwargs.keys():
            if col in cols:
                setattr(self, col, kwargs[col])
        kalika_kendra = KalikaKendraModel.find_by_kalika_kendra_name(
            kwargs['kalika_kendra_name'])
        # print(kalika_kendra.json())
        if not kalika_kendra:
            return {
                       "message": f"Kalika Kendra name not found for the teacher"}, 401
        cluster = ClusterModel.find_by_cluster_name(kwargs['cluster_name'])
        if not cluster:
            return {"message": f"Cluster name not found for the teacher"}, 401
        print(cluster.json())
        self.kalika_kendra_id = kalika_kendra.id
        self.cluster_id = cluster.id
        return None

    def json(self):
        return {'teacher_id': self.id, 'teacher_name': self.teacher_name,
                'teacher_code': self.teacher_code,
                'kalika_kendra_id': self.kalika_kendra_id,
                'cluster_id': self.cluster_id,
                'kalika_kendra_name':
                    KalikaKendraModel.find_by_kalika_kendra_id(
                        self.kalika_kendra_id).kalika_kendra_name if KalikaKendraModel.find_by_kalika_kendra_id(
                        self.kalika_kendra_id) else None,
                'cluster_name': ClusterModel.find_by_cluster_id(
                    self.cluster_id).cluster_name, 'isactive': self.isactive,
                'bank_account_no': self.bank_account_no,
                'bank_name': self.bank_name,
                'ifsc': self.ifsc,
                'teacher_category': self.teacher_category,
                'creation_date': str(self.creation_date),
                'modified_date': str(self.modified_date)
                }

    @classmethod
    def find_by_teacher_name(cls, teacher_name):
        return cls.query.filter_by(teacher_name=teacher_name).first()

    @classmethod
    def find_by_teacher_code(cls, teacher_code):
        # print(teacher_code)
        return cls.query.filter_by(teacher_code=teacher_code).first()

    @classmethod
    def find_by_teacher_id(cls, teacher_id):
        return cls.query.filter_by(id=teacher_id).first()

    @classmethod
    def find_by_cluster_id(cls, cluster_id):
        return cls.query.filter_by(cluster_id=cluster_id).first()

    @classmethod
    def find_by_kalika_kendra_id(cls, kalika_kendra_id):
        return cls.query.filter_by(kalika_kendra_id=kalika_kendra_id).first()

    @classmethod
    def find_by_cluster_name(cls, cluster_name):
        cluster = ClusterModel.find_by_cluster_name(cluster_name)
        return cls.query.filter_by(cluster_id=cluster.id).first()

    @classmethod
    def find_by_kalika_kendra_name(cls, kalika_kendra_name):
        kalika_kendra = KalikaKendraModel.find_by_kalika_kendra_name(
            kalika_kendra_name)
        return cls.query.filter_by(kalika_kendra_id=kalika_kendra.id).first()

    @classmethod
    def find_by_isactive(cls, isactive):
        return cls.query.filter_by(isactive=isactive).first()

    @classmethod
    def find_by_any(cls, **kwargs):
        cols = ['teacher_id', 'teacher_name', 'teacher_code', 'cluster_id',
                'kalika_kendra_id', 'cluster_name', 'kalika_kendra_name',
                'isactive',
                'bank_account_no', 'bank_name', 'ifsc', 'teacher_category']
        filter_str = 'cls.query'
        if 'bank_account_no' in kwargs.keys():
            filter_str = filter_str + '.filter_by(bank_account_no="' + str(
                kwargs['bank_account_no']) + '")'
        if 'bank_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(bank_name="' + str(
                kwargs['bank_name']) + '")'
        if 'ifsc' in kwargs.keys():
            filter_str = filter_str + '.filter_by(ifsc="' + str(
                kwargs['ifsc']) + '")'
        if 'teacher_category' in kwargs.keys():
            filter_str = filter_str + '.filter_by(teacher_category="' + str(
                kwargs['teacher_category']) + '")'
        if 'creation_date' in kwargs.keys():
            filter_str = filter_str + '.filter_by(creation_date="' + str(
                kwargs['creation_date']) + '")'
        if 'modified_date' in kwargs.keys():
            filter_str = filter_str + '.filter_by(modified_date="' + str(
                kwargs['modified_date']) + '")'
        if 'teacher_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(id="' + str(
                kwargs['teacher_id']) + '")'
        if 'teacher_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(teacher_name="' + str(
                kwargs['teacher_name']) + '")'
        if 'teacher_code' in kwargs.keys():
            filter_str = filter_str + '.filter_by(teacher_code="' + str(
                kwargs['teacher_code']) + '")'
        if 'cluster_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(cluster_id="' + str(
                kwargs['cluster_id']) + '")'
        if 'kalika_kendra_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(kalika_kendra_id="' + str(
                kwargs['kalika_kendra_id']) + '")'
        if 'kalika_kendra_name' in kwargs.keys():
            kalika_kendra = KalikaKendraModel.find_by_kalika_kendra_name(
                kwargs['kalika_kendra_name'])
            if kalika_kendra:
                kalika_kendra_id = kalika_kendra.id
                filter_str = filter_str + '.filter_by(kalika_kendra_id="' \
                             + str(kalika_kendra_id) + '")'
        if 'cluster_name' in kwargs.keys():
            cluster = ClusterModel.find_by_cluster_name(kwargs['cluster_name'])
            if cluster:
                cluster_id = cluster.id
                filter_str = filter_str + '.filter_by(cluster_id="' \
                             + str(cluster_id) + '")'
        if 'isactive' in kwargs.keys():
            filter_str = filter_str + '.filter_by(isactive="' + str(
                kwargs['isactive']) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    def set_attribute(self, payload):
        cols = ['teacher_name', 'teacher_code', 'isactive', 'bank_account_no',
                'bank_name', 'ifsc', 'teacher_category', 'modified_date']
        for col in cols:
            if col in payload.keys():
                setattr(self, col, payload[col])
        if 'cluster_name' in payload.keys():
            cluster = ClusterModel.find_by_cluster_name(
                payload['cluster_name'])
            if not cluster:
                return {
                           "message": f"Cluster name not found for the teacher"}, 401
            self.cluster_id = cluster.id
        if 'kalika_kendra_name' in payload.keys():
            kalika_kendra = KalikaKendraModel.find_by_kalika_kendra_name(
                payload['kalika_kendra_name'])
            if not kalika_kendra:
                return {
                           "message": f"Kalika Kendra name not found for the teacher"}, 401
            self.kalika_kendra_id = cluster.id
        print(self.json())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
