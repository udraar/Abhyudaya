from flask_restful import Resource, reqparse
from flask import jsonify
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
from models.student import StudentModel
from models.kalika_kendra import KalikaKendraModel
from models.cluster import ClusterModel
from models.teacher import TeacherModel

_student_parser  = reqparse.RequestParser()
_student_parser.add_argument('student_id', required=False, type=int, store_missing=False)
# _student_parser.add_argument('student_ids', required=False, type=list, store_missing=False)
_student_parser.add_argument('student_name', required=False, type=str, store_missing=False)
_student_parser.add_argument('gender', type=str, store_missing=False)
_student_parser.add_argument('aadhar', type=str, store_missing=False)
_student_parser.add_argument('class_std', type=str, store_missing=False)
_student_parser.add_argument('kalika_kendra_name', type=str, store_missing=False)
_student_parser.add_argument('cluster_name', type=str, store_missing=False)
_student_parser.add_argument('kalika_kendra_id', type=str, store_missing=False)
_student_parser.add_argument('cluster_id', type=str, store_missing=False)
_student_parser.add_argument('father_name', type=str, store_missing=False)
_student_parser.add_argument('father_occupation', type=str, store_missing=False)
_student_parser.add_argument('mother_name', type=str, store_missing=False)
_student_parser.add_argument('mother_occupation', type=str, store_missing=False)
_student_parser.add_argument('contact', type=str, store_missing=False)
_student_parser.add_argument('dob', type=str, store_missing=False)
_student_parser.add_argument('register_date', type=str, store_missing=False)
_student_parser.add_argument('modified_date', type=str, store_missing=False)
_student_parser.add_argument('modified_by', type=str, store_missing=False)
_student_parser.add_argument('isactive', type=str, store_missing=False)

class StudentList(Resource):
    @jwt_required
    def get(self):
        data = dict(request.args)
        print(data)
        claims = get_jwt_claims()
        if not claims['is_admin']:
            if not claims['teacher_code']:
                return {'message': 'User not a teacher. Unauthorized to view student data.'}, 401
            else:
                teacher = TeacherModel.find_by_teacher_code(
                    claims['teacher_code'])
                student_kalika_kendra_id = teacher.kalika_kendra_id
                student_kalika_kendra_name = KalikaKendraModel.find_by_kalika_kendra_id(student_kalika_kendra_id).kalika_kendra_name
            if data.get("kalika_kendra_id"):
                if data.get("kalika_kendra_id") != student_kalika_kendra_id:
                    return {'message': 'User not authorized to view other Kalika Kendra data.'}, 401
            elif data.get("kalika_kendra_name"):
                if data.get("kalika_kendra_name") != student_kalika_kendra_name:
                    return {'message': 'User not authorized to view other Kalika Kendra data.'}, 401
            else:
                data["kalika_kendra_id"] = student_kalika_kendra_id
        students = StudentModel.find_by_student_by_any(**data)
        if students:
            resp = []
            for student in students:
                resp.append(student.json())
            return resp
        else:
            return {'message': 'Students not found'}


class Student(Resource):
    @jwt_required
    def get(self):
        data = request.args
        print(data)
        data = data.to_dict(flat=False)
        claims = get_jwt_claims()

        student_kalika_kendra_name = None
        student_kalika_kendra_id = None
        student_cluster_name = None
        student_cluster_id = None

        if not claims['is_admin']:
            user_email = claims['email']
            if claims['teacher_code']:
                teacher = TeacherModel.find_by_teacher_code(claims['teacher_code'])
                student_kalika_kendra_id = teacher.kalika_kendra_id
                print(student_kalika_kendra_id)
            else:
                return {'message': 'User do not have permission. Contact admin.'}, 401

        student_id = data.get("student_id")
        student_name = data.get("student_name")
        student_aadhar = data.get("aadhar")

        print(data)
        if student_id:
            student = StudentModel.find_by_student_id(student_id)
        if student_aadhar:
            student = StudentModel.find_by_student_aadhar(student_aadhar)
        if student_name:
            student = StudentModel.find_by_student_name(student_name)
        if student:
            print(student.kalika_kendra_id)
            if claims['is_admin'] or (str(student.kalika_kendra_id).__eq__(str(student_kalika_kendra_id))):
                return student.json()
            else:
                return {'message': 'User not authorized to view other Kalika Kendra data.'}, 401
        else:
            return {"message": "Student not found"}, 404

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        data = _student_parser.parse_args()
        dt = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        data["register_date"] = dt
        data["modified_date"] = dt
        data["modified_by"] = claims["email"]
        try:
            print(data)
            student = StudentModel(**data)
            print(student.json())
            student.save_to_db()
        except Exception as ex:
            return {"message": f"Error saving student data. {repr(ex)}"}, 403
        return student.json()


    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _student_parser.parse_args()
        student_id = data.get("student_id")
        student_name = data.get("student_name")
        student_aadhar = data.get("aadhar")
        if student_id:
            student = StudentModel.find_by_student_id(student_id)
        elif student_aadhar:
            student = StudentModel.find_by_student_aadhar(student_aadhar)
        elif student_name:
            student = StudentModel.find_by_student_name(student_name)
        else:
            return {"message": "Missing student key fields"}, 404
        if student:
            student.delete_from_db()
            return {'message': 'Student deleted.'}
        return {'message': 'Student not found.'}, 404

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        data = _student_parser.parse_args()
        for key in data.keys():
            if str(data[key]).lower() in ('none', 'null', ''):
                data[key] = None
        dt = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        data["modified_date"] = dt
        data["modified_by"] = claims["email"]
        student_id = data.get("student_id")
        student_name = data.get("student_name")
        student_aadhar = data.get("aadhar")
        if student_id:
            student = StudentModel.find_by_student_id(student_id)
        elif student_aadhar:
            student = StudentModel.find_by_student_aadhar(student_aadhar)
        elif student_name:
            student = StudentModel.find_by_student_name(student_name)
        else:
            return {"message": "Missing student key fields"}, 404
        try:
            if student:
                student.set_attribute(data)
            else:
                student = StudentModel(**data)
            student.save_to_db()
            return student.json()
        except Exception as ex:
            return {"message": f"Error updating student data. {repr(ex)}"}, 403