
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.UserModel import UserModel

parser = reqparse.RequestParser()
parser.add_argument('username',
                    type = str, 
                    required = True,
                    help = "Username is required in order to register a user"
                    )
parser.add_argument('password',
                    type = str,
                    required = True,
                    help = 'Both username and password are required to register')

class UserRegister(Resource) :
    global parser
    def post(self) :
        data = parser.parse_args()
        if UserModel.find_by_username(data['username']) :
            return {"message" : "A user with that username already exists"} , 400
        
        user = UserModel(data['username'] , data['password'])
        try :
            user.save_to_db()
        except :
            return {"message" : "An error occurred while inserting the item"} ,500

        return user.tojson() , 201

class User(Resource) :
    @jwt_required()
    def get(self, name) :
        user = UserModel.find_by_username(name)
        if user:
            return user.tojson()
        return {"message" : "user with the following username does not exist"} , 400
    
    @jwt_required()
    def delete(self,name) :
        user = UserModel.find_by_username(name)
        if user :
            try :
                user.delete_from_db()
            except :
                return{"message" : "some error occured while saving"}
            return{"Following user deleted successfully" : user.tojson()} , 
        return {"message" : "No such user exists"} ,400 
    
class UserPasswordChange(Resource) :
    @jwt_required()
    def put(self) :
        data = parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user :
            if user.password == data['password'] :
                return {"message" : "New password cannot be the same as previous password"} ,400 
            user.password = data['password']
            user.save_to_db()
            return {"message" : "Password successfully changed."} , 200
        else:
            user = UserModel(data['username'],data['password'])
            try :
                user.save_to_db()
            except :
                return{"message" : "some error occured while saving"}
            return {"message" : "no such user existed, hence user created."} , 201
        
            
    

class Users(Resource) :
    @jwt_required()

    def get(self):
        return {"Users" : [x.tojson() for x in UserModel.query.all()]}


