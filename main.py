import requests
import pandas as pd
from datetime import datetime
def extract_products():
    url = "https://dummyjson.com/products?limit=100"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data["products"])
        return df
    else:
        raise Exception("Erreur lors de l'extraction des données dans l'API")
extract_products()