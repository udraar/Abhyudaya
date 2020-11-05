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
from datetime import datetime
# from blacklist import BLACKLIST
from models.teacher import TeacherModel
from models.kalika_kendra import KalikaKendraModel
from models.cluster import ClusterModel

_teacher_parser  = reqparse.RequestParser()
_teacher_parser.add_argument('teacher_id', required=False, type=int, store_missing=False)
_teacher_parser.add_argument('teacher_name', required=False, type=str, store_missing=False)
_teacher_parser.add_argument('teacher_code', type=str, required=False, store_missing=False)
_teacher_parser.add_argument('cluster_name', type=str, store_missing=False)
_teacher_parser.add_argument('cluster_id', type=str, store_missing=False)
_teacher_parser.add_argument('kalika_kendra_name', type=str, store_missing=False)
_teacher_parser.add_argument('kalika_kendra_id', type=str, store_missing=False)
_teacher_parser.add_argument('isactive', type=str, store_missing=False)

class Teacher(Resource):
    @jwt_required
    def get(self):
        data = request.args
        teacher_id = data.get("teacher_id")
        teacher_name = data.get("teacher_name")
        teacher_code = data.get("teacher_code")
        
        if teacher_id:
            teacher = TeacherModel.find_by_teacher_id(teacher_id)
        if teacher_code:
            teacher = TeacherModel.find_by_teacher_code(teacher_code)
        if teacher_name:
            teacher = TeacherModel.find_by_teacher_name(teacher_name)
            
        if teacher:
            return teacher.json()
        else:
            return {"message": "Teacher not found"}, 404

    @jwt_required
    def post(self):
        data = _teacher_parser.parse_args()
        claims = get_jwt_claims()
        if not claims.get('is_admin'):
            user_email = claims.get('email')
            return {'message': 'Admin privilege required.'}, 401
        try:
            dt = datetime.now()
            data["creation_date"] = dt
            data["modified_date"] = dt
            print(f"data: {data}")
            teacher = TeacherModel(**data)
            teacher.save_to_db()
        except KeyError as ex:
            return {"message": f"Error saving teacher data. Missing key fields. {repr(ex)}"}, 403
        except Exception as ex:
            return {"message": f"Error saving teacher data. {repr(ex)}"}, 403
        return teacher.json()


    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _teacher_parser.parse_args()
        teacher_id = data.get("teacher_id")
        teacher_name = data.get("teacher_name")
        teacher_code = data.get("teacher_code")
        if teacher_id:
            teacher = TeacherModel.find_by_teacher_id(teacher_id)
        elif teacher_code:
            teacher = TeacherModel.find_by_teacher_code(teacher_code)
        else:
            return {"message": "Missing teacher key fields"}, 404
        if teacher:
            teacher.delete_from_db()
            return {'message': 'Teacher deleted.'}
        return {'message': 'Teacher not found.'}, 404

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _teacher_parser.parse_args()
        for key in data.keys():
            if str(data[key]).lower() in ('none', 'null', ''):
                data[key] = None
        teacher_id = data.get("teacher_id")
        teacher_name = data.get("teacher_name")
        teacher_code = data.get("teacher_code")
        if teacher_id:
            teacher = TeacherModel.find_by_teacher_id(teacher_id)
        elif teacher_code:
            teacher = TeacherModel.find_by_teacher_code(teacher_code)
        elif teacher_name:
            teacher = TeacherModel.find_by_teacher_name(teacher_name)
        else:
            return {"message": "Missing teacher key fields"}, 404
        try:
            data['modified_date'] = datetime.now()
            if teacher:
                teacher.set_attribute(data)
            else:
                teacher = TeacherModel(**data)
            teacher.save_to_db()
            return teacher.json()
        except Exception as ex:
            return {"message": f"Error updating teacher data. {repr(ex)}"}, 403

class TeacherList(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = request.args
        teachers = TeacherModel.find_by_any(**data)
        if teachers:
            resp = []
            for teacher in teachers:
                resp.append(teacher.json())
            return resp
        else:
            return {'message': 'Teachers not found'}
        