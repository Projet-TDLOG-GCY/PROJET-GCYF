from flask import Flask
from flask import render_template
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


from flask import request
from src.ask_question_to_pdf import (
    ask_question_to_pdf,
    gpt3_completion,
    gpt3_completion_context,
    verification,
)


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
    file.save(
        os.path.join(os.path.expanduser("~/Desktop/hackaton flask"), file.filename)
    )
    return {"success": True}


@app.route("/")
def index():
    return render_template("index.html")


from flask import Flask, render_template, request
from scipy.stats import norm

@app.route("/calculate-cdf", methods=["POST"])
def calculate_cdf():
    try:
        # Récupère les valeurs depuis les champs de formulaire
        K = float(request.form["strike K"])
        r= float(request.form["taux r"])

        # Vérifie si les valeurs sont des nombres valides
        if not (r and K):
            raise ValueError("Veuillez saisir des nombres valides pour les paramètres.")

        # Calcule la somme
        sum_result = r+K

        # Calcul de la CDF pour illustrer l'exemple
        cdf_result = norm.cdf(sum_result)

        # Renvoie le résultat, y compris la CDF
        return render_template("result.html", sum_result=sum_result, cdf_result=cdf_result)

    except ValueError as e:
        # Gère le cas où les valeurs d'entrée ne sont pas valides
        return render_template("error.html", message=str(e))

# ... (autres routes)

if __name__ == "__main__":
    app.run()



