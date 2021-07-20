from models.UserModel import UserModel



def authenticate(username,password) :
    user = UserModel.find_by_username(username)
    if user:
        if user.password == password :
            return user
       
def identity(payload) :
    userid = payload['identity']
    return UserModel.find_by_id(userid)


