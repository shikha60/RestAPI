
from typing import Optional
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity#, additional_claims


from models.ProjectModel import ProjectModel

parser = reqparse.RequestParser()
parser.add_argument("project_type",
                type = str,
                required = True,
                help = 'Project type is required'
                )
parser.add_argument('client',
                type = str,
                # required = True,
                # help = 'client is required'
                )
parser.add_argument('emp_name',
            type = str,
            # required = True,
            # help = 'employee name is required'
            )
parser.add_argument('status',
            type = str,
            
            )


class Project(Resource) :
    
    @jwt_required()
    def get(self, name) :
        project = ProjectModel.get_by_project_name(name)
        if project :
            return project.tojson()
        return {"message" : "invalid project id"} , 400
    
    def post(self,name) :
        global parser
        if ProjectModel.get_by_project_name(name) is not None:
            return {"message" : "The project name is already associated with another project"} , 400
        data = parser.parse_args()
        project = ProjectModel(name, data['project_type'],data['client'],data['emp_name'],data['status'])
        
        try :
            project.save_to_db()
        except :
            return {"message": "An error occurred while inserting the item."}, 500 
        return project.tojson() , 201
    
    @jwt_required()
    def delete(self,name) :
        project = ProjectModel.get_by_project_name(name)
        if project :
            project.delete_from_db()
            return {"message : Following project deleted successfully" : project.tojson()}
        return {"message" : "no such user exists"}
    
    @jwt_required()
    def put(self,name):
        parser1 = reqparse.RequestParser()
        parser1.add_argument('status',
                            type = str,
                            required = True,
                            help ="A new status is required for changing the status")
        data = parser1.parse_args()
        project = ProjectModel.get_by_project_name(name)
        if project :
            if project.status == data['status'] :
                return {"message" : "New status cannot be the same as old status"} , 400
            project.status = data['status']
            try :
                project.save_to_db()
            except :
                return {"message" :" error occured while saving to database.Try again"} ,500
            return {"message" : " status changed successfully"}
        return {"message" : " a project with the given name does not exist"}
        


class ProjectsStatus(Resource) :
    @jwt_required(optional = True)
    def get(self,status) :
        username = get_jwt_identity()
        if username :
            return {"project names" : [x.tojson() for x in ProjectModel.get_by_status(status)]}
        return {"projects" : [x.project_name for x in ProjectModel.get_by_status(status)],
                "message" : "for more information on projects login"}
        
    
class Projects(Resource) :
    @jwt_required()
    def get(self) :
        # claims = additional_claims()
        # if not claims['is_admin'] :
        #     return {"message" : "admin privilage required"} , 401 
        return {"projects" : [x.tojson() for x in ProjectModel.get_all()]} 
                


