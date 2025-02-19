from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Admin Table Model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
# ElectoralCandidates Table Model
class ElectoralCandidates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_period = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    candidate1_name = db.Column(db.String(255), nullable=False)
    candidate1_reg_no = db.Column(db.String(50), nullable=False)
    candidate1_picture = db.Column(db.String(255), nullable=False)
    candidate2_name = db.Column(db.String(255), nullable=False)
    candidate2_reg_no = db.Column(db.String(50), nullable=False)
    candidate2_picture = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    reg_number = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)



class Dues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    reg_number = db.Column(db.String(50), nullable=False)
    session = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # "Paid" or "Unpaid"
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    student = db.relationship('Student', backref=db.backref('dues', lazy=True))

class TotalStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    reg_number = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name, reg_number):
        self.name = name
        self.reg_number = reg_number
