# module providing classes to structure data being sent to and received from database

# ------------ Products ------------ 

class ProductImage: 
    id : int # product id, FK
    image_path : str        # idk
    image_binary : bytes    # idk

class Product:
    id : int # PK
    name : str
    price : float
    currency : str
    # price : dict[str, float] # {'DKK' : 19.95, 'EUR' : 2, 'USD' : 2.75}
    stock : int
    image : ProductImage

class Cereal(Product):
    # ingredients : list[str]
    unit_weight : int
    
    # nutritional info (per 100 g)
    calories : int
    protein : float
    fat : float
    carbs : float
    sugars : float
    fiber : float
    sodium : float
    potassium : float
    vitamins : float


# ------------ Customers and Orders ------------ 

class Customer:
    id : int
    first_name : str
    last_name : str
    
class Order:
    id : int # id of the order, PK
    customer_id : int # FK
    cart : dict[int, int] # {(product id) : (amount bought), (other product id) : etc..}

    def total_price(self):
        # loop thru product ids in cart and add up cart[product id].value * product.price
        pass