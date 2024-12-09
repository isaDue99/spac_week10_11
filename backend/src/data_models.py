# module providing classes to structure data being sent to and received from database

# TODO TODO TODO brain is cooked....

# ------------ Products ------------ 

class ProductImage:
    # TODO
    file : str

class Product:
    id : int
    name : str
    # price : float
    # currency : str
    price : dict[str, float] # {'DKK' : 19.95, 'EUR' : 2, 'USD' : 2.75}
    stock : int
    image : ProductImage

class Food(Product):
    ingredients : list[str]
    unit_weight : int
    
    # nutritional info (per 100 g)
    calories : int
    protein : int
    fat : int
    carbs : int
    sugars : int
    fiber : int
    sodium : int
    potassium : int
    vitamins : int

class Cereal(Food):
    mascot : str


# ------------ Customer ------------ 

class Customer:
    id : int
    
class Order:
    customer_id : int
    cart : dict[int, int] # {(product id) : (amount bought), (other product id) : etc..}

    def total_price(self):
        # loop thru product ids in cart and add up cart[product id].value * product.price
        pass