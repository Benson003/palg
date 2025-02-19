from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import session




db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.squlite3"
    app.secret_key = "bensuu9u247yjf#!)ndawud384"

    db.init_app(app)
    migrate.init_app(app,db)


    with app.app_context():
        from routes import routes
        from models import models
        routes.register_routes(app)
        
    return app
