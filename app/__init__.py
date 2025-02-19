from flask import Flask
from models.model import db
from routes import routes




def create_app():
    app = Flask(__name__)
    app.secret_key = 'gvhbhgbycrsrtff54tfrcvvyy778uuyggcrdeded4we56gyghuihugtdfrderd'


    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///palgunn.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    routes.register_routes(app)
    db.init_app(app)


    return app
