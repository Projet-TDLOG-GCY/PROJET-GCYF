from flask import Flask, render_template, request
from flask import redirect, url_for
from flask import jsonify


# Import other necessary modules
import sys
sys.path.append('/Users/clementdureuil/Downloads/2A/TDLOG/Projet TD LOG FINAL/PROJET-GCYF/src')

import pandas as pd
from src import financeProg
from src.financeProg import fonction, fonction_2
from src.financeProg import plot_yesterday_stock




from scipy.stats import norm

import numpy as np
import os


app = Flask(__name__)

@app.route("/")
def hello(name=None):
    return render_template("index.html", name=name)

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

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/stock_data/<symbol>/<Nom_Symbol>')
def stock_data(symbol, Nom_Symbol):
    if (Nom_Symbol== "Nom"):
        Real_Symbol = fonction_2(symbol)
    else:
        Real_Symbol = symbol
    # Code pour récupérer les données du cours de l'action
    L, V = fonction(Real_Symbol)
    stock_data = {
        "labels": L,
        "values": V,
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
    return render_template('american.html')

@app.route('/european')
def european():
    return render_template('european.html')

def Black_Scholes(S0, K, r, T, sigma):
    d1 = ( np.log(S0/K) + ( r + 0.5* sigma**2 ) * T ) / (sigma * np.sqrt(T) )
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp( -r * T ) * norm.cdf(d2)


@app.route('/resultat_european', methods=['POST'])
def resultat_european():
    try:
        # Validate numerical inputs
        K = float(request.form["strike_K_eur"])
        r = float(request.form["taux_r_eur"])
        T = float(request.form["maturity_T_eur"])
        S0 = float(request.form["spot_price_0_eur"])

        stock_name=str(request.form["stock_symbol"])
        
        sigma = prix_de_cloture_passé(stock_name, key)
        
        resultat_european=Black_Scholes(S0, K, r, T, sigma)
        return render_template("resultat_european.html", resultat_european=resultat_european)

    except ValueError as e:
        return render_template("error.html", error_message=str(e))


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

@app.route('/resultat_americaine', methods=['POST'])
def resultat_americaine():
    try:
        # Validate numerical inputs
        K = float(request.form["strike_K"])
        r = float(request.form["taux_r"])
        T = float(request.form["maturity_T"])
        S0 = float(request.form["spot_price_0"])
        num_periods = int(request.form["number_of_period"])
        volatility=float(request.form["volatility_american"])
        

        u=np.exp(volatility*np.sqrt(T))
        d=1/u
        resultat_americaine=Cox_Ross(K,S0,r,T,num_periods,u,d)

        return render_template("resultat_americaine.html", resultat_americaine=resultat_americaine)
            
    except ValueError as e:
        return render_template("error.html", error_message=str(e))


