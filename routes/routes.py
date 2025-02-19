from flask import render_template
from routes import class_views as cl
from app import session

def register_routes(app):
    @app.route("/",methods=["GET"])
    def index():
        return render_template("user/index.html")

    app.add_url_rule("/user/",view_func=cl.User.as_view('user_base'))
    app.add_url_rule("/user/<string:link_type>",view_func=cl.User.as_view('user_links'))
    app.add_url_rule("/admin/",view_func=cl.Admin.as_view('admin_base'))
    app.add_url_rule("/admin/<string:link_type>",view_func=cl.Admin.as_view('admin_links'))
