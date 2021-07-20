from db import db

class ClientModel(db.Model) :
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key = True)
    client_name = db.Column(db.String)
    projects = db.relationship('ProjectModel',lazy = 'dynamic',back_populates = 'c')

    def __init__(self,client_name) -> None:
        self.client_name = client_name
    
    def tojson(self) :
        return {
            "client_id" : self.client_id,
            "client_name" : self.client_name,
            "projects" : [x.tojson() for x in self.projects.all()]
        } 
    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self) :
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_client_by_name(cls,client_name) :
        return cls.query.filter_by(client_name = client_name).first()
    
    @classmethod
    def get_all_clients(cls) :
        return cls.query.all()
    

        

