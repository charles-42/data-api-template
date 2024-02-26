import sqlite3


def get_database():
    connection = sqlite3.connect('olist.db')
    return connection

def close_database(connection: sqlite3.Connection):
    connection.close()


if __name__ == "__main__":
    conn = get_database()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, customer_unique_id FROM Customers LIMIT 10")
    reviews = cursor.fetchall()
    print(reviews)



