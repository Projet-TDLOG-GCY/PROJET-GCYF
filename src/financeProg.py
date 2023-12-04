#Other libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from urllib.request import urlopen
from datetime import datetime
import requests
import matplotlib.pyplot as plt

key = "84b2859fb03d27f28125c365b0b8967d"

symbol = 'NKE'



def prix_de_cloture_passé(symbol, key):
    # URL de l'API pour récupérer les données historiques des prix d'une action
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={key}'

    # Effectuer la requête GET vers l'API
    response = requests.get(url)
    
    if response.status_code == 200:
        # Convertir la réponse en format JSON
        data = response.json()
        # Récupérer les prix de clôture
        historical_data = data['historical']

        # Extraire les dates et les prix de clôture pour le tracé
        dates = [entry['date'] for entry in historical_data]
        # Convertir les chaînes de date en objets datetime pour un meilleur affichage graphique
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

        closing_prices = [float(entry['close']) for entry in historical_data]

        # Tracer le graphique
        plt.figure(figsize=(10, 6))
        plt.plot(dates, closing_prices, linestyle='-')
        plt.title(f'Historique des prix de clôture pour {symbol}')
        plt.xlabel('Date')
        plt.ylabel('Prix de clôture')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print('Échec de la requête. Vérifiez votre clé API ou le symbole de l\'action.')

def prix_actuelle(symbol,key):
    current_price_url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={key}'

    response_current_price = requests.get(current_price_url)
    if response_current_price.status_code == 200:
        # Convertir la réponse en format JSON
        data_current_price = response_current_price.json()

        

        # Récupérer le prix actuel de l'action
        current_price = data_current_price[0]['price']

    else:
        print('Échec de la requête. Vérifiez votre clé API ou le symbole de l\'action.')

prix_de_cloture_passé(symbol, key)