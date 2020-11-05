import enum
import json
from sqlalchemy import Integer, Enum
from hashlib import md5

from db import db
from models.organization import OrganizationModel
from models.user_role import UserRoleModel


class StatusEnum(enum.Enum):
    active = 'active'
    inactive = 'inactive'


class GenderEnum(enum.Enum):
    male = 'male'
    female = 'female'


class DesignationEnum(enum.Enum):
    abhyudaya = 'Abhyudaya'
    senior_teacher = 'Senior Teacher'
    kalika_kendra_teacher = 'Kalika kendra Teacher'
    volunteer = 'Volunteer'


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    status = db.Column(Enum(StatusEnum))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    mobile = db.Column(db.String(50))
    designation = db.Column(db.String(50))
    image = db.Column(db.String(250))
    type = db.Column(db.String(250), default='general')
    authtoken = db.Column(db.String(250))
    teacher_code = db.Column(db.String(50))
    bloodgroup = db.Column(db.String(10))
    organization_id = db.Column(db.Integer)
    user_role_id = db.Column(db.Integer)

    def __init__(self, email, password, **kwargs):
        self.email = email
        # self.password = md5(str(password).encode('UTF-8'))
        self.password = md5(str(password).encode('UTF-8')).hexdigest()
        cols = ['status', 'first_name', 'last_name', 'gender', 'mobile', \
                'designation', 'image', 'type', 'authtoken', \
                'teacher_code', 'bloodgroup', 'organization_id',
                'user_role_id']
        self.status = StatusEnum.active
        self.designation = 'Volunteer'  # DesignationEnum.volunteer
        for col in cols:
            if col in kwargs.keys():
                setattr(self, col, kwargs[col])
        if not kwargs.get('user_role_id'):
            self.user_role_id = 5
        else:
            self.user_role_id = kwargs["user_role_id"]
        if self.user_role_id == 1:
            self.organization_id = None
        elif 'organization_id' not in kwargs.keys() or kwargs["organization_id"] == '':

            self.organization_id = 1
        else:
            self.organization_id = kwargs["organization_id"]

    def json(self):
        return {"email": self.email,  # "status": self.status, \
                "first_name": self.first_name, "last_name": self.last_name, \
                "gender": self.gender, "mobile": self.mobile, \
                "organization_id": self.organization_id, "organization_name":
                    OrganizationModel.find_by_organization_id(
                        self.organization_id).organization_name if OrganizationModel.find_by_organization_id(
                        self.organization_id) else None,
                "user_role_id": self.user_role_id, "user_role_name":
                    UserRoleModel.find_by_role_id(self.user_role_id).role_name if UserRoleModel.find_by_role_id(self.user_role_id) else None, \
                "image": self.image, "type": self.type, \
                "authtoken": self.authtoken, "teacher_code": self.teacher_code, \
                "bloodgroup": self.bloodgroup}

    @classmethod
    def find_by_email(cls, email, isactive=True):
        if isactive:
            return cls.query.filter_by(email=email).filter_by(
                status='active').first()
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).filter_by(status='active').first()

    @classmethod
    def find_by_any(cls, **kwargs):
        cols = ['id', 'email', 'status', 'first_name', 'last_name', 
                'gender', 'mobile', 'designation', 'type', 'teacher_code',
                'bloodgroup', 'organization_id', 'user_role_id', 
                'organization_name', 'user_role_name']
        filter_str = 'cls.query'
        if 'id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(_id="' + str(
                kwargs['id']) + '")'
        if 'email' in kwargs.keys():
            filter_str = filter_str + '.filter_by(email="' + str(
                kwargs['email']) + '")'
        if 'status' in kwargs.keys():
            filter_str = filter_str + '.filter_by(status="' + str(
                kwargs['status']) + '")'
        if 'first_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(first_name="' + str(
                kwargs['first_name']) + '")'
        if 'last_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(last_name="' + str(
                kwargs['last_name']) + '")'
        if 'gender' in kwargs.keys():
            filter_str = filter_str + '.filter_by(gender="' + str(
                kwargs['gender']) + '")'
        if 'mobile' in kwargs.keys():
            filter_str = filter_str + '.filter_by(mobile="' + str(
                kwargs['mobile']) + '")'
        if 'designation' in kwargs.keys():
            filter_str = filter_str + '.filter_by(designation="' + str(
                kwargs['designation']) + '")'
        if 'type' in kwargs.keys():
            filter_str = filter_str + '.filter_by(type="' + str(
                kwargs['type']) + '")'
        if 'teacher_code' in kwargs.keys():
            filter_str = filter_str + '.filter_by(teacher_code="' + str(
                kwargs['teacher_code']) + '")'
        if 'bloodgroup' in kwargs.keys():
            filter_str = filter_str + '.filter_by(bloodgroup="' + str(
                kwargs['bloodgroup']) + '")'
        if 'organization_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(organization_id="' + str(
                kwargs['organization_id']) + '")'
        if 'user_role_id' in kwargs.keys():
            filter_str = filter_str + '.filter_by(user_role_id="' + str(
                kwargs['user_role_id']) + '")'
        if 'user_role_name' in kwargs.keys():
            user_role = UserRoleModel.find_by_role_name(kwargs['user_role_name'])
            if user_role:
                user_role_id = user_role[0].id
                filter_str = filter_str + '.filter_by(user_role_id="' + str(user_role_id) + '")'
        if 'organization_name' in kwargs.keys():
            organization = OrganizationModel.find_by_organization_name(kwargs['organization_name'])
            if organization:
                organization_id = organization[0].id
                filter_str = filter_str + '.filter_by(organization_id="'\
                             + str(organization_id) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    def set_attribute(self, payload):
        cols = ['status', 'first_name', 'last_name', 'gender', 'password',
                'mobile', 'designation', 'image', 'type',
                'authtoken', 'teacher_code', 'bloodgroup', 'user_role_id',
                'organization_id']
        for col in cols:
            if col in payload.keys():
                setattr(self, col, payload[col])
        if payload.get('user_role_name'):
            user_role = UserRoleModel.find_by_role_name(payload['user_role_name'])
            self.user_role_id = user_role.id
        if payload.get('organization_name'):
            organization = OrganizationModel.find_by_organization_name(payload['organization_name'])
            self.organization_id = organization.id
        if 'password' in payload.keys():
            self.password = md5(
                str(payload['password']).encode('UTF-8')).hexdigest()

    def save_to_db(self):

        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
