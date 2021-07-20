from models.UserModel import UserModel
from flask_jwt_extended import JWTManager,get_jti,get_jwt

from flask_restful import Api
from flask import Flask,jsonify

from resources.User import (UserRegister,Users,User,UserPasswordChange,
            UserLogin,TokenRefresh, User_by_token, UserLogout)
from resources.Project import Project, Projects,ProjectsStatus
from resources.Client import Clients, Client
from db import db
from Blacklist import Blacklist



app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access' , 'refresh']
app.secret_key = 'shikha'
app.config['JWT_SECRET_KEY'] = 'test'
jwt = JWTManager(app)


@app.before_first_request
def create_tables() :
    db.init_app(app)
    db.create_all()

# @jwt.additional_claims_loader
# def add_claim_jwt(identity) :
#     user : UserModel = UserModel.find_by_username(identity)
#     if user.access == "admin" :
#         return {"is_admin" : True}
#     return {"is_admin" : False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header,jwt_data) :
    return jwt_data["jti"] in Blacklist

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header,jwt_data) :
    return jsonify({
        "message" : "the token has been revoked",
        "error" : "token_revoked"
    }) , 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({
        "message" : "the token has expired",
        "error" : "token_expired"
    }) , 401

@jwt.invalid_token_loader
def invalid_token_callback(error) :
    return jsonify({
        "message" :"Signature verification failed",
        "error" : "invalid_token"
    }) ,401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "message" :"Request does not contain an access token",
        "error" : "authorization_required"
    }) , 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_data) :
    return jsonify({
        "message" :"The token is not fresh",
        "error" : "fresh_token_required"
    })

api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin , "/login")
api.add_resource(Users, "/users")
api.add_resource(User, "/user/<string:name>")
api.add_resource(User_by_token, "/user")
api.add_resource(UserPasswordChange,"/password-change")
api.add_resource(UserLogout,"/logout")
api.add_resource(Projects,"/projects")
api.add_resource(Project, "/project/<string:name>")
api.add_resource(ProjectsStatus, "/project-status/<string:status>")
api.add_resource(Clients , "/clients")
api.add_resource(Client, "/client/<string:client_name>")
api.add_resource(TokenRefresh, "/refresh")



if __name__ == '__main__' :
    from db import db
    db.init_app(app)
    app.run(port=5000)