from flask.views import MethodView
from flask import flash
from flask import redirect
from flask import render_template
from flask import abort
from flask import request
from models.data_handler import verify_password
from models import data_handler as dl
from flask import url_for
from app import session




admin_templates =  {
            None:"admin/index.html",
            **{t: f"admin/{t}.html" for t in ["login","signup","logout","student_dues"]}
        }

user_templates = {
            None:"user/index.html",
            **{t: f"user/{t}.html" for t in ["login","signup","logout"]}
        }


class Admin(MethodView):
    def get(self,link_type = None):
        templates = admin_templates
        link_type = link_type.strip().lower().rstrip("/") if link_type else None
        template = templates.get(link_type)

        if link_type == "logout":
            self.logout()

        return render_template(template) if template else abort(404)

    def post(self,link_type):
        link_type = link_type.strip().lower().rstrip("/") if link_type else None
        form_data = request.form.to_dict()

        handlers = {
            "login": self.login,
            "signup":self.signup,
            "student_dues": self.student_dues,
            }
        handler = handlers.get(link_type, lambda *args: abort(404))
        return handler(form_data)

    def login(self,form_data):
        email = form_data.get("email")
        password = form_data.get("password")
        admin = dl.Admin().get_specfic_admin(user_email=email)
        if admin != None:
            if verify_password(plain_password=password,hashed_password= admin.password):
                flash(f"Logged in as {admin.email}",category='info')
                session["email"] = admin.email
                session["isAdmin"] = True
                session["fullname"] = admin.full_name
                return redirect(url_for("admin_base"))
    def signup(self,form_data):
        full_name = form_data.get("fullname")
        email = form_data.get("email")
        password = form_data.get("password")

        if full_name != None and email !=None and password != None:
            dl.Admin().add_admin(
                full_name = full_name,
                email = email,
                password = password
            )
            return redirect(url_for("admin_links",link_type = "login"))

    def student_dues(self,form_data):
        full_name = form_data.get("full_name")
        reg_number = form_data.get("reg_number")
        if full_name != None and reg_number != None:
            dl.Dues().add_dues(
                full_name= full_name,
                reg_number=reg_number,
            )
        flash("Student Dues Updated sucessfully")
        return redirect(url_for("admin_links",link_type = "student_dues"))



    def logout(self):
        session.clear()
        return redirect(url_for("admin_base"))





class User(MethodView):
    def get(self,link_type = None):
        templates = user_templates
        link_type = link_type.strip().lower().rstrip("/") if link_type else None
        template = templates.get(link_type)
        if link_type == "logout":
            self.logout()

        return render_template(template) if template else abort(404)

    def post(self,link_type):
        link_type = link_type.strip().lower().rstrip("/") if link_type else None
        form_data = request.form.to_dict()

        handlers = {
            "login": self.login,
            "signup":self.signup,
            "logout":self.logout,
            }
        handler = handlers.get(link_type, lambda *args: abort(404))
        return handler(form_data)

    def login(self,form_data):
        reg_number = form_data.get("reg_number")
        password = form_data.get("password")
        user = dl.User().get_specfic_user(user_reg_number= reg_number)
        if user != None:
            if verify_password(plain_password=password,hashed_password= user.password):
                flash(f"Logged in as {user.reg_number}",category='info')
                session["reg_number"] = user.reg_number
                session["isAdmin"] = False
                session["fullname"] = user.full_name
                session["email"] = user.email
                return redirect(url_for("user_base"))


    def signup(self,form_data):
        full_name = form_data.get("fullname")
        email = form_data.get("email")
        password = form_data.get("password")
        reg_number = form_data.get("reg_number")

        if full_name != None and email !=None and password != None and reg_number != None:
            dl.User().add_user(
                full_name = full_name,
                email = email,
                reg_number= reg_number,
                password = password
            )
            return redirect(url_for("user_links",link_type = "login"))

    def logout(self):
        session.clear()
        return redirect(url_for("user_base"))
