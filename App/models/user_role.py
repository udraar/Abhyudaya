from db import db
from models.organization import OrganizationModel


class UserRoleModel(db.Model):
    __tablename__ = "user_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(200))
    role_desc = db.Column(db.String(200))
    isactive = db.Column(db.Integer)

    def __init__(self, role_name, organization_id=None, role_desc=None,
                 organization_name=None, isactive=0):
        self.role_name = role_name
        self.role_desc = role_desc
        self.isactive = isactive

    def json(self):
        return {'role_id': self.id,
                'role_name': self.role_name,
                'role_desc': self.role_desc,
                'isactive': self.isactive}

    @classmethod
    def find_by_any(cls, **kwargs):
        filter_str = 'cls.query'
        cols = ['isactive', 'role_name', 'role_desc']
        if 'isactive' in kwargs.keys():
            filter_str = filter_str + '.filter_by(isactive="' + str(
                kwargs['isactive']) + '")'
        if 'role_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(role_name="' + str(
                kwargs['role_name']) + '")'
        if 'role_desc' in kwargs.keys():
            filter_str = filter_str + '.filter_by(role_desc="' + str(
                kwargs['role_desc']) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)
        return cls.query.all()

    @classmethod
    def find_by_role_desc(cls, role_desc):
        return cls.query.filter_by(role_desc=role_desc).first()

    @classmethod
    def find_by_role_name(cls, role_name):
        return cls.query.filter_by(role_name=role_name).first()

    @classmethod
    def find_by_role_id(cls, role_id):
        return cls.query.filter_by(id=role_id).first()

    @classmethod
    def find_by_isactive(cls, isactive):
        return cls.query.filter_by(isactive=isactive).first()

    def set_attribute(self, payload):
        cols = ['isactive', 'role_name', 'role_desc']
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
