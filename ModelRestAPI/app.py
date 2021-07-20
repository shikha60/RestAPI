from flask_jwt import JWT
from models.UserModel import UserModel
from models.ProjectModel import ProjectModel
from flask_restful import Resource, Api
from flask import Flask
from security import authenticate, identity
from resources.User import UserRegister,Users,User,UserPasswordChange
from resources.Project import Project, Projects,ProjectsStatus
from resources.Client import Clients, Client



app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.secret_key = 'shikha'
JWT_SECRET_KEY = 'test'
jwt = JWT(app,authenticate,identity)


@app.before_first_request
def create_tables() :
    db.create_all()

api.add_resource(UserRegister,'/register')
api.add_resource(Users, "/users")
api.add_resource(User,"/user/<string:name>")
api.add_resource(UserPasswordChange,"/password-change")
api.add_resource(Projects,"/projects")
api.add_resource(Project, "/project/<string:name>")
api.add_resource(ProjectsStatus, "/project-status/<string:status>")
api.add_resource(Clients , "/clients")
api.add_resource(Client, "/client/<string:client_name>")



if __name__ == '__main__' :
    from db import db
    db.init_app(app)
    app.run(port=5000)