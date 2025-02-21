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
from app import db


positions = ["President", "Vice President", "Secretary", "Treasurer"]

admin_templates =  {
            None:"admin/index.html",
            **{t: f"admin/{t}.html" for t in ["login","signup","logout","student_dues","add_contenstants","results"]}
        }

user_templates = {
            None:"user/index.html",
            **{t: f"user/{t}.html" for t in ["login","signup","logout","vote"]}
        }


class Admin(MethodView):
    def get(self, link_type=None):
        candidates = dl.ElectoralCandidates().get_all_candidates()
        if link_type:
            link_type = link_type.strip().lower().rstrip("/")

        templates = admin_templates
        template = templates.get(link_type)

        if link_type == "clear_polls":
            self.clear_polls()
            return redirect(url_for("admin_base"))

        if link_type == "logout":
            self.logout()

        return render_template(template, positions=positions ,candidates = candidates) if template else abort(404)


    def post(self,link_type):
        link_type = link_type.strip().lower().rstrip("/") if link_type else None
        form_data = request.form.to_dict()

        handlers = {
            "login": self.login,
            "signup":self.signup,
            "student_dues": self.student_dues,
            "add_contenstants":self.add_contenstants,
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
        flash("It seems you dont have an account")
        return redirect(url_for("admin_links",link_type ="signup"))
    def signup(self,form_data):
        full_name = form_data.get("fullname")
        email = form_data.get("email")
        password = form_data.get("password")

        if dl.Admin().get_specfic_admin(email) != None:
            flash("Admin registred",category="warning")
            return redirect(url_for("admin_links",link_type = "login"))

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

        return redirect(url_for("admin_links",link_type = "student_dues"))


    def add_contenstants(self,form_data):
        full_name = form_data.get("full_name")
        reg_number = form_data.get("reg_number")
        position = form_data.get("position")

        if dl.ElectoralCandidates().get_specfic_candidates(reg_number) != None:
            flash("Candidate allready running",category="warning")
            return redirect(url_for("admin_links",link_type = "add_contenstants"))

        if full_name != None and reg_number != None and position != None:
            dl.ElectoralCandidates().add_electoral_candidates(
                full_name=full_name,
                reg_number=reg_number,
                position= position

            )
        return redirect(url_for("admin_links",link_type="add_contenstants"))

    def clear_polls(self):
        users = dl.User().get_all_user()
        candidates = dl.ElectoralCandidates().get_all_candidates()

        if users and candidates :
            for user in users:
                user.hasVoted = False
            for candidate in candidates:
                candidate.votes = 0

            db.session.commit()
            flash("All polls have been reset")


        return redirect(url_for("admin_base"))


    def logout(self):
        session.clear()
        return redirect(url_for("admin_base"))






class User(MethodView):
    def get(self,link_type = None):
        templates = user_templates
        candidates = dl.ElectoralCandidates().get_all_candidates()
        voter = dl.User().get_specfic_user(session.get("reg_number"))
        link_type = link_type.strip().lower().rstrip("/") if link_type else None
        template = templates.get(link_type)
        if link_type == "logout":
            self.logout()

        return render_template(template,candidates = candidates, voter = voter) if template else abort(404)

    def post(self,link_type):
        link_type = link_type.strip().lower().rstrip("/") if link_type else None
        form_data = request.form.to_dict()

        handlers = {
            "login": self.login,
            "signup":self.signup,
            "logout":self.logout,
            "vote":self.vote,
            }
        handler = handlers.get(link_type, lambda: abort(404))
        return handler(form_data) if link_type in ["login", "signup"] else handler()

    def login(self,form_data):
        reg_number = form_data.get("reg_number")
        password = form_data.get("password")
        user = dl.User().get_specfic_user(reg_number)
        if user != None:
            if verify_password(plain_password=password,hashed_password= user.password):
                flash(f"Logged in as {user.reg_number}",category='info')
                session["reg_number"] = user.reg_number
                session["isAdmin"] = False
                session["fullname"] = user.full_name
                session["email"] = user.email
                session["hasVoted"] = user.hasVoted
                return redirect(url_for("user_base"))
        flash("Please sign up")
        return redirect(url_for("user_links", link_type = "login"))


    def signup(self, form_data):
        full_name = form_data.get("fullname")
        email = form_data.get("email")
        password = form_data.get("password")
        reg_number = form_data.get("reg_number")

        # Check if dues are paid first
        if not dl.Dues().get_specfic_dues(reg_number):
            flash("Account not created. You may not have paid your dues or the database has not been updated.", "warning")
            return redirect(url_for("user_links", link_type="signup"))

        # Check if user already exists
        if dl.User().get_specfic_user(reg_number) :
            flash("User already has an account.", "warning")
            return redirect(url_for("user_links", link_type="login"))

        existing_user = dl.User().get_specfic_user(reg_number)
        if existing_user != None:
            if existing_user.email:
                flash("This email is already in use. Please use a different email.", "warning")
                return redirect(url_for("user_links", link_type="signup"))

        # Create the user
        dl.User().add_user(
            full_name=full_name,
            email=email,
            reg_number=reg_number,
            password=password
        )


        flash("Account successfully created!", "success")
        return redirect(url_for("user_links", link_type="login"))



    def logout(self):
        session.clear()
        return redirect(url_for("user_base"))


    def vote(self):
    # Extract votes from the form
        votes = {key.replace("vote_", ""): request.form.get(key) for key in request.form if key.startswith("vote_")}

        if not votes:
            flash("Please select a candidate foor each category")
            return redirect(url_for("user_links",link_type = "vote"))

        try:
            for reg_number in votes.values():
                candidate = dl.ElectoralCandidates().get_specfic_candidates(reg_number)
                person = dl.User().get_specfic_user(session["reg_number"])
                if candidate and person.hasVoted == False:
                    candidate.votes += 1
                    person.hasVoted = True# Increment vote count
                    db.session.add(candidate)
                    db.session.commit()  # Commit all updates in one transaction
                    flash("Vote has been submited")
                    return redirect(url_for("user_links",link_type = "vote"))

                flash("You have voted already.")
                return redirect(url_for("user_links",link_type ="vote"))

        except Exception as e:
            flash(f"An Error Occured : {e}")
            db.session.rollback()  # Rollback in case of an error
            return redirect(url_for("user_base"))
