from sqlalchemy.orm import relationship
from db import db


class ProjectModel(db.Model):
    __tablename__ = 'projects'
    project_id = db.Column(db.Integer, primary_key = True)
    project_name = db.Column(db.String(50))
    project_type = db.Column(db.String(50))
    client = db.Column(db.String,db.ForeignKey('client.client_name'))
    status = db.Column(db.String)
    emp_name = db.Column(db.String, db.ForeignKey('users.username'))
    user = db.relationship('UserModel',back_populates = 'projects')
    c = db.relationship('ClientModel',back_populates = 'projects')
    

    def __init__(self, project_name,project_type,client, emp_name,status):
        self.project_name = project_name
        self.project_type = project_type
        self.client = client
        self.emp_name = emp_name
        self.status = status
    
    def tojson(self) :
        return {
            "project id "  :self.project_id,
            "project_name" : self.project_name,
            "project_type" : self.project_type,
            "client" : self.client,
            "employee name" : self.emp_name,
            "project status" : self.status
        }
    @classmethod
    def get_all(cls) :
        return cls.query.all()
    
    @classmethod
    def get_by_project_id(cls, pid) :
        return cls.query.filter_by(project_id = pid)

    @classmethod
    def get_by_project_name(cls,name) :
        return cls.query.filter_by(project_name = name).first()
    
    @classmethod
    def get_by_status(cls,status) :
        return  cls.query.filter_by(status = status).all()

    
    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) :
        db.session.delete(self)
        db.session.commit()
    
    def update_db(self) :
        db.session.up
      

