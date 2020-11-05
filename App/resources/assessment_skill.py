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
from models.assessment_skill import AssessmentSkillModel

_assessment_skill_parser = reqparse.RequestParser()
_assessment_skill_parser.add_argument('skill_id', type=int,
                                      store_missing=False)
_assessment_skill_parser.add_argument('skill_name', type=str,
                                      store_missing=False)
_assessment_skill_parser.add_argument('skill_code', type=str,
                                      store_missing=False)
_assessment_skill_parser.add_argument('subject_id', type=int,
                                      store_missing=False)
_assessment_skill_parser.add_argument('subject_name', type=str,
                                      store_missing=False)
_assessment_skill_parser.add_argument('category_id', type=int,
                                      store_missing=False)
_assessment_skill_parser.add_argument('category_name', type=str,
                                      store_missing=False)
_assessment_skill_parser.add_argument('isactive', type=str,
                                      store_missing=False)

class AssessmentSkillList(Resource):
    @jwt_required
    def get(self):
        data = request.args
        skills = AssessmentSkillModel.find_assessment_skill_by_any(**data)
        if skills:
            resp = []
            for skill in skills:
                resp.append(skill.json())
            return resp
        else:
            {'message': 'Skills not found'}, 404


class AssessmentSkill(Resource):
    @jwt_required
    def get(self):
        # data = _assessment_skill_parser.parse_args()
        data = request.args
        if 'skill_id' in data.keys():
            assessment_skill = AssessmentSkillModel.find_by_skill_id(
                data['skill_id'])
            if assessment_skill:
                return assessment_skill.json()
            else:
                return {'message': "Assessment skill id not found"}, 404
        if 'skill_name' in data.keys():
            assessment_skill = AssessmentSkillModel.find_by_skill_name(
                data['skill_name'])
            if assessment_skill:
                return assessment_skill.json()
            else:
                return {'message': "Assessment skill id not found"}, 404
        if 'subject_name' in data.keys():
            assessment_skill = AssessmentSkillModel.find_by_subject_name(
                data['subject_name'])
            if assessment_skill:
                return assessment_skill.json()
            else:
                return {'message': 'Invalid subject name.'}, 404
        if 'category_name' in data.keys():
            assessment_skill = AssessmentSkillModel.find_by_category_name(
                data['category_name'])
            if assessment_skill:
                return assessment_skill.json()
            else:
                return {'message': 'Invalid category name.'}, 404


    @jwt_required
    def post(self):
        data = _assessment_skill_parser.parse_args()
        assessment_skills = AssessmentSkillModel.find_assessment_skill_by_any(
            **data)
        if assessment_skills:
            return {'message':
                        f"Assessment skill already exists with the details provided."}, 400
        if 'skill_name' not in data.keys() or 'skill_code' not in data.keys() \
                or 'subject_id' not in data.keys() \
                or 'category_id' not in data.keys():
            return {'message':
                        f"Not all mandatory columns(Skill Name, Skill Code, Subject ID and Category ID) provided."}, 401
        assessment_skill = AssessmentSkillModel(**data)
        try:
            assessment_skill.save_to_db()
        except Exception as e:
            return {"message":
                        f"An error occurred inserting the assessment skill details. Error: {repr(e)}"}, 500
        return assessment_skill.json(), 201

    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _assessment_skill_parser.parse_args()
        assessment_skills = AssessmentSkillModel.find_assessment_skill_by_any(
            **data)
        if assessment_skills:
            for assessment_skill in assessment_skills:
                assessment_skill.delete_from_db()
            return {'message': 'Assessment skills deleted.'}
        return {'message': 'Assessment skills not found.'}, 404

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _assessment_skill_parser.parse_args()
        for key in data.keys():
            if str(data[key]).lower() in ('none', 'null', ''):
                data[key] = None
        try:
            assessment_skill_id = data["skill_id"]
            assessment_skill = AssessmentSkillModel.find_by_skill_id(
                assessment_skill_id)
            if assessment_skill:
                assessment_skill.set_attribute(data)
                assessment_skill.save_to_db()
            return assessment_skill.json()
        except Exception as e:
            return {
                       'message': f"Assesment skill could not be found. {repr(e)}"}, 404
