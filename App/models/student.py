from db import db
from models.cluster import ClusterModel
from models.kalika_kendra import KalikaKendraModel


class StudentModel(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_name = db.Column(db.String(200))
    gender = db.Column(db.String(200))
    aadhar = db.Column(db.String(200), unique=True)
    dob = db.Column(db.DateTime)
    class_std = db.Column(db.String(10))
    kalika_kendra_id = db.Column(db.Integer, db.ForeignKey('kalika_kendra.id'))
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
    father_name = db.Column(db.String(200))
    father_occupation = db.Column(db.String(200))
    mother_name = db.Column(db.String(200))
    mother_occupation = db.Column(db.String(200))
    contact = db.Column(db.String(15))
    isactive = db.Column(db.Integer)
    register_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)
    modified_by = db.Column(db.String(200), db.ForeignKey('user.email'))

    def __init__(self, **kwargs):
        cols = ['student_name', 'gender', 'aadhar',
                'dob', 'class_std', 'father_name',
                'father_occupation', 'mother_name',
                'mother_occupation', 'contact', 'isactive',
                'register_date', 'modified_date', 'modified_by', 'kalika_kendra_id', 'cluster_id']
        for col in cols:
            setattr(self, col, None)
        for col in kwargs.keys():
            if col in cols:
                setattr(self, col, kwargs[col])
        if kwargs.get('kalika_kendra_name'):
            kalika_kendra = KalikaKendraModel.find_by_kalika_kendra_name(kwargs['kalika_kendra_name'])
            if kalika_kendra:
                self.kalika_kendra_id = kalika_kendra.id
        if kwargs.get('cluster_name'):
            cluster = ClusterModel.find_by_cluster_name(kwargs['cluster_name'])
            if cluster:
                self.cluster_id = cluster.id
        return None

    def json(self):
        return {'student_id': self.id, 'student_name': self.student_name,
                'gender': self.gender, 'aadhar': self.aadhar,
                'dob': self.dob, 'class_std': self.class_std,
                'kalika_kendra_id': self.kalika_kendra_id,
                'kalika_kendra_name':
                    KalikaKendraModel.find_by_kalika_kendra_id(
                        self.kalika_kendra_id).kalika_kendra_name if KalikaKendraModel.find_by_kalika_kendra_id(
                        self.kalika_kendra_id) else None,
                'cluster_name': ClusterModel.find_by_cluster_id(
                    self.cluster_id).cluster_name,
                'cluster_id': self.cluster_id, 'father_name': self.father_name,
                'father_occupation': self.father_occupation,
                'mother_name': self.mother_name,
                'mother_occupation': self.mother_occupation,
                'contact': self.contact,
                'isactive': self.isactive,
                'register_date': str(self.register_date),
                'modified_date': str(self.modified_date),
                'modified_by': self.modified_by
                }

    @classmethod
    def find_by_student_by_any(cls, **kwargs):
        print(kwargs)
        filter_str = 'cls.query'
        if 'contact' in kwargs.keys():
            filter_str = filter_str + '.filter_by(contact="' + str(
                kwargs['contact']) + '")'
        if 'isactive' in kwargs.keys():
            filter_str = filter_str + '.filter_by(isactive="' + str(
                kwargs['isactive']) + '")'
        if 'register_date' in kwargs.keys():
            filter_str = filter_str + '.filter_by(register_date="' + str(
                kwargs['register_date']) + '")'
        if 'modified_date' in kwargs.keys():
            filter_str = filter_str + '.filter_by(modified_date="' + str(
                kwargs['modified_date']) + '")'
        if 'modified_by' in kwargs.keys():
            filter_str = filter_str + '.filter_by(modified_by="' + str(
                kwargs['modified_by']) + '")'
        if 'class_std' in kwargs.keys():
            filter_str = filter_str + '.filter_by(class_std="' + str(
                kwargs['class_std']) + '")'
        if 'kalika_kendra_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(kalika_kendra_id="' + str(
                kwargs['kalika_kendra_id']) + '")'
        if 'cluster_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(cluster_id="' + str(
                kwargs['cluster_id']) + '")'
        if 'kalika_kendra_name' in kwargs.keys():
            kalika_kendra = KalikaKendraModel.find_by_kalika_kendra_name(kwargs["kalika_kendra_name"])
            print(kalika_kendra.json())
            if kalika_kendra:
                kalika_kendra_id = kalika_kendra.id
                filter_str = filter_str + '.filter_by(kalika_kendra_id="' + str(
                kalika_kendra_id) + '")'
        if 'cluster_name' in kwargs.keys():
            cluster = ClusterModel.find_by_cluster_name(kwargs["cluster_name"])
            if cluster:
                cluster_id = cluster.id
                filter_str = filter_str + '.filter_by(cluster_id="' + str(
                kwargs['cluster_id']) + '")'
        if 'father_occupation' in kwargs.keys():
            filter_str = filter_str + '.filter_by(father_occupation="' + str(
                kwargs['father_occupation']) + '")'
        if 'mother_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(mother_name="' + str(
                kwargs['mother_name']) + '")'
        if 'mother_occupation' in kwargs.keys():
            filter_str = filter_str + '.filter_by(mother_occupation="' + str(
                kwargs['mother_occupation']) + '")'
        if 'student_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(student_id="' + str(
                kwargs['student_id']) + '")'
        if 'student_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(student_name="' + str(
                kwargs['student_name']) + '")'
        if 'gender' in kwargs.keys():
            filter_str = filter_str + '.filter_by(gender="' + str(
                kwargs['gender']) + '")'
        if 'aadhar' in kwargs.keys():
            filter_str = filter_str + '.filter_by(aadhar="' + str(
                kwargs['aadhar']) + '")'
        if 'dob' in kwargs.keys():
            filter_str = filter_str + '.filter_by(dob="' + str(
                kwargs['dob']) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    @classmethod
    def find_by_student_name(cls, student_name):
        return cls.query.filter_by(student_name=student_name).first()

    @classmethod
    def find_by_student_id(cls, student_id):
        return cls.query.filter_by(id=student_id).first()

    @classmethod
    def find_by_student_aadhar(cls, aadhar):
        return cls.query.filter_by(aadhar=aadhar).first()

    # @classmethod
    # def find_by_student_gender(cls, gender):
    #     return cls.query.filter_by(gender=gender).first()
    #
    # @classmethod
    # def find_by_student_class_std(cls, class_std):
    #     return cls.query.filter_by(class_std=class_std).first()
    #
    # @classmethod
    # def find_by_student_kalika_kendra_id(cls, kalika_kendra_id):
    #     return cls.query.filter_by(kalika_kendra_id=kalika_kendra_id).first()
    #
    # @classmethod
    # def find_by_student_kalika_kendra_name(cls, kalika_kendra_name):
    #     kalika_kendra = \
    #     KalikaKendraModel.find_by_kalika_kendra_name(kalika_kendra_name)[0]
    #     return cls.find_by_student_kalika_kendra_id(kalika_kendra.id)
    #
    # @classmethod
    # def find_by_student_cluster_id(cls, cluster_id):
    #     return cls.query.filter_by(cluster_id=cluster_id).first()
    #
    # @classmethod
    # def find_by_student_cluster_name(cls, cluster_name):
    #     cluster = ClusterModel.find_by_cluster_name(cluster_name)
    #     return cls.find_by_student_cluster_id(cluster.id)
    #
    # @classmethod
    # def find_by_student_contact(cls, contact):
    #     return cls.query.filter_by(contact=contact).first()
    #
    # @classmethod
    # def find_by_student_modified_date(cls, modified_date):
    #     return cls.query.filter_by(modified_date=modified_date).first()
    #
    # @classmethod
    # def find_by_student_register_date(cls, register_date):
    #     return cls.query.filter_by(register_date=register_date).first()
    #
    # @classmethod
    # def find_by_student_dob(cls, dob):
    #     return cls.query.filter_by(dob=dob).first()
    #
    # @classmethod
    # def find_by_student_father_name(cls, father_name):
    #     return cls.query.filter_by(father_name=father_name).first()
    #
    # @classmethod
    # def find_by_student_mother_name(cls, mother_name):
    #     return cls.query.filter_by(mother_name=mother_name).first()
    #
    # @classmethod
    # def find_by_student_father_occupation(cls, father_occupation):
    #     return cls.query.filter_by(father_occupation=father_occupation).first()
    #
    # @classmethod
    # def find_by_student_mother_occupation(cls, mother_occupation):
    #     return cls.query.filter_by(mother_occupation=mother_occupation).first()
    #
    # @classmethod
    # def find_by_student_isactive(cls, isactive):
    #     return cls.query.filter_by(isactive=isactive).first()
    #
    # @classmethod
    # def find_by_student_modified_by(cls, modified_by):
    #     return cls.query.filter_by(modified_by=modified_by).first()

    def set_attribute(self, payload):
        cols = ['student_name', 'gender', 'aadhar',
                'dob', 'class_std', 'father_name',
                'father_occupation', 'mother_name',
                'mother_occupation', 'contact', 'isactive',
                'register_date', 'modified_date', 'modified_by']
        for col in cols:
            if col in payload.keys():
                setattr(self, col, payload[col])
        if 'cluster_name' in payload.keys():
            cluster = ClusterModel.find_by_cluster_name(
                payload['cluster_name'])
            if not cluster:
                return {
                           "message": f"Cluster name not found for the student"}, 401
            self.cluster_id = cluster.id
        if 'kalika_kendra_name' in payload.keys():
            kalika_kendra = KalikaKendraModel.find_by_kalika_kendra_name(
                payload['kalika_kendra_name'])
            if not kalika_kendra:
                return {
                           "message": f"Kalika Kendra name not found for the student"}, 401
            self.kalika_kendra_id = cluster.id

    def save_to_db(self):
        print(self.json())
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
