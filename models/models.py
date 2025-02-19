from app import db


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True)
    full_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    reg_number = db.Column(db.String(255),unique=True)
    hasVoted = db.Column(db.Boolean, default=False)

    def __init__(self,email,full_name,password,reg_number):
        self.email = email
        self.full_name = full_name
        self.password = password
        self.reg_number = reg_number


class Dues(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String(255))
    reg_number = db.Column(db.String(255),unique=True)
    timestamp = db.Column(db.DateTime,default = db.func.current_timestamp())


class Admin(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True)
    full_name = db.Column(db.String(255))
    password = db.Column(db.String(255))

class ElectoralCandidates(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String(255))
    reg_number = db.Column(db.String(255),unique=True)
    position = db.Column(db.String(255))
    votes = db.Column(db.Integer,default = 0)


    def __init__(self,full_name,reg_number,position):
        self.full_name = full_name
        self.reg_number = reg_number
        self.position = position
