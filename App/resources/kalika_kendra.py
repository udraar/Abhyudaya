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
from models.kalika_kendra import KalikaKendraModel
from models.cluster import ClusterModel

_kalika_kendra_parser  = reqparse.RequestParser()
_kalika_kendra_parser.add_argument('kalika_kendra_name',
                             required=True,
                             type=str,
                             store_missing=False)
_kalika_kendra_parser.add_argument('cluster_name',
                             type=str,
                             store_missing=False)
_kalika_kendra_parser.add_argument('isactive',
                             type=str,
                             store_missing=False,
                             help="If active flag. Default 1.")
_kalika_kendra_parser.add_argument('isdeprecated',
                             type=str,
                             store_missing=False,
                             help="If depricated flag. Default 0.")
class KalikaKendraList(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'User not authorized to view'}, 401
        data = request.args
        kalika_kendras = KalikaKendraModel.find_by_any(**data)
        if kalika_kendras:
            resp = []
            for kalika_kendra in kalika_kendras:
                resp.append(kalika_kendra.json())
            return resp
        else:
            return {'message': 'Kalika Kendra not found'}

class KalikaKendra(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'User not authorized to view'}, 401
        data = request.args
        # data = _kalika_kendra_parser.parse_args()
        print(data)
        kalika_kendra_name = data.get("kalika_kendra_name")
        cluster_name = data.get("cluster_name")
        cluster_id = data.get("cluster_id")
        kalika_kendra_id = data.get("kalika_kendra_id")
        if kalika_kendra_id:
            kalika_kendras = KalikaKendraModel.find_by_kalika_kendra_id(kalika_kendra_id)
        elif kalika_kendra_name:
            kalika_kendras = KalikaKendraModel.find_by_kalika_kendra_name(kalika_kendra_name)
        elif cluster_name:
            kalika_kendras = KalikaKendraModel.find_by_cluster_name(cluster_name)
        elif cluster_id:
            kalika_kendras = KalikaKendraModel.find_by_cluster_id(cluster_id)
        else:
            return {'message': 'Inadequate keys to fetch data.'}, 401
        if kalika_kendras:
            resp = []
            for kalika_kendra in kalika_kendras:
                resp.append(kalika_kendra.json())
            return resp
        return {'message': 'Kalika Kendra not found'}, 404


    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _kalika_kendra_parser.parse_args()
        kalika_kendra_name = data["kalika_kendra_name"]
        if KalikaKendraModel.find_by_kalika_kendra_name(kalika_kendra_name):
            return {'message': f"A Kalika Kendra with name '{kalika_kendra_name}' already exists."}, 400
        cluster = ClusterModel.find_by_cluster_name(data['cluster_name'])
        if not cluster:
            return {"message": f"Cluster name not found for the Kalika Kendra"}, 401
        kalika_kendra = KalikaKendraModel(**data)
        try:
            kalika_kendra.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the Kalika Kendra. Error: {repr(e)}"}, 500
        return kalika_kendra.json(), 201

    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _kalika_kendra_parser.parse_args()
        kalika_kendra_name = data["kalika_kendra_name"]
        kalika_kendra = KalikaKendraModel.find_by_kalika_kendra_name(kalika_kendra_name)
        if kalika_kendra:
            kalika_kendra.delete_from_db()
            return {'message': 'Kalika Kendra deleted.'}
        return {'message': 'Kalika Kendra not found.'}, 404

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _kalika_kendra_parser.parse_args()
        for key in data.keys():
            if str(data[key]).lower() in ('none', 'null', ''):
                data[key] = None
        kalika_kendra_name = data["kalika_kendra_name"]
        kalika_kendra = KalikaKendraModel.find_by_kalika_kendra_name(kalika_kendra_name)
        if kalika_kendra:
            kalika_kendra.set_attribute(data)
        else:
            kalika_kendra = KalikaKendraModel(**data)
        kalika_kendra.save_to_db()
        return kalika_kendra.json()