from app import db


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True)
    full_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    reg_number = db.Column(db.String(255),unique=True)

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
    postion = db.Column(db.String(255))
    votes = db.Column(db.Integer)


    def __init__(self,full_name,password,reg_number,postion):
        self.full_name = full_name
        self.password = password
        self.reg_number = reg_number
        self.postion = postion
