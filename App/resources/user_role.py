from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, \
    jwt_optional, fresh_jwt_required
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
from models.organization import OrganizationModel
from models.user_role import UserRoleModel

_user_role_parser = reqparse.RequestParser()
_user_role_parser.add_argument('role_id', required=False, type=int,
                               store_missing=False)
_user_role_parser.add_argument('role_name', required=False, type=str,
                               store_missing=False)
_user_role_parser.add_argument('role_desc', required=False, type=str,
                               store_missing=False)
_user_role_parser.add_argument('isactive', type=str, store_missing=False,
                               help="If depricated flag. Default 0.")


class UserRole(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'User not authorized to view'}
        try:
            data = request.args
            role_id = data.get("role_id")
            role_desc = data.get("role_desc")
            role_name = data.get("role_name")
            if role_id:
                roles = UserRoleModel.find_by_role_id(role_id)
            elif role_name:
                roles = UserRoleModel.find_by_role_name(role_name)
            elif role_desc:
                roles = UserRoleModel.find_by_role_desc(role_desc)
            else:
                roles = UserRoleModel.find_all()
        except:
            roles = UserRoleModel.find_all()
        finally:
            if len(roles) > 0:
                resp = []
                for role in roles:
                    resp.append(role.json())
                return resp, 200
            return {'message': 'Role not found'}, 404

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if not claims['is_super_admin']:
            return {'message': 'Super Admin privilege required.'}, 412
        data = _user_role_parser.parse_args()
        try:
            role_name = data["role_name"]
        except Exception as e:
            return {'message': f"Role name missing. {repr(e)}"}

        if UserRoleModel.find_by_role_name(role_name):
            return {
                       'message': f"Role name already exists."}, 400
        user_role = UserRoleModel(**data)
        try:
            user_role.save_to_db()
        except Exception as e:
            return {
                       "message": f"An error occurred inserting the role. Error: {repr(e)}"}, 500
        return user_role.json(), 201

    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if not claims['is_super_admin']:
            return {'message': 'Super Admin privilege required.'}, 412
        data = _user_role_parser.parse_args()
        try:
            role_name = data["role_name"]
        except Exception as e:
            return {"message": f"Role name missing."}
        user_role = UserRoleModel.find_by_role_name(role_name)[0]
        if user_role:
            user_role.delete_from_db()
            return {'message': 'Role name deleted.'}, 200
        return {'message': 'Role name not found.'}, 404

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        if not claims['is_super_admin']:
            return {'message': 'Super Admin privilege required.'}, 412
        data = _user_role_parser.parse_args()
        for key in data.keys():
            if str(data[key]).lower() in ('none', 'null', ''):
                data[key] = None
        try:
            role_name = data["role_name"]
        except Exception as e:
            return {"message": f"Role name required. {repr(e)}"}
        user_role = UserRoleModel.find_by_role_name(role_name)[0]
        if user_role:
            user_role.set_attribute(data)
        else:
            user_role = UserRoleModel(**data)
        user_role.save_to_db()
        return user_role.json(), 201
