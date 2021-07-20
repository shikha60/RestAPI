from models.ProjectModel import ProjectModel
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.ClientModel import ClientModel

class Client(Resource) :
    @jwt_required()
    def get(self,client_name) :
        client = ClientModel.get_client_by_name(client_name)
        if client :
            return client.tojson(), 200
        return {"message" : "There is no such client"}
    
    def post(self,client_name) :
        if ClientModel.get_client_by_name(client_name) is not None :
            return {"message" : "A client with the same name already exists"}
        client = ClientModel(client_name)
        try :
            client.save_to_db()
        except :
                return{"message" : "some error occured while saving"}
        return{"client created" : client.tojson()} , 201
    
    @jwt_required(fresh = True)
    def delete(self,client_name) :
        client:ClientModel =  ClientModel.get_client_by_name(client_name)
        copy = client
        if client :
            if len(client.tojson()['projects']) :
                for project in client.tojson()['projects'] :
                    p : ProjectModel = ProjectModel.get_by_project_name(project['project_name'])
                    p.delete_from_db()
            client.delete_from_db()
            return {"client deleted with all its associated projects" : copy.tojson()} , 200
        return {"message" : "no such client"}
            

class Clients(Resource) :
    @jwt_required()
    def get(self) :
        return {"clients" : [x.tojson() for x in ClientModel.get_all_clients()]} , 200
    

