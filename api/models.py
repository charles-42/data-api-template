from pydantic import BaseModel

# Pydantic models
class StateName(BaseModel):
    state: str
    state_name: str

class Geolocation(BaseModel):
    geolocation_zip_code_prefix: str
    geolocation_lat: float
    geolocation_lng: float
    geolocation_city: str
    geolocation_state: str

class Customer(BaseModel):
    customer_id: str
    customer_unique_id: str
    customer_zip_code_prefix: str
    customer_city: str
    customer_state: str

class Sellers(BaseModel):
    seller_id: str
    seller_zip_code_prefix: str
    seller_city: str
    seller_state: str

class Orders(BaseModel):
    order_id: str
    customer_id: str
    seller_city: str
    order_status: int
    order_purchase_timestamp: str
    order_approved_at: str
    order_delivered_carrier_date: str
    order_delivered_customer_date: str
    order_estimated_delivery_date: str

class ProductCategoryName(BaseModel):
    product_category_name: str
    product_category_name_english: str


class Products(BaseModel):
    product_id: str
    product_category_name: str
    product_name_lenght: int
    product_description_lenght: int
    product_photos_qty: int
    product_weight_g: int
    product_length_cm: int
    product_height_cm: int
    product_width_cm: int


class Order_items(BaseModel):
    order_id: str
    order_item_id: int
    product_id: str
    seller_id: str
    shipping_limit_date: str
    price: float
    freight_value: float

class Payments(BaseModel):
    order_id: str
    payment_sequential: int
    payment_type: str
    payment_installments: int
    payment_value: float

class Reviews(BaseModel):
    review_id: str
    order_id: str
    review_score: int
    review_comment_title: str
    review_comment_message: str
    review_creation_date: str
    review_answer_timestamp: str
    timestamp_field_7: str

