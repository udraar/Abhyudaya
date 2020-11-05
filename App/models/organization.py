from db import db


class OrganizationModel(db.Model):
    __tablename__ = "organization"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_name = db.Column(db.String(200))
    organization_desc = db.Column(db.String(200))
    isactive = db.Column(db.Integer)

    def __init__(self, organization_name, organization_desc, isactive=0):
        self.organization_name = organization_name
        self.organization_desc = organization_desc
        self.isactive = isactive

    def json(self):
        return {'organization_id': self.id,
                'organization_name': self.organization_name,
                'organization_desc': self.organization_desc,
                'isactive': self.isactive}

    @classmethod
    def find_by_any(cls, **kwargs):
        filter_str = 'cls.query'
        cols = ['isactive', 'organization_desc']
        if 'isactive' in kwargs.keys():
            filter_str = filter_str + '.filter_by(isactive="' + str(
                kwargs['isactive']) + '")'
        if 'organization_desc' in kwargs.keys():
            filter_str = filter_str + '.filter_by(organization_desc="' + str(
                kwargs['organization_desc']) + '")'
        if 'organization_name' in kwargs.keys():
            filter_str = filter_str + '.filter_by(organization_name="' + str(
                kwargs['organization_name']) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    @classmethod
    def find_by_organization_name(cls, organization_name):
        return cls.query.filter_by(organization_name=organization_name).first()

    @classmethod
    def find_by_organization_id(cls, organization_id):
        return cls.query.filter_by(id=organization_id).first()

    @classmethod
    def find_by_organization_desc(cls, organization_desc):
        return cls.query.filter_by(organization_desc=organization_desc).first()

    @classmethod
    def find_by_isactive(cls, isactive):
        return cls.query.filter_by(isactive=isactive).first()

    def set_attribute(self, payload):
        cols = ['isactive', 'organization_desc', 'organization_name']
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
