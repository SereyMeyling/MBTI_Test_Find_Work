from werkzeug.security import check_password_hash, generate_password_hash
from dbs.connection import db
from models.user import User

def register_user(form):
    name = form.get('name')
    email = form.get('email')
    password = form.get('password')
    confirm_password = form.get('confirm_password')

    if not all([name, email, password, confirm_password]):
        return {'success': False, 'message': 'All fields are required'}

    if password != confirm_password:
        return {'success': False, 'message': 'Passwords do not match'}
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {'success': False, 'message': 'Email already exists'}

    hashed_password = generate_password_hash(password)

    new_user = User(
        name=name,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return {'success': True, 'user': new_user}


def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return {'success': True, 'user': user}

    return {'success': False, 'message': 'Invalid email or password'}