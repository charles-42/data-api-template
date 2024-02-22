import pandas as pd
import sqlite3
from utils import import_clean_dataset

connection = sqlite3.connect("olist.db")

df = import_clean_dataset()

# Creation de la variable score
df['score'] = df['review_score'].apply(lambda x : 1 if x==5 else 0)
df["temps_livraison"] = (df.order_delivered_customer_date - df.order_purchase_timestamp).dt.days
df["retard_livraison"] = (df.order_delivered_customer_date - df.order_estimated_delivery_date).dt.days

def f(x):
    (delivered_date,review_date)=x
    if pd.isna(delivered_date):
        return 0
    elif delivered_date.normalize()>review_date:
        return 0
    else:
        return 1

df['produit_recu'] = df[["order_delivered_customer_date","review_creation_date"]].apply(f, axis=1)

df["order_status"] = df["order_status"].apply(lambda x: "unavailable" if x in ["created","approved"] else x)


df.to_sql('TrainingDataset', connection, index=False, if_exists='replace')

print("Table TrainingDataset mise à jour")

connection.close()