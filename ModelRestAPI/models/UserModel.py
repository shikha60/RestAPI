from db import db

class UserModel(db.Model) :
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(50))
    projects = db.relationship('ProjectModel', lazy = 'dynamic',back_populates='user')

    def __init__(self,username,password) :
        self.username = username
        self.password = password
    
    def tojson(self) :
        return {'id':self.id ,
                'username' : self.username,
                'projects' : [project.tojson() for project in self.projects.all()] 
               }
    
    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self) :
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls,uname) :
        return cls.query.filter_by(username = uname).first()
    # @classmethod
    # def get_project_by_username(cls,name) :

    @classmethod
    def find_by_id(cls,_id) :
        return cls.query.filter_by(id = _id).first()
        