from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt import JWT
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from resources.cluster import Cluster, ClusterList
from resources.user import UserRegister, User, UserLogin, UserList
from resources.student import Student, StudentList
from resources.teacher import Teacher, TeacherList
from models.user import UserModel
from models.organization import OrganizationModel
from models.user_role import UserRoleModel
from resources.kalika_kendra import KalikaKendra, KalikaKendraList
from resources.organization import Organization
from resources.user_role import UserRole

from resources.subject import Subject, SubjectList
from resources.assessment_period import AssessmentPeriod, AssessmentPeriodList
from resources.assessment_category import AssessmentCategory, AssessmentCategoryList
from resources.assessment_skill import AssessmentSkill, AssessmentSkillList
from resources.assessment_result import AssessmentResult, AssessmentResultList

app = Flask(__name__)
CORS(app)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://abhyudaya:abhyudaya123@localhost:3306/abhyudaya'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'abhyudaya'
api = Api(app)

# jwt = JWT(app, authenticate, identity)  # /auth
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(
        identity):  # Remember identity is what we define when creating the access token
    user = UserModel.find_by_id(identity)
    super_admins = ['Super Admin']
    admins = ['Admin']
    db_admins = ['DB Admin']
    program_manager = ['Program Manager']
    op_claims = {"email": user.email, 'is_super_admin': False,
                 'is_admin': False, 'is_db_admin': False,
                 'is_program_manager': False, 'teacher_code': user.teacher_code}

    user_role_org = fetch_user_role_org(user)
    user_role = user_role_org['user_role']
    user_org = user_role_org['user_organization']

    if user_role in super_admins:
        op_claims['is_super_admin'], op_claims['is_admin'], op_claims[
            'is_db_admin'] = True, True, True
    elif user_role in admins:
        op_claims['is_admin'] = True
    elif user_role in db_admins:
        op_claims['is_db_admin'] = True
    elif user_role in program_manager:
        op_claims['is_program_manager'] = True
    print(op_claims)
    return op_claims


def fetch_user_role_org(user: UserModel):
    try:
        user_role = UserRoleModel.find_by_role_id(user.user_role_id).role_name
        user_organization = \
            OrganizationModel.find_by_organization_id(user.organization_id).organization_name
    except:
        user_role = None
        user_organization = None
    finally:
        return {'user_role': user_role, 'user_organization': user_organization}


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token[
               'jti'] in BLACKLIST  # Here we blacklist particular JWTs that have been created in the past.


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(
        error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


api.add_resource(User, '/user')
api.add_resource(UserList, '/user/list')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Cluster, '/cluster')
api.add_resource(ClusterList, '/cluster/list')
api.add_resource(KalikaKendra, '/kalika_kendra')
api.add_resource(KalikaKendraList, '/kalika_kendra/list')
api.add_resource(Student, '/student')
api.add_resource(StudentList, '/student/list')
api.add_resource(Teacher, '/teacher')
api.add_resource(TeacherList, '/teacher/list')
api.add_resource(Organization, '/organization')
api.add_resource(UserRole, '/user_role')
api.add_resource(Subject, '/subject')
api.add_resource(SubjectList, '/subject/list')
api.add_resource(AssessmentPeriod, '/assessment_period')
api.add_resource(AssessmentPeriodList, '/assessment_period/list')
api.add_resource(AssessmentCategory, '/assessment_category')
api.add_resource(AssessmentCategoryList, '/assessment_category/list')
api.add_resource(AssessmentSkill, '/assessment_skill')
api.add_resource(AssessmentSkillList, '/assessment_skill/list')
api.add_resource(AssessmentResult, '/assessment_result')
api.add_resource(AssessmentResultList, '/assessment_result/list')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
