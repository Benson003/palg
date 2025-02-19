from models import models
from app import db
import bcrypt

def verify_password(plain_password, hashed_password):

    encoded_password = plain_password.encode('utf-8')  # Convert to bytes
    return bcrypt.checkpw(encoded_password, hashed_password)

def __password_hashing__(password):
    gen_salt = bcrypt.gensalt()
    encoded_password = password.encode('utf_8')
    hashed_password = bcrypt.hashpw(encoded_password,gen_salt)
    return hashed_password


class User:

    def  get_all_user(self):
        return models.User.query.all()

    def get_specfic_user(self,user_reg_number):
        user = models.User.query.filter(models.User.reg_number == user_reg_number).first()
        return user

    def add_user(self,email,full_name,password,reg_number):
        new_user = models.User(
            email = email,
            full_name = full_name,
            password = __password_hashing__(password),
            reg_number = reg_number,
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

class Admin:
    def get_all_admin(self):
        return models.Admin.query.all()

    def get_specfic_admin(self,user_email):
        admin = models.Admin.query.filter(models.Admin.email == user_email).first()
        return admin

    def add_admin(self,email,full_name,password):
        new_admin = models.Admin(
            email = email,
            full_name = full_name,
            password = __password_hashing__(password),
        )

        try:
            db.session.add(new_admin)
            db.session.commit()
        except Exception as e:
            db.session.rollback()


class Dues:
    def get_all_admin(self):
        return models.Dues.query.all()

    def get_specfic_dues(self,reg_number):
        due= models.Dues.query.filter(models.Dues.reg_number == reg_number).first()
        return due

    def add_dues(self,full_name,reg_number):
        new_dues = models.Dues(
            full_name = full_name,
            reg_number = reg_number
        )
        try:
            db.session.add(new_dues)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

class ElectoralCandidates:
    def get_all_admin(self):
        return models.ElectoralCandidates.query.all()

    def get_specfic_dues(self,reg_number):
        due= models.ElectoralCandidates.query.filter(models.ElectoralCandidates.reg_number == reg_number).first()
        return due

    def add_electoral_candidates(self,full_name,password,reg_number,postion):
        new_dues = models.ElectoralCandidates(
            full_name = full_name,
            password = password,
            reg_number = reg_number,
            postion = postion,
        )
        try:
            db.session.add(new_dues)
            db.session.commit()
        except Exception as e:
            print("f{e}")
            db.session.rollback()
