from dbs.connection import db

class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    mbti_type = db.Column(db.String(10))

    def __init__(self, user_id, mbti_type):
        self.user_id = user_id
        self.mbti_type = mbti_type