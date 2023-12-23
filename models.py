from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    score = db.Column(db.Integer, default=10000)


