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
from models.assessment_category import AssessmentCategoryModel

_assessment_category_parser  = reqparse.RequestParser()
_assessment_category_parser.add_argument('category_id',required=False,type=int,store_missing=False)
_assessment_category_parser.add_argument('category_name',required=False,type=str,store_missing=False)
_assessment_category_parser.add_argument('category_code',type=str,store_missing=False)
_assessment_category_parser.add_argument('subject_id',type=int,store_missing=False)
_assessment_category_parser.add_argument('subject_name',type=str,store_missing=False)
_assessment_category_parser.add_argument('isactive',type=str,store_missing=False)

class AssessmentCategoryList(Resource):
    @jwt_required
    def get(self):
        data = request.args
        assessment_categories = AssessmentCategoryModel.find_assessment_category_by_any(**data)
        if assessment_categories:
            resp = []
            for assessment_category in assessment_categories:
                resp.append(assessment_category.json())
            return resp
        else:
            {'message': 'Assessment categories not found'}, 404

class AssessmentCategory(Resource):
    @jwt_required
    def get(self):
        data = request.args
        # data = _assessment_category_parser.parse_args()
        if 'category_id' in data.keys():
            assessment_category = AssessmentCategoryModel.find_by_category_id(data['category_id'])
            if assessment_category:
                return assessment_category.json(), 200
            else:
                return {'message': "Assessment category id not found"}, 404
        if 'category_name' in data.keys():
            assessment_category = AssessmentCategoryModel.find_by_category_name(data['category_name'])
            if assessment_category:
                return assessment_category.json(), 200
            else:
                return {'message': "Assessment category name not found"}, 404
        if 'subject_name' in data.keys():
            assessment_category = AssessmentCategoryModel.find_by_subject_name(data['subject_name'])
            if assessment_category:
                return assessment_category.json()
            else:
                return {'message': 'Invalid subject name.'}, 404

        assessment_categories = AssessmentCategoryModel.find_assessment_category_by_any(**data)
        if assessment_categories:
            resp = []
            for assessment_category in assessment_categories:
                resp.append(assessment_category.json())
            return resp, 200
        return {'message': 'Assessment category not found'}, 404

    @jwt_required
    def post(self):
        data = _assessment_category_parser.parse_args()
        assessment_categories = AssessmentCategoryModel.find_assessment_category_by_any(
            **data)
        if assessment_categories:
            return {'message': f"Assessment category already exists with the details provided."}, 400
        if 'category_name' not in data.keys() or 'category_code' not in data.keys() or 'subject_id' not in data.keys():
            return {'message': f"Not all mandatory columns(Category Name, Category Code and Subject ID) provided."}, 401
        assessment_category = AssessmentCategoryModel(**data)
        try:
            assessment_category.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the assessment category details. Error: {repr(e)}"}, 500
        return assessment_category.json(), 201

    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _assessment_category_parser.parse_args()
        assessment_categories = AssessmentCategoryModel.find_assessment_category_by_any(
            **data)
        if assessment_categories:
            for assessment_category in assessment_categories:
                assessment_category.delete_from_db()
            return {'message': 'Assessment categories deleted.'}
        return {'message': 'Assessment categories not found.'}, 404

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _assessment_category_parser.parse_args()
        for key in data.keys():
            if str(data[key]).lower() in ('none', 'null', ''):
                data[key] = None
        try:
            assessment_category_id = data["category_id"]
            assessment_category = AssessmentCategoryModel.find_by_category_id(assessment_category_id)
            if assessment_category:
                assessment_category.set_attribute(data)
                assessment_category.save_to_db()
            return assessment_category.json()
        except Exception as e:
            return {'message': f"Assesment category could not be found. {repr(e)}"}, 404