
from flask import Flask, render_template, request
from scipy.stats import norm
import numpy as np

import os
from src.ask_question_to_pdf import ask_question_to_pdf, gpt3_completion, gpt3_completion_context, verification

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

@app.route("/prompt", methods=["POST"])
def prompt():
    prompt = request.form["prompt"]
    return {"answer": gpt3_completion_context(prompt)}

@app.route("/question", methods=["GET"])
def question():
    return {"answer": ask_question_to_pdf("pose moi une question sur le texte")}

@app.route("/answer", methods=["POST"])
def answer():
    question = request.form["question"]
    prompt = request.form["prompt"]
    return {"answer": verification(question, prompt)}

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(os.path.join(os.path.expanduser("~/Desktop/hackaton flask"), file.filename))
    return {"success": True}

@app.route("/")
def index():
    return render_template("index.html")



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


@app.route('/resultat', methods=['POST'])
def calcul():
    try:
        # Validate numerical inputs
        K = float(request.form["strike_K"])
        r = float(request.form["taux_r"])
        T = float(request.form["maturity_T"])
        S0 = float(request.form["spot_price_0"])
        num_periods = float(request.form["number_of_period"])
        u = float(request.form["up"])
        d = float(request.form["down"])
        
        resultat=Cox_Ross(K,S0,r,T,num_periods,u,d)
        return render_template("resultat.html", resultat=resultat)

    except ValueError as e:
        return render_template("error.html", error_message=str(e))


def Black_Scholes(S0, K, r, T, sigma):
    d1 = ( np.log(S0/K) + ( r + 0.5* sigma**2 ) * T ) / (sigma * np.sqrt(T) )
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp( -r * T ) * norm.cdf(d2)