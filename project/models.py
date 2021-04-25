from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))

    def __init__(self,id,email,password,name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return f"<User {self.name}>"
