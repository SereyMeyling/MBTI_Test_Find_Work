import os
from pathlib import Path
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


def load_env_file(env_path: str = '.env') -> None:
    path = Path(__file__).resolve().with_name(env_path)
    if not path.exists():
        return

    for encoding in ('utf-8-sig', 'utf-16', 'utf-16-le', 'utf-16-be'):
        try:
            content = path.read_text(encoding=encoding)
            break
        except UnicodeError:
            continue
    else:
        content = path.read_text(encoding='utf-8', errors='ignore')

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[7:].strip()
        if '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_env_file()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'mbti')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)
   

    # Register routes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Create database tables only when explicitly requested.
    if os.getenv('CREATE_TABLES_ON_STARTUP', 'false').lower() == 'true':
        with app.app_context():
            db.create_all()

    return app


# Run App
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)