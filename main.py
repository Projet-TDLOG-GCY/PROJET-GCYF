from flask import Flask, render_template, request
from flask import redirect, url_for, session
from flask import jsonify

import pandas as pd
# Import other necessary modules
import os
import sys
# Obtenez le chemin du dossier courant
chemin_courant = os.path.dirname(os.path.abspath(__file__))

# Construisez le chemin relatif vers le dossier 'src'
chemin_src = os.path.join(chemin_courant, 'PROJET-GCYF', 'src')

# Ajoutez le chemin à sys.path
sys.path.append(chemin_src)

import pandas as pd
from src import financeProg
from src.financeProg import plot_yesterday_stock




from scipy.stats import norm

import numpy as np
import os


app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Chemin vers la base de données
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)

# Modèle de l'utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=100.0)

# Créer la base de données (s'il n'existe pas encore)
with app.app_context():
    db.create_all()


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
        new_user = User(username=username, password=password)
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


@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return render_template('index.html', username=user.username, balance=user.balance)
        else:
            return "Utilisateur introuvable."
    else:
        return redirect(url_for('login'))



@app.route("/about_us")
def about_us():
    return render_template("about_us.html")


@app.route("/actions")
def actions():
    return render_template("actions.html")

@app.route('/stock_data/<symbol>/<Nom_Symbol>')
def stock_data(symbol, Nom_Symbol):
    if (Nom_Symbol== "Nom"):
        Real_Symbol = nom_marque_to_symbol(symbol)
    else:
        Real_Symbol = symbol
    # Code pour récupérer les données du cours de l'action
    L, V = plot_yesterday_stock(Real_Symbol)
    stock_data = {
        "labels": L,
        "values": V,
    }
    return jsonify(stock_data)



@app.route('/american')
def american():
    return render_template('american.html')

@app.route('/prix_americain/<maturity>')
def prix_americain(maturity):
    resultat_americaine = 0  # Initialisez à None pour gérer l'affichage conditionnel dans le template

    # Validate and process form data
    K = 4#float(request.form["strike_K"])
    r = 3#float(request.form["taux_r"])
    T = 0#float(maturity)
    S0 = 4#float(request.form["spot_price_0"])
    num_periods = 2#int(request.form["number_of_period"])
    volatility = 3#float(request.form["volatility_american"])

    u = 2#np.exp(volatility * np.sqrt(T))
    d = 1 / u
    resultat_americaine = maturity #Cox_Ross(K, S0, r, T, num_periods, u, d)
    
    return jsonify(resultat_americaine=resultat_americaine)

@app.route('/european')
def european():
    return render_template('european.html')

def Black_Scholes(S0, K, r, T, sigma):
    d1 = ( np.log(S0/K) + ( r + 0.5* sigma**2 ) * T ) / (sigma * np.sqrt(T) )
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp( -r * T ) * norm.cdf(d2)




##Pricing of an american option 

    #Cox Ross method with a binomial tree

def Cox_Ross(K,S0,r,T,num_periods,u,d):

    dt = T / num_periods
    q = (np.exp(r * dt) - d) / (u - d)
    disc = np.exp(-r * dt)

    # Initialization of the price at maturity
    S = S0 * d**(np.arange(num_periods, -1, -1)) * u**(np.arange(0, num_periods + 1, 1))

    # Payoff of the option
    C = np.maximum(0, K - S)

    for i in np.arange(num_periods - 1, -1, -1):
        S = S0 * d**(np.arange(int(i), -1, -1)) * u**(np.arange(0, int(i) + 1, 1))
        C_new = disc * (q * C[1:int(i) + 2] + (1 - q) * C[0:int(i) + 1])
        C = np.maximum(C_new, K - S)
    return C[0]


# @app.route('/resultat_americaine', methods=['POST'])
# def resultat_americaine():
#     try:
#         # Validate numerical inputs
#         K = float(request.form["strike_K"])
#         r = float(request.form["taux_r"])
#         T = float(request.form["maturity_T"])
#         S0 = float(request.form["spot_price_0"])
#         num_periods = float(request.form["number_of_period"])
#         u = float(request.form["up"])
#         d = float(request.form["down"])
        
#         resultat_americaine=Cox_Ross(K,S0,r,T,num_periods,u,d)
#         return render_template("resultat_americaine.html", resultat_americaine=resultat_americaine)

#     except ValueError as e:
#         return render_template("error.html", error_message=str(e))



    #Monte Carlo method

def monte_carlo_american_call(S0, K, r, sigma, T, paths):
    dt = T / paths
    option_prices = []

    for i in range(paths):
        prices = [S0]
        for j in range(1, paths):
            Z = np.random.normal(0, 1)
            S_next = prices[-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
            prices.append(S_next)        

        
        # Determine exercise opportunities
        payoffs = np.maximum(np.array(prices) - K, 0)

        # Backward induction for early exercise
        for j in range(paths - 2, 0, -1):
            payoffs[j] = np.maximum(payoffs[j], np.exp(-r * dt) * (0.5 * payoffs[j + 1] + 0.5 * payoffs[j]))
                    

        option_prices.append(payoffs[0])

    return np.mean(option_prices)



"""
@app.route('/ajouter-argent', methods=['POST'])
def ajouter_argent():
    montant = request.form['montant']
    mon_portefeuille.ajouter_argent(float(montant))
    return render_template('index.html', message="Argent ajouté avec succès!")

@app.route('/acheter', methods=['POST'])
def acheter_action():
    symbol = request.form['symbol']
    nombre = int(request.form['nombre'])
    mon_portefeuille.acheter_action(symbol, nombre)
    return render_template('index.html', message="Achat réalisé avec succès!")

@app.route('/vendre', methods=['POST'])
def vendre_action():
    symbol = request.form['symbol']
    nombre = int(request.form['nombre'])
    mon_portefeuille.vendre_action(symbol, nombre)
    return render_template('index.html', message="Vente réalisée avec succès!")
"""
      
file_path = os.path.join(os.path.dirname(__file__), 'nouveau_actions.txt')

with open(file_path, 'r') as file:
    stocks_data = [line.strip().split(': ') for line in file]

stocks = [stocks_data[i][1] for i in range(len(stocks_data))]
noms=[stocks_data[i][0] for i in range(len(stocks_data))]

@app.route('/get_stock_suggestions')
def get_stock_suggestions():
    input_prefix = request.args.get('input', '').lower()

    # Filter stocks based on input prefix
    suggestion = []
    for i in stocks:
        if i.lower().startswith(input_prefix):
            suggestion.append(i)
    return jsonify(suggestion)


@app.route('/get_stock_suggestions_noms')
def get_stock_suggestions_noms():
    input_prefix = request.args.get('input', '').lower()

    # Filter stocks based on input prefix
    suggestion = []
    for i in noms:
        if i.lower().startswith(input_prefix):
            suggestion.append(i)
    return jsonify(suggestion)