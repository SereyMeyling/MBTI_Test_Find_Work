from flask import Blueprint, render_template, request
from dbs.connection import db
from models.submit import Submit
from sent_mail import send_email

views=Blueprint('views',__name__)
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