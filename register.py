

# from flask import Blueprint, render_template, redirect, url_for, flash
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, validators
# from models import db, User
# from werkzeug.security import generate_password_hash

# register_bp = Blueprint('register', __name__)

# class RegistrationForm(FlaskForm):
#     id = StringField('ID', validators=[validators.DataRequired()])
#     password = PasswordField('Password', validators=[validators.DataRequired()])
#     submit = SubmitField('Sign Up')



# @register_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = RegistrationForm()

#     if form.validate_on_submit():
#         user_id = form.id.data
#         password = form.password.data

#         # Check if the user already exists in the database
#         existing_user = User.query.filter_by(id=user_id).first()
#         if existing_user:
#             flash('User already exists! Your score is {}'.format(existing_user.score), 'danger')
#         else:
#             # Hash the password before storing it
#             hashed_password = generate_password_hash(password, method='sha256')
#             # Create a new user
#             new_user = User(id=user_id, password=hashed_password)
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Account created for {}!'.format(form.id.data), 'success')

#         return redirect(url_for('register.signup'))

#     return render_template('signup.html', form=form)


# import requests

# url = 'http://127.0.0.1:5000/signup'  # Replace with the actual URL
# data = {'id': 'claragmail.com', 'password': '12345', 'score': 200}
# response = requests.post(url, data=data)

# if response.status_code == 200:
#     print('User added successfully')
# else:
#     print('Failed to add user')

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from .models import db, User
from werkzeug.security import generate_password_hash

register_bp = Blueprint('register', __name__)

class RegistrationForm(FlaskForm):
    id = StringField('ID', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Sign Up')

@register_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        user_id = form.id.data
        password = form.password.data

        # Check if the user already exists in the database
        existing_user = User.query.filter_by(id=user_id).first()
        if existing_user:
            flash('User already exists! Your score is {}'.format(existing_user.score), 'danger')
        else:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password, method='sha256')
            # Create a new user
            new_user = User(id=user_id, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created for {}!'.format(form.id.data), 'success')

        return redirect(url_for('register.signup'))

    return render_template('signup.html', form=form)