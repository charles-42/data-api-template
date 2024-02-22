import pandas as pd
import sqlite3
import numpy as np

connection = sqlite3.connect("olist.db")

df_reviews = pd.read_sql_query("SELECT * FROM Reviews",connection)


# Gestion valeurs manquantes
df_reviews = df_reviews.drop(["timestamp_field_7"],axis=1)

if df_reviews.shape[1]!= 7:
    raise ValueError("Le nombre de colonnes ne correspond pas")
else:
    print("Valeurs manquantes: OK")

# Gestion des doublons
df_reviews = df_reviews.drop_duplicates(['order_id','review_score','review_comment_title','review_comment_message','review_creation_date'])


# Changement des types
df_reviews.review_creation_date = pd.to_datetime(df_reviews['review_creation_date'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")
df_reviews.review_answer_timestamp = pd.to_datetime(df_reviews['review_answer_timestamp'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")

from numpy import dtype


if df_reviews.dtypes['review_creation_date'] != dtype('<M8[ns]') or df_reviews.dtypes['review_answer_timestamp'] != dtype('<M8[ns]'):
    raise ValueError("Les dates ne sont pas au bon format")
else:
    print("Gestion des dates: OK")

#Changement des valeurs types pour les dates
df_reviews = df_reviews.dropna(subset=['review_creation_date','review_answer_timestamp'])

# Jointure avec la Table Orders
df_orders = pd.read_sql_query("SELECT * FROM Orders",connection)
df = df_reviews.merge(df_orders, how='left', on ='order_id')


# Gestion des types de data
df.order_purchase_timestamp = pd.to_datetime(df['order_purchase_timestamp'], 
                                            format= '%Y-%m-%d %H:%M:%S', 
                                            errors="coerce")

df.order_delivered_customer_date = pd.to_datetime(df['order_delivered_customer_date'], 
                                                  format= '%Y-%m-%d %H:%M:%S', 
                                                  errors="coerce")

df.order_estimated_delivery_date = pd.to_datetime(df['order_estimated_delivery_date'], 
                                                  format= '%Y-%m-%d %H:%M:%S', 
                                                  errors="coerce")


if df.dtypes['order_estimated_delivery_date'] != dtype('<M8[ns]') \
    or df.dtypes['order_delivered_customer_date'] != dtype('<M8[ns]')\
    or df.dtypes['order_estimated_delivery_date'] != dtype('<M8[ns]')    :
    raise ValueError("Les dates ne sont pas au bon format")
else:
    print("Gestion des dates (Orders): OK")

# Création des variables montant price et freight value

df_order_item = pd.read_sql_query("SELECT * FROM OrderItem",connection)

df_montant_global = df_order_item[["order_id","price","freight_value"]].groupby("order_id").sum()

df = df.merge(df_montant_global, how='left', on ='order_id')

print("Création de total_price et total_freight_value")

# Récupération des variables description, photo

df_products = pd.read_sql_query("SELECT * FROM Products",connection)

df_item_product = df_order_item[['order_id','product_id']].merge(df_products, how='left', on ='product_id')
df_item_product["product_photos_qty"] = df_item_product["product_photos_qty"].replace("","0").astype("int")
df_item_product["product_description_lenght"] = df_item_product["product_description_lenght"].replace("","0").astype("int")

df_item_product_group_by = df_item_product[['order_id','product_photos_qty','product_description_lenght']].groupby('order_id').mean()


df_item_product_group_by = df_item_product_group_by.reset_index()

df = df.merge(df_item_product_group_by,how='left')

#Création de la table CleanDataset

df.to_sql('CleanDataset', connection, index=False, if_exists='replace')

print("Table CleanDataset mise à jour")

connection.close()