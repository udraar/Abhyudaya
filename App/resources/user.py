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

from models.user import UserModel


_user_parser  = reqparse.RequestParser()
_user_parser.add_argument('email', required=True, type=str, store_missing=False)
_user_parser.add_argument('password', type=str, store_missing=False)
_user_parser.add_argument('status', type=str, store_missing=False)
_user_parser.add_argument('first_name', type=str, store_missing=False)
_user_parser.add_argument('last_name', type=str, store_missing=False)
_user_parser.add_argument('gender', type=str, store_missing=False)
_user_parser.add_argument('mobile', type=str, store_missing=False)
_user_parser.add_argument('user_role_name', type=str, store_missing=False)
_user_parser.add_argument('organization_name', type=str, store_missing=False)
_user_parser.add_argument('user_role_id', type=int, store_missing=False)
_user_parser.add_argument('organization_id', type=int, store_missing=False)
_user_parser.add_argument('designation', type=str, store_missing=False)
_user_parser.add_argument('image', type=str, store_missing=False)
_user_parser.add_argument('type', type=str, store_missing=False)
_user_parser.add_argument('authtoken', type=str, store_missing=False)
_user_parser.add_argument('teacher_code', type=str, store_missing=False)
_user_parser.add_argument('bloodgroup', type=str, store_missing=False)

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        print(data)
        user = UserModel.find_by_email(data['email'])
        if user:
            print(user.json())
            return {"message": "A user with that email already exists"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully."}, 201


class User(Resource):

    @jwt_required
    def get(self):
        data = request.args
        email = data.get("email")
        claims = get_jwt_claims()
        user_email = claims['email']
        if claims['is_admin'] or email == user_email :
            user = UserModel.find_by_email(email, False)
            if user:
                return user.json()
            return {'message': 'User not found'}, 404
        return {'message': 'User not authorized to view'}

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _user_parser.parse_args()
        print(f"data: {data}")
        email = data["email"]
        if UserModel.find_by_email(email):
            return {'message': f"A user with email {email} already exists."}, 400

        # user = UserModel(email, **data)
        user = UserModel(**data)
        try:
            user.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the user. Error: {repr(e)}"}, 500
        return user.json(), 201

    @jwt_required
    def delete(self):
        data = _user_parser.parse_args()
        email = data["email"]
        claims = get_jwt_claims()
        user_email = claims['email']
        print(f"user: {email}, user_email: {user_email}")
        if claims['is_admin']:
            user = UserModel.find_by_email(email)
            if user:
                user.delete_from_db()
                return {'message': 'User deleted.'}
            else:
                return {'message': 'User not found'}, 404
        return {'message': 'User not authorized to delete'}

    @jwt_required
    def put(self):
        data = _user_parser.parse_args()
        for key in data.keys():
            if str(data[key]).lower() in ('none', 'null', ''):
                data[key] = None
        email = data["email"]
        claims = get_jwt_claims()
        user_email = claims['email']
        print(data)
        if email == user_email or claims['is_admin']:
            user = UserModel.find_by_email(email)
            if user:
                user.set_attribute(data)
                user.save_to_db()
                return user.json()
            else:
                return {'message': 'User not found'}, 404
        return {'message': 'User not authorized to update'}
    
class UserList(Resource):
    @jwt_required
    def get(self):
        data = request.args
        claims = get_jwt_claims()
        if claims['is_admin']:
            users = UserModel.find_by_any(**data)
            if users:
                resp = []
                for user in users:
                    resp.append(user.json())
                return resp
            else:
                {'message': 'No user found'}, 404
        else:
            {'message': 'User not authorized'}, 401


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_email(data['email'])

        if user and safe_str_cmp(user.password, md5(data['password'].encode('UTF-8')).hexdigest()):
            # identity= is what the identity() function did in security.py—now stored in the JWT
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid Credentials!"}, 401