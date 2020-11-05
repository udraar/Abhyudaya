from db import db
from models.cluster import ClusterModel
# from models.student import StudentModel

class KalikaKendraModel(db.Model):
    __tablename__ = "kalika_kendra"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kalika_kendra_name = db.Column(db.String(200))
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
    isactive = db.Column(db.Integer)
    isdeprecated = db.Column(db.Integer)

    # students = db.relationship('StudentModel', backref='kalika_kendra')

    def __init__(self, kalika_kendra_name, cluster_name, isactive=1, isdeprecated=0):
        self.kalika_kendra_name = kalika_kendra_name
        cluster = ClusterModel.find_by_cluster_name(cluster_name)
        if not cluster:
            return {"message": f"Cluster name not found for the Kalika Kendra"}, 401
        self.cluster_id = cluster.id
        self.isactive = isactive
        self.isdeprecated = isdeprecated

    def json(self):
        return {'kalika_kendra_name': self.kalika_kendra_name, 'cluster_id': self.cluster_id,
                'cluster_name': ClusterModel.find_by_cluster_id(self.cluster_id).cluster_name,
                'isactive': self.isactive,
                'isdeprecated': self.isdeprecated,
                "id":self.id
                }

    @classmethod
    def find_by_any(cls, **kwargs):
        filter_str = 'cls.query'
        cols = ['isactive', 'isdeprecated', 'cluster_name', 'cluster_id']
        if 'cluster_id' in kwargs.keys():
            filter_str = filter_str +  '.filter_by(cluster_id="' + str(
                kwargs['cluster_id']) + '")'
        if 'cluster_name' in kwargs.keys():
            cluster = ClusterModel.find_by_cluster_name(kwargs['cluster_name'])
            if cluster:
                cluster_id = cluster.id
                filter_str = filter_str +  '.filter_by(cluster_id="' + str(cluster_id) + '")'
        if 'isactive' in kwargs.keys():
            filter_str = filter_str +  '.filter_by(isactive="' + str(
                kwargs['isactive']) + '")'
        if 'isdeprecated' in kwargs.keys():
            filter_str = filter_str +  '.filter_by(isdeprecated="' + str(
                kwargs['isdeprecated']) + '")'
        filter_str = filter_str + '.all()'
        return eval(filter_str)

    @classmethod
    def find_by_kalika_kendra_name(cls, kalika_kendra_name):
        return cls.query.filter_by(kalika_kendra_name=kalika_kendra_name).first()

    @classmethod
    def find_by_cluster_name(cls, cluster_name):
        cluster = ClusterModel.find_by_cluster_name(cluster_name)
        if cluster:
            return cls.query.filter_by(cluster_id=cluster.id).first()

    @classmethod
    def find_by_cluster_id(cls, cluster_id):
        return cls.query.filter_by(cluster_id=cluster_id).first()

    @classmethod
    def find_by_kalika_kendra_id(cls, kalika_kendra_id):
        return cls.query.filter_by(id=kalika_kendra_id).first()

    def set_attribute(self, payload):
        cols = ['isactive', 'isdeprecated']
        for col in cols:
            if col in payload.keys():
                setattr(self, col, payload[col])
        if 'cluster_name' in payload.keys():
            cluster = ClusterModel.find_by_cluster_name(payload['cluster_name'])
            if not cluster:
                return {"message": f"Cluster name not found for the Kalika Kendra"}, 401
            self.cluster_id = cluster.id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()