from flask import Flask, render_template, request, flash
from flask import redirect, url_for, session
from flask import jsonify
import json

# Import other necessary modules
import sys
sys.path.append('/Users/clementdureuil/Downloads/2A/TDLOG/Projet TD LOG FINAL/PROJET-GCYF/src')

import pandas as pd
from src import financeProg
from src.financeProg import *
from scipy.stats import norm
import numpy as np
import os


app = Flask(__name__)
from src.portefeuille import Porte_feuille

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Chemin vers la base de données
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)

migrate = Migrate(app, db) 

# Modèle de l'utilisateur


# Créer la base de données (s'il n'existe pas encore)
with app.app_context():
    db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=500.0)   
    stock_portfolio = db.Column(db.JSON, default={})
    european_option_portfolio = db.Column(db.JSON, default={'option_name':'AAPL', 'number_of_option_eur':2})
    american_option_portfolio = db.Column(db.JSON, default={})


@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    if 'user_id' in session:
        user_id = session['user_id']
        print(user_id)
        user = User.query.get(user_id)
        number_of_stocks = int(request.form.get('stock_number_buy'))

        new_stock_portfolio = user.stock_portfolio.copy()
        # Get the stock name and validate it (you may add additional validation)
        stock_name = request.form.get('stock_name_buy')
        print(stock_name)

        if not stock_name:
            return "Invalid stock name."

        # Get the current price of the stock using the prix_actuelle function
        stock_price = prix_actuelle(stock_name)
        print('stock_price = ', stock_price)

        # Check if the user has enough balance to buy the stock
        if user.balance >= number_of_stocks * stock_price:
            # Deduct the stock price from the user's balance
            user.balance -= number_of_stocks * stock_price
            print('user.balance after purchase:', user.balance)

            user = User.query.get(user_id)
            # Update the user's portfolio
            if stock_name in user.stock_portfolio:
                new_stock_portfolio[stock_name] += number_of_stocks
            else:
                new_stock_portfolio[stock_name] = number_of_stocks

            user.stock_portfolio = new_stock_portfolio    
            # Commit changes to the database after making all updates
            db.session.commit()

            print('user.stock_portfolio after purchase:', user.stock_portfolio)

            flash(f"Achat réussi! Tu as acheté {number_of_stocks} actions de {stock_name} cotées {stock_price}€ pour un total de {number_of_stocks * stock_price}€ ")
            return render_template('actions.html', username=user.username, balance=user.balance, stock_portfolio=user.stock_portfolio, real_user=user)
        else:
            flash(f"Solde insuffisant pour acheter cette action.")
            return render_template('actions.html', username=user.username, balance=user.balance, stock_portfolio=user.stock_portfolio, real_user=user)
    return redirect(url_for('login'))

@app.route('/sell_stock', methods=['POST'])
def sell_stock():
    if 'user_id' in session:
        user_id = session['user_id']
        print(user_id)
        user = User.query.get(user_id)
        number_of_stocks = int(request.form.get('stock_number_sell'))
        new_stock_portfolio = user.stock_portfolio.copy()
        # Get the stock name and validate it (you may add additional validation)
        stock_name = request.form.get('stock_name_sell')
        print(stock_name)
        if not stock_name:
            return "Invalid stock name."

        # Get the current price of the stock using the prix_actuelle function
        stock_price = prix_actuelle(stock_name)
        print('stock_price = ', stock_price)

        if stock_name in user.stock_portfolio and new_stock_portfolio[stock_name]>=number_of_stocks:
            user.balance += number_of_stocks * stock_price
            print('user.balance after selling:', user.balance)
            user = User.query.get(user_id)
            #actualise les number of stocks
            new_stock_portfolio[stock_name] -= number_of_stocks

            #on cactualise la db
            user.stock_portfolio = new_stock_portfolio    
            # Commit changes to the database after making all updates
            db.session.commit()

            print('user.stock_portfolio after purchase:', user.stock_portfolio)

            flash(f"Vente réussie! Tu as vendu {number_of_stocks} actions de {stock_name} cotées {stock_price}€ pour un total de {number_of_stocks * stock_price}€ ")
            return render_template('actions.html', username=user.username, balance=user.balance, stock_portfolio=user.stock_portfolio, real_user=user)
        
        else:
            flash(f"Nombre d'actions dans le portefeuille insuffisant pour vendre ce nombre d'actions.")
            return render_template('actions.html', username=user.username, balance=user.balance, stock_portfolio=user.stock_portfolio, real_user=user)
    return redirect(url_for('login'))

@app.route('/sell_european_option', methods=['POST'])
def sell_european_option():
    if 'user_id' in session:
        user_id = session['user_id']
        print(user_id)
        user = User.query.get(user_id)

        option_name = request.form.get('option_name_sell_eur')
        number_of_option_eur= int(request.form.get('number_of_option_sell_eur'))
        
        K = int(request.form.get('K_sell_eur'))
        T = int(request.form.get('T_sell_eur'))
        sigma = prix_de_cloture_passé(option_name)

        new_european_option_portfolio = user.european_option_portfolio.copy()
        # Get the stock name and validate it (you may add additional validation)
        
        print(option_name)
        if not option_name:
            return "Invalid stock name."

        # Get the current price of the stock using the prix_actuelle function
         
        sport_price= prix_actuelle(option_name)
        option_price= Black_Scholes(sport_price,K,0.05,T,sigma)
        
        print('option_price = ', option_price)

        # Check if the user has enough balance to buy the stock
        if user.balance >= number_of_option_eur * option_price:
            # Deduct the stock price from the user's balance
            user.balance -= number_of_option_eur * option_price
            print('user.balance after purchase:', user.balance)

            user = User.query.get(user_id)
            # Update the user's portfolio
            if option_name in user.european_option_portfolio and new_european_option_portfolio[option_name]>=number_of_option_eur:
                user.balance += number_of_option_eur * option_price
                print('user.balance after selling:', user.balance)
                user = User.query.get(user_id)
                #actualise les number of stocks
                new_european_option_portfolio[option_name] -= number_of_option_eur

                #on cactualise la db
                user.european_option_portfolio = new_european_option_portfolio    
                # Commit changes to the database after making all updates
                db.session.commit()

            print('user.stock_portfolio after purchase:', user.european_option_portfolio)

            flash(f"Achat réussi! Tu as vendu {number_of_option_eur} actions de {option_name} cotées {option_price}€ pour un total de {number_of_option_eur * option_price}€ ")
            return render_template('european.html', username=user.username, balance=user.balance, european_option_portfolio=user.european_option_portfolio, real_user=user)
        else:
            flash(f"pas assez d'options dans ton portefeuille.")
            return render_template('european.html', username=user.username, balance=user.balance, european_option_portfolio=user.european_option_portfolio, real_user=user)
    return redirect(url_for('login'))

@app.route('/buy_european_option', methods=['POST'])
def buy_european_option():
    if 'user_id' in session:
        user_id = session['user_id']
        print(user_id)
        user = User.query.get(user_id)

        option_name = request.form.get('option_name_buy_eur')
        number_of_option_eur= int(request.form.get('number_of_option_buy_eur'))
        
        K = int(request.form.get('K_buy_eur'))
        T = int(request.form.get('T_buy_eur'))
        sigma = prix_de_cloture_passé(option_name)

        new_european_option_portfolio = user.european_option_portfolio.copy()
        # Get the stock name and validate it (you may add additional validation)
        
        print(option_name)
        if not option_name:
            return "Invalid stock name."

        # Get the current price of the stock using the prix_actuelle function
         
        sport_price= prix_actuelle(option_name)
        option_price= Black_Scholes(sport_price,K,0.05,T,sigma)
        
        print('option_price = ', option_price)

        # Check if the user has enough balance to buy the stock
        if user.balance >= number_of_option_eur * option_price:
            # Deduct the stock price from the user's balance
            user.balance -= number_of_option_eur * option_price
            print('user.balance after purchase:', user.balance)

            user = User.query.get(user_id)
            # Update the user's portfolio
            if option_name in user.european_option_portfolio:
                new_european_option_portfolio[option_name] += number_of_option_eur
            else:
                new_european_option_portfolio[option_name] = number_of_option_eur

            user.european_option_portfolio = new_european_option_portfolio    
            # Commit changes to the database after making all updates
            db.session.commit()

            print('user.stock_portfolio after purchase:', user.stock_portfolio)

            flash(f"Achat réussi! Tu as acheté {number_of_option_eur} actions de {option_name} cotées {option_price}€ pour un total de {number_of_option_eur * option_price}€ ")
            return render_template('european.html', username=user.username, balance=user.balance, european_option_portfolio=user.european_option_portfolio, real_user=user)
        else:
            flash(f"Solde insuffisant pour acheter cette action.")
            return render_template('european.html', username=user.username, balance=user.balance, european_option_portfolio=user.european_option_portfolio, real_user=user)
    return redirect(url_for('login'))

@app.route('/sell_american_option', methods=['POST'])
def sell_ammerican_option():
    if 'user_id' in session:
        user_id = session['user_id']
        print(user_id)
        user = User.query.get(user_id)

        option_name = request.form.get('option_name_sell_am')
        number_of_option_am= int(request.form.get('number_of_option_sell_am'))
        
        K = int(request.form.get('K_sell_am'))
        T = int(request.form.get('T_sell_am'))
        sigma = prix_de_cloture_passé(option_name)

        new_american_option_portfolio = user.american_option_portfolio.copy()
        # Get the stock name and validate it (you may add additional validation)
        
        print(option_name)
        if not option_name:
            return "Invalid stock name."

        # Get the current price of the stock using the prix_actuelle function
         
        sport_price= prix_actuelle(option_name)
        option_price= Black_Scholes(sport_price,K,0.05,T,sigma)
        
        print('option_price = ', option_price)

        # Check if the user has enough balance to buy the stock
        if user.balance >= number_of_option_am * option_price:
            # Deduct the stock price from the user's balance
            user.balance -= number_of_option_am * option_price
            print('user.balance number_of_option_am purchase:', user.balance)

            user = User.query.get(user_id)
            # Update the user's portfolio
            if option_name in user.european_option_portfolio and new_american_option_portfolio[option_name]>=number_of_option_am:
                user.balance += number_of_option_am * option_price
                print('user.balance after selling:', user.balance)
                user = User.query.get(user_id)
                #actualise les number of stocks
                new_american_option_portfolio[option_name] -= number_of_option_am

                #on cactualise la db
                user.european_option_portfolio = new_american_option_portfolio    
                # Commit changes to the database after making all updates
                db.session.commit()

            print('user.stock_portfolio after purchase:', user.american_option_portfolio)

            flash(f"Achat réussi! Tu as vendu {number_of_option_am} actions de {option_name} cotées {option_price}€ pour un total de {number_of_option_am * option_price}€ ")
            return render_template('american.html', username=user.username, balance=user.balance, european_option_portfolio=user.american_option_portfolio, real_user=user)
        else:
            flash(f"pas assez d'options dans ton portefeuille.")
            return render_template('american.html', username=user.username, balance=user.balance, european_option_portfolio=user.american_option_portfolio, real_user=user)
    return redirect(url_for('login'))



@app.route('/add_money', methods=['POST'])
def add_money():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)

        # Get the amount to add and validate it (you may add additional validation)
        amount_to_add = request.form.get('amount')
        if not amount_to_add:
            return "Invalid amount."

        # Add the amount to the user's balance
        user.balance += float(amount_to_add)

        # Commit changes to the database
        db.session.commit()

        flash(f"Montant ajouté avec succès! Nouveau solde: {user.balance} euros.")
        return render_template('index.html', username=user.username, balance=user.balance, stock_portfolio=user.stock_portfolio, real_user=user)

    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'user_id' in session:
        # Retrieve the user's information from the database
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if user:
            portfolio_value = user.stock_portfolio
            
        else : 
            flash("User not found.")
            return redirect(url_for('login'))        

        # Render the template with the portfolio value
        return render_template('index.html', username=user.username, balance=user.balance, portfolio_value=portfolio_value, stock_portfolio=user.stock_portfolio, real_user=user)
    else:
        return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Cet utilisateur existe déjà !"
        
        # Créer un nouvel utilisateur
        new_user = User(username=username, password=password, balance=500)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        
        return "Identifiant ou mot de passe incorrect."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


####ajout de yentl
@app.route("/actions")
def actions():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    return render_template("actions.html",username=user.username, balance=user.balance, stock_portfolio=user.stock_portfolio, real_user=user)



#####fin ajout
@app.route("/pricer")
def pricer():
    return render_template("pricer.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")



@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(os.path.join(os.path.expanduser("~/Desktop/hackaton flask"), file.filename))
    return {"success": True}


@app.route('/stock_data')
def stock_data():
    # Code pour récupérer les données du cours de l'action
    L, V = plot_yesterday_stock('AAPL')
    stock_data = {
        "labels": L,
        "values": V
    }
    return jsonify(stock_data)



@app.route('/choix_option', methods=['POST'])
def choix_option():
    option = request.form['option']

    if option == 'americaine':
        return redirect(url_for('american'))
    elif option == 'europenne':
        return redirect(url_for('european'))

@app.route('/american')
def american():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    return render_template('american.html', username=user.username, balance=user.balance, american_option_portfolio=user.american_option_portfolio, real_user=user)

@app.route('/european')
def european():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    return render_template('european.html', username=user.username, balance=user.balance, european_option_portfolio=user.european_option_portfolio, real_user=user)


from formule import Black_Scholes, american_call_option_price, monte_carlo_american_call
from src.financeProg import prix_de_cloture_passé, symbol, key, prix_actuelle


@app.route("/resultat_european", methods=["POST"])
def resultat_european():
    try:        
        K = float(request.form["strike_K_eur"])
        r = float(request.form["taux_r_eur"])
        T = float(request.form["maturity_T_eur"])  
        stock_name = str(request.form["stock_symbol"])

        S0 = prix_actuelle(stock_name)
        sigma = prix_de_cloture_passé(stock_name)

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

        S0=prix_actuelle(stock_name)
        sigma = prix_de_cloture_passé(stock_name)              
        resultat_americaine = american_call_option_price(S0, K, r, T, sigma, 300)

        return render_template(
            "resultat_americaine.html", resultat_americaine=resultat_americaine
        )
    except ValueError as e:
        return render_template("error.html", error_message=str(e))


if __name__ == '__main__':
    app.run(debug=True)