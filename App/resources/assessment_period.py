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
from models.assessment_period import AssessmentPeriodModel

_assessment_period_parser  = reqparse.RequestParser()
_assessment_period_parser.add_argument('assessment_period_id',required=False,type=int,store_missing=False)
_assessment_period_parser.add_argument('assessment_year',required=False,type=int,store_missing=False)
_assessment_period_parser.add_argument('assessment_month',type=int,store_missing=False)
_assessment_period_parser.add_argument('assessment_day',type=int,store_missing=False)
_assessment_period_parser.add_argument('session',type=str,store_missing=False)
_assessment_period_parser.add_argument('period',type=str,store_missing=False)

class AssessmentPeriodList(Resource):
    @jwt_required
    def get(self):
        data = request.args
        periods  = AssessmentPeriodModel.find_assessment_period_by_any(**data)
        if periods:
            resp = []
            for period in periods:
                resp.append(period.json())
            return resp
        else:
            return {'message': 'Assessment periods not found.'}

class AssessmentPeriod(Resource):
    @jwt_required
    def get(self):
        data = request.args
        if 'assessment_period_id' in data.keys():
            assessment_period = AssessmentPeriodModel.find_by_assessment_period_id(data['assessment_period_id'])
            if assessment_period:
                return assessment_period.json(), 200
            else:
                return {'message': "Assessment period id not found"}, 404
        assessment_period = AssessmentPeriodModel.find_assessment_period_by_any(**data)
        if assessment_period:
            assessment_period.json()
            return resp, 200
        return {'message': 'Assessment period not found'}, 404

    @jwt_required
    def post(self):
        data = _assessment_period_parser.parse_args()
        assessment_periods = AssessmentPeriodModel.find_assessment_period_by_any(
            **data)
        if len(assessment_periods)>0:
            return {'message': f"Assessment periods already exists with the details provided."}, 400
        if 'assessment_year' not in data.keys() or 'session' not in data.keys() or 'period' not in data.keys():
            return {'message': f"Not all mandatory columns(Assessment Year, Session and Period) provided."}, 401
        assessment_period = AssessmentPeriodModel(**data)
        try:
            assessment_period.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the assessment_period details. Error: {repr(e)}"}, 500
        return assessment_period.json(), 201

    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _assessment_period_parser.parse_args()
        assessment_periods = AssessmentPeriodModel.find_assessment_period_by_any(
            **data)
        if assessment_periods:
            for assessment_period in assessment_periods:
                assessment_period.delete_from_db()
            return {'message': 'Assessment periods deleted.'}
        return {'message': 'Assessment periods not found.'}, 404

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _assessment_period_parser.parse_args()
        for key in data.keys():
            if str(data[key]).lower() in ('none', 'null', ''):
                data[key] = None
        try:
            assessment_period_id = data["assessment_period_id"]
            assessment_period = AssessmentPeriodModel.find_by_assessment_period_id(assessment_period_id)
            if assessment_period:
                assessment_period.set_attribute(data)
                assessment_period.save_to_db()
            return assessment_period.json()
        except Exception as e:
            return {'message': f"Assesment period could not be found. {repr(e)}"}, 404