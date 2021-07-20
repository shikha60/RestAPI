Model Rest API

#Installation
```
pip install Flask
pip install Flask-RESTful
pip install Flask-JWT-extended
pip install Flask-SQLAlchemny
```

#Description
This is a simple Model Rest API with CRUD functionalities .
The app is connected to SQL databases, and relationships are formed between tables in various resources.
Further authentication is done through JWT tokens, which involves logging in to access various resources, checking access rights to access certain resources(admin rights for resource - Users) , checking if the token is fresh for critical resources such as for changing the password for a user and logging out and blacklisting the token once the user has successfully logged out.


#Implementation 
This project is implemented using Flask_restful, interaction with a SQL database is done using Flask-SQLAlchemy while the authorization for accessing the resources is done using Flask-jwt-extended.