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
from models.organization import OrganizationModel

_organization_parser  = reqparse.RequestParser()
_organization_parser.add_argument('organization_id',
                             required=False,
                             type=int,
                             store_missing=False)
_organization_parser.add_argument('organization_name',
                             required=False,
                             type=str,
                             store_missing=False)
_organization_parser.add_argument('organization_desc',
                             type=str,
                             store_missing=False,
                             help="If active flag. Default 1.")
_organization_parser.add_argument('isactive',
                             type=str,
                             store_missing=False,
                             help="If depricated flag. Default 0.")

class Organization(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'User not authorized to view'}
        try:
            # data = _organization_parser.parse_args()
            data = request.args
            organization_name = data.get("organization_name")
            organization_desc = data.get("organization_desc")
            organization_id = data.get("organization_id")
            # isactive = data.get("isactive")
            if organization_id:
                organizations = OrganizationModel.find_by_organization_id(organization_id)
            elif organization_name:
                organizations = OrganizationModel.find_by_organization_name(organization_name)
            elif organization_desc:
                organizations = OrganizationModel.find_by_organization_desc(organization_desc)
            else:
                organizations = OrganizationModel.find_all()
        except:
            organizations = OrganizationModel.find_all()
        finally:
            if len(organizations)>0:
                resp = []
                for organization in organizations:
                    resp.append(organization.json())
                return resp, 200
            return {'message': 'Organization not found'}, 404

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if not claims['is_super_admin']:
            return {'message': 'Super Admin privilege required.'}, 412
        data = _organization_parser.parse_args()
        try:
            organization_name = data["organization_name"]
        except Exception as e:
            return {'message': f"Organization Name missing. {repr(e)}"}

        if OrganizationModel.find_by_organization_name(organization_name):
            return {'message': f"An Organization with name '{organization_name}' already exists."}, 400
        organization = OrganizationModel(**data)
        try:
            organization.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the organization. Error: {repr(e)}"}, 500
        return organization.json(), 201

    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if not claims['is_super_admin']:
            return {'message': 'Super Admin privilege required.'}, 412
        data = _organization_parser.parse_args()
        try:
            organization_name = data["organization_name"]
        except Exception as e:
            return {"message": f"Organization name missing. {organization_name}"}
        organization = OrganizationModel.find_by_organization_name(organization_name)[0]
        if organization:
            organization.delete_from_db()
            return {'message': 'Organization deleted.'}, 200
        return {'message': 'Organization not found.'}, 404

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        if not claims['is_super_admin']:
            return {'message': 'Super Admin privilege required.'}, 412
        data = _organization_parser.parse_args()
        for key in data.keys():
            if str(data[key]).lower() in ('none', 'null', ''):
                data[key] = None
        try:
            organization_name = data["organization_name"]
        except Exception as e:
            return {"message": f"Organization name required. {repr(e)}"}
        organization = OrganizationModel.find_by_organization_name(organization_name)[0]
        if organization:
            organization.set_attribute(data)
        else:
            organization = OrganizationModel(**data)
        organization.save_to_db()
        return organization.json(), 201