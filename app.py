from  app import create_app
from app import db

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all()
