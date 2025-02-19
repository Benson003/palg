from models import models
from app import db
import bcrypt
from flask import flash

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
            flash("User added sucessfully")
        except Exception as e:
            flash(f"Something went wrong {e}",category="error")
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
            flash("Admin has been created")
        except Exception as e:
            flash(f"Something went wrong {e}",category="error")
            db.session.rollback()


class Dues:
    def get_all_dues(self):
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
            flash("Database has been succesfully updated")
        except Exception as e:
            flash("Something has goe wrong",category="error")
            db.session.rollback()

class ElectoralCandidates:
    def get_all_candidates(self):
        return models.ElectoralCandidates.query.all()

    def get_specfic_candidates(self,reg_number):
        due= models.ElectoralCandidates.query.filter(models.ElectoralCandidates.reg_number == reg_number).first()
        return due

    def add_electoral_candidates(self,full_name,reg_number,position):
        new_dues = models.ElectoralCandidates(
            full_name = full_name,
            reg_number = reg_number,
            position = position,
        )
        try:
            db.session.add(new_dues)
            db.session.commit()
            flash("Candidate Added Sucessfully")
        except Exception as e:
            flash("Something went wrong",category="error")
            print("f{e}")
            db.session.rollback()
