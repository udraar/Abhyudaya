from db import db

class ClusterModel(db.Model):
    __tablename__ = "cluster"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cluster_name = db.Column(db.String(200))
    isactive = db.Column(db.Integer)
    isdeprecated = db.Column(db.Integer)

    def __init__(self, cluster_name, isactive=1, isdeprecated=0):
        self.cluster_name = cluster_name
        self.isactive = isactive
        self.isdeprecated = isdeprecated

    def json(self):
        return {'cluster_name': self.cluster_name, 'isactive': self.isactive, 'isdeprecated': self.isdeprecated}

    @classmethod
    def find_by_cluster_name(cls, cluster_name):
        return cls.query.filter_by(cluster_name=cluster_name).first()

    @classmethod
    def find_by_cluster_id(cls, cluster_id):
        return cls.query.filter_by(id=cluster_id).first()

    @classmethod
    def find_by_any(cls, **kwargs):
        filter_str = 'cls.query'
        cols = ['isactive', 'isdeprecated']
        if 'isactive' in kwargs.keys():
            filter_str = filter_str +  '.filter_by(isactive="' + str(
                kwargs['isactive']) + '")'
        if 'isdeprecated' in kwargs.keys():
            filter_str = filter_str +  '.filter_by(isdeprecated="' + str(
                kwargs['isdeprecated']) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    def set_attribute(self, payload):
        cols = ['isactive', 'isdeprecated']
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