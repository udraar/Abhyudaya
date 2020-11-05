from werkzeug.security import safe_str_cmp
from models.user import UserModel
from hashlib import md5


def authenticate(username, password):
    user = UserModel.find_by_email(username)
    print(f"Password: {password}")
    print(f"{user.password}, {md5(str(password).encode('UTF-8')).hexdigest()}")
    if user and safe_str_cmp(user.password, md5(str(password).encode('UTF-8')).hexdigest()):
    # if user and safe_str_cmp(user.password, password):
        print(user.json())
        return user
    else:
        print()

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)