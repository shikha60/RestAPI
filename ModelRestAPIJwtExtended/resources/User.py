
from flask_jwt_extended import (jwt_required, create_access_token,create_refresh_token,
                                get_jwt_identity,get_jwt)
from flask_restful import Resource, reqparse
from models.UserModel import UserModel
from Blacklist import Blacklist


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
parser.add_argument('access',
                    type = str,
                    )


class UserRegister(Resource) :
    global parser

    def post(self) :
        data = parser.parse_args()
        if UserModel.find_by_username(data['username']) :
            return {"message" : "A user with that username already exists"} , 400
        
        user = UserModel(**data)
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


class User_by_token(Resource) :
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = UserModel.find_by_username(current_user)
        return user.tojson()

    
class UserPasswordChange(Resource) :
    @jwt_required(fresh = True)
    def put(self) :
        data = parser.parse_args()
        user: UserModel = UserModel.find_by_username(data['username'])
        current = get_jwt_identity()
        if user :
            if current != user.username :
                return {"message" :  "you do not have authorization to change the password for the given user"}
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
        username = get_jwt_identity()
        user = UserModel.find_by_username(username)
        if user.access == "admin" :
            return {"Users" : [x.tojson() for x in UserModel.query.all()]}
        return {"message" : "admin access required"}, 401


class UserLogin(Resource) :
    def post(self) :
        global parser
        data = parser.parse_args()
        user =  UserModel.find_by_username(data['username']) 
        if user :
            if data['password'] == user.password:
                access_token = create_access_token(identity = user.username, fresh= True)
                refresh_token = create_refresh_token(user.username)
                return {
                    "access_token" : access_token ,
                    "refresh_token" : refresh_token
                } , 200
            return {"message"  : "incorrect password"} , 401
        return {"message" : "invalid username"} , 401

class TokenRefresh(Resource) :
    @jwt_required(fresh = False)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token" : new_token}, 200

class UserLogout(Resource) :
    @jwt_required()
    def post(self) :
        jti = get_jwt()["jti"]
        Blacklist.add(jti)
        return {"message" : "user successfully logged out"}