import pandas as pd
import sqlite3

def import_clean_dataset():

    connection = sqlite3.connect("olist.db")

    df = pd.read_sql_query("SELECT * FROM CleanDataset",connection)

    df.review_creation_date = pd.to_datetime(df['review_creation_date'], 
                                             format= '%Y-%m-%d %H:%M:%S', 
                                             errors="coerce")

    df.review_answer_timestamp = pd.to_datetime(df['review_answer_timestamp'], 
                                                format= '%Y-%m-%d %H:%M:%S', 
                                                errors="coerce")


    df.order_purchase_timestamp = pd.to_datetime(df['order_purchase_timestamp'], 
                                            format= '%Y-%m-%d %H:%M:%S', 
                                            errors="coerce")

    df.order_delivered_customer_date = pd.to_datetime(df['order_delivered_customer_date'], 
                                                    format= '%Y-%m-%d %H:%M:%S', 
                                                    errors="coerce")

    df.order_estimated_delivery_date = pd.to_datetime(df['order_estimated_delivery_date'], 
                                                    format= '%Y-%m-%d %H:%M:%S', 
                                                    errors="coerce")
    
    connection.close()

    return df