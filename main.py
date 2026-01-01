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

def transform_products(df):
    df = df.copy()
    cols_drop = ["images", "thumbnail", "description", "tags", "reviews"]
    df.drop(columns = cols_drop, inplace=True, axis=1, errors='ignore')
    df.rename(columns = { 
        "title": "product_name",
        "price": "price_usd",
        "discountPercentage": "discount_pct"
    }, inplace=True)
    
    df["final_price"] = df["price_usd"] * (1 - df["discount_pct"] / 100)
    df["final_price"] = df["final_price"].round(2)
    df["rating"] = df["rating"].astype(float)
    df["stock"] = df["stock"].astype(int)

    df.fillna({
        "brand": "Unknown",
        "category": "Unknown"
    }, inplace=True)
    
    # df["final_price"] = df["final_price"].apply(lambda x: f"${x}")
    # df["discount_pct"] = df["discount_pct"].apply(lambda x: f"{x}%")

    return df
df_raw = extract_products()
df_clean = transform_products(df_raw)
print(df_clean.head())