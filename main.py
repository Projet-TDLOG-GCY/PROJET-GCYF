from flask import Flask, render_template, request,  Blueprint, flash, redirect, url_for
from .models import User 
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from .src.financeProg import prix_de_cloture_passé, symbol, key, prix_actuelle 
from scipy.stats import norm
import numpy as np
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


sys.path.append(
    "/Users/clementdureuil/Downloads/2A/TDLOG/Projet TD LOG FINAL/PROJET-GCYF/src"
)

app = Flask(__name__)

#########################

from .register import register_bp
from .models import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)



# Register the blueprint
app.register_blueprint(register_bp)



@app.route('/signup', methods=['POST'])
def signup():
    user_id = request.form.get('email')
    password = request.form.get('password1')

    print(f'Received data: email={user_id}, password1={password}')

    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password, method='sha256')

    # Create a new user
    new_user = User(id=user_id, password=hashed_password)

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful! You can now log in.', 'success')
    return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def login():    
    if request.method == "POST":
        user_id = request.form.get("id")
        password = request.form.get("password")
        user = User.query.filter_by(id=user_id).first()

        if user and check_password_hash(user.password, password):
            # Login user
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("hello"))
        else:
            flash("Login failed. Please check your credentials or sign up.", "danger")

    return render_template("login.html")


@app.route("/")
def hello(name=None):
    return render_template("index.html", name=name)


@app.route("/pricer")
def pricer():
    return render_template("pricer.html")


@app.route("/about_us")
def about_us():
    return render_template("about_us.html")



@app.route("/choix_option", methods=["POST"])
def choix_option():
    option = request.form["option"]

    if option == "americaine":
        return redirect(url_for("american"))
    elif option == "europenne":
        return redirect(url_for("european"))


@app.route("/american")
def american():
    return render_template("american.html")


@app.route("/european")
def european():
    return render_template("european.html")



#########################
from .formule import Black_Scholes, american_call_option_price


@app.route("/resultat_european", methods=["POST"])
def resultat_european():
    try:        
        K = float(request.form["strike_K_eur"])
        r = float(request.form["taux_r_eur"])
        T = float(request.form["maturity_T_eur"])  
        stock_name = str(request.form["stock_symbol"])

        S0=prix_actuelle(stock_name,key)
        sigma = prix_de_cloture_passé(stock_name, key)
        resultat_european = Black_Scholes(S0, K, r, T, sigma)

        return render_template(
            "resultat_european.html", resultat_european=resultat_european
        )

    except ValueError as e:
        return render_template("error.html", error_message=str(e))


@app.route("/resultat_americaine", methods=["POST"])
def resultat_americaine():
    try:      
        K = float(request.form["strike_K"])
        r = float(request.form["taux_r"])
        T = float(request.form["maturity_T"])       
        
        stock_name = str(request.form["stock_symbol_am"])

        S0=prix_actuelle(stock_name,key)
        sigma = prix_de_cloture_passé(stock_name, key)              
        resultat_americaine = american_call_option_price(S0, K, r, T, sigma, 300)

        return render_template(
            "resultat_americaine.html", resultat_americaine=resultat_americaine
        )
    except ValueError as e:
        return render_template("error.html", error_message=str(e))


if __name__ == '__main__':
    app.run(debug=True)


