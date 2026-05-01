from dbs.connection import db

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), unique=True)
    text = db.Column(db.String(200))
    dimension = db.Column(db.String(50))

    def __init__(self, question, text, dimension):
        self.question = question
        self.text = text
        self.dimension = dimension