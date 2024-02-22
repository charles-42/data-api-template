-- Execute this command to create the tables
-- sqlite3 olist.db < database_building/create_table.sql

-- Create table StateName
CREATE TABLE IF NOT EXISTS StateName (
    state TEXT PRIMARY KEY,
    state_name TEXT 
);

-- .import --csv --skip 1 -v data/state_name.csv StateName


-- Create a table for Geolocalisation
CREATE TABLE IF NOT EXISTS Geolocation (
    geolocation_zip_code_prefix TEXT PRIMARY KEY,
    geolocation_lat REAL,
    geolocation_lng REAL,
    geolocation_city TEXT,
    geolocation_state TEXT,
    FOREIGN KEY (geolocation_state) REFERENCES StateName(state)
);

-- .import --csv --skip 1 -v data/geolocation_dataset.csv Geolocation



-- Create a table for Customers
CREATE TABLE IF NOT EXISTS Customers (
    customer_id TEXT PRIMARY KEY,
    customer_unique_id TEXT,
    customer_zip_code_prefix TEXT,
    customer_city TEXT ,
    customer_state TEXT,
    FOREIGN KEY (customer_zip_code_prefix) REFERENCES Geolocation(geolocation_zip_code_prefix)
);

-- .import --csv --skip 1 -v data/customers_dataset.csv Customers

-- Create table Sellers
CREATE TABLE IF NOT EXISTS Sellers (
    seller_id TEXT PRIMARY KEY,
    seller_zip_code_prefix TEXT ,
    seller_city TEXT,
    seller_state TEXT,
    FOREIGN KEY (seller_zip_code_prefix) REFERENCES Geolocation(geolocation_zip_code_prefix)
);

-- .import --csv --skip 1 -v data/sellers_dataset.csv Sellers

-- Create table Orders
CREATE TABLE IF NOT EXISTS Orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT ,
    order_status INTEGER,
    order_purchase_timestamp TEXT,
    order_approved_at TEXT,
    order_delivered_carrier_date TEXT,
    order_delivered_customer_date TEXT,
    order_estimated_delivery_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- .import --csv --skip 1 -v data/orders_dataset.csv Orders



-- Create table ProductCategoryName
CREATE TABLE IF NOT EXISTS ProductCategoryName (
    product_category_name TEXT PRIMARY KEY,
    product_category_name_english TEXT 
);

-- .import --csv --skip 1 -v data/product_category_name_translation.csv ProductCategoryName


-- Create table Products
CREATE TABLE IF NOT EXISTS Products (
    product_id TEXT PRIMARY KEY,
    product_category_name TEXT ,
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER,
    product_weight_g INTEGER,
    product_length_cm INTEGER,
    product_height_cm INTEGER,
    product_width_cm INTEGER,
    FOREIGN KEY (product_category_name) REFERENCES ProductCategoryName(product_category_name)
);

-- .import --csv --skip 1 -v data/products_dataset.csv Products




-- Create table Order_items
CREATE TABLE IF NOT EXISTS OrderItem (
    order_id TEXT  ,
    order_item_id INTEGER ,
    product_id TEXT,
    seller_id TEXT,
    shipping_limit_date TEXT,
    price REAL,
    freight_value REAL,
    PRIMARY KEY (order_id,order_item_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- .import --csv --skip 1 -v data/order_items_dataset.csv OrderItem




-- Create table Paiements
CREATE TABLE IF NOT EXISTS Payments (
    order_id TEXT  ,
    payment_sequential INTEGER ,
    payment_type TEXT,
    payment_installments INTEGER,
    payment_value REAL,
    PRIMARY KEY (order_id,payment_sequential),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- .import --csv --skip 1 -v data/order_payments_dataset.csv Payments



-- Create table Reviews
CREATE TABLE IF NOT EXISTS Reviews (
    review_id TEXT PRIMARY KEY,
    order_id TEXT ,
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TEXT,
    review_answer_timestamp TEXT,
    timestamp_field_7 TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- .import --csv --skip 1 -v data/order_review_dataset_clean.csv Reviews


