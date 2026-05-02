from dbs.connection import db

class PersonalityInfo(db.Model):
    __tablename__ = 'personality_info'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), unique=True) 
    title = db.Column(db.String(100))         
    description = db.Column(db.Text)        
    suitable_jobs = db.Column(db.Text)       