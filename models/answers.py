from dbs.connection import db

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer,db.ForeignKey('questions.id'))
    score = db.Column(db.Integer)

    def __init__(self, user_id, question_id, score):
        self.user_id = user_id
        self.question_id = question_id
        self.score = score