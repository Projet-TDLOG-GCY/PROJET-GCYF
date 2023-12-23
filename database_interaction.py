from flask import Flask
from models import User
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    score = db.Column(db.Integer, default=10000)

# Push the application context
app.app_context().push()

users = User.query.all()
print(len(users))
for user in users:
    print(user.id, user.score)

