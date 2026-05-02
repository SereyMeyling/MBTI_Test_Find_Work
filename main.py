import os
from flask import Flask
from dbs.connection import db
from view import views

# Import all models
from models.user import User
from models.submit import Submit
from models.questions import Question
from models.answers import Answer
from models.result import Result
from models.personality_info import PersonalityInfo

# Import controllers
from controller.auth_controller import auth

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

  
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'mbti')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)
   

    # Register routes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


# Run App
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)