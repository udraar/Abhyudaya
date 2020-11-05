from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, jwt_optional, fresh_jwt_required
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from flask import request
from werkzeug.security import safe_str_cmp
from hashlib import md5
# from blacklist import BLACKLIST
from models.cluster import ClusterModel

_cluster_parser  = reqparse.RequestParser()
_cluster_parser.add_argument('cluster_name',
                             required=True,
                             type=str,
                             store_missing=False)
_cluster_parser.add_argument('isactive',
                             type=str,
                             store_missing=False,
                             help="If active flag. Default 1.")
_cluster_parser.add_argument('isdeprecated',
                             type=str,
                             store_missing=False,
                             help="If depricated flag. Default 0.")

class ClusterList(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'User not authorized to view.'}, 401
        data = request.args
        clusters = ClusterModel.find_by_any(**data)
        if clusters:
            resp = []
            for cluster in clusters:
                resp.append(cluster.json())
            return resp
        else:
            return {'message': 'Cluster not found'}

class Cluster(Resource):
    @jwt_required
    def get(self):
        data = request.args
        # data = _cluster_parser.parse_args()
        cluster_name = data["cluster_name"]
        claims = get_jwt_claims()
        if claims['is_admin']:
            cluster = ClusterModel.find_by_cluster_name(cluster_name)
            if cluster:
                return cluster.json()
            return {'message': 'Cluster not found'}, 404
        return {'message': 'User not authorized to view'}

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _cluster_parser.parse_args()
        cluster_name = data["cluster_name"]
        if ClusterModel.find_by_cluster_name(cluster_name):
            return {'message': f"A cluster with name '{cluster_name}' already exists."}, 400
        cluster = ClusterModel(**data)
        try:
            cluster.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the cluster. Error: {repr(e)}"}, 500
        return cluster.json(), 201

    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _cluster_parser.parse_args()
        cluster_name = data["cluster_name"]
        cluster = ClusterModel.find_by_cluster_name(cluster_name)
        if cluster:
            cluster.delete_from_db()
            return {'message': 'Cluster deleted.'}
        return {'message': 'Cluster not found.'}, 404

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _cluster_parser.parse_args()
        for key in data.keys():
            if str(data[key]).lower() in ('none', 'null', ''):
                data[key] = None
        cluster_name = data["cluster_name"]
        cluster = ClusterModel.find_by_cluster_name(cluster_name)
        if cluster:
            cluster.set_attribute(data)
        else:
            cluster = ClusterModel(**data)
        cluster.save_to_db()
        return cluster.json()