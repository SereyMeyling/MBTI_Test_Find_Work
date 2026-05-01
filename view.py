from flask import Blueprint, render_template, request , redirect ,url_for,flash
from dbs.connection import db
from models.submit import Submit
from models.questions import Question
from models.answers import Answer
from models.personality_info import PersonalityInfo

from sent_mail import send_email
from controller.auth_controller import login_required
from flask_login import current_user 



views=Blueprint('views',__name__)
@views.route('/')
def home():
    return render_template("homepage.html")

@views.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    all_questions = Question.query.order_by(Question.id).all()

    if request.method == 'POST':
        for q in all_questions:
            score = request.form.get(f'q{q.id}')
            if score:
                new_answer = Answer(user_id=current_user.id, question_id=q.id, score=int(score))
                db.session.add(new_answer)

        db.session.commit()
        return redirect(url_for('views.show_result'))

    return render_template("testpage.html", questions=all_questions)
@views.route('/personalities')
def personalities():
    return render_template("personality.html")
@views.route('/contact')
def contact():
    return render_template("contact.html")
@views.route('/login')
def login():
    return render_template("login.html")

@views.route('/register')
def register():
    return render_template("register.html")


@views.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email or not subject or not message:
        return render_template('contact.html', message='Please fill in all fields')

    data = Submit(name, email, subject, message)
    db.session.add(data)
    db.session.commit()

    send_email(name, email, message, subject)

    return render_template('success.html')

@views.route('/result')
def show_result():
    user_mbti = "INTJ"
    info = PersonalityInfo.query.filter_by(code=user_mbti).first()
    return render_template('result.html', mbti=user_mbti, info=info)