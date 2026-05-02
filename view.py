from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from dbs.connection import db
from models.submit import Submit
from models.questions import Question
from models.answers import Answer
from models.personality_info import PersonalityInfo
from models.result import Result
from sent_mail import send_email
from controller.auth_controller import login_required
from services.mbti_calculator import calculate_mbti

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("homepage.html")

@views.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    all_questions = Question.query.order_by(Question.id).all()

    if request.method == 'POST':
        answers = {}
        for q in all_questions:
            score = request.form.get(f'q{q.id}')
            if score:
                score_int = int(score)
                answers[q.id] = score_int
                user_id = session.get('user_id')
                Answer.query.filter_by(user_id=user_id, question_id=q.id).delete()
                db.session.add(Answer(user_id=user_id, question_id=q.id, score=score_int))

        db.session.commit()

      
        mbti = calculate_mbti(answers)

      
        user_id = session.get('user_id')
        Result.query.filter_by(user_id=user_id).delete()
        db.session.add(Result(user_id=user_id, mbti_type=mbti))
        db.session.commit()

        session['mbti_result'] = mbti
        return redirect(url_for('views.show_result'))

    return render_template("testpage.html", questions=all_questions)

@views.route('/result')
@login_required
def show_result():
    mbti = session.get('mbti_result')

    if not mbti:
      
        user_id = session.get('user_id')
        saved = Result.query.filter_by(user_id=user_id).first()
        if saved:
            mbti = saved.mbti_type
        else:
            flash("Please complete the test first.")
            return redirect(url_for('views.test'))

    info = PersonalityInfo.query.filter_by(code=mbti).first()
    return render_template('result.html', mbti=mbti, info=info)

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