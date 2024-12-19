# main script that starts frontend to interact with mysql database through flask api

from flask import Flask, render_template, redirect, url_for, request
import requests as rq

import frontend_config as f_conf
backend = f_conf.BACKEND_URL

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    # /index.html = long list of products w their: image, name, product category (type), price & currency, stock, buttons to add to cart?

    ### get data from backend
    # get all products
    prod_res = rq.get(f"{backend}/Products")
    products = prod_res.json()

    # get all images
    img_res = rq.get(f"{backend}/ProductImages")
    images = img_res.json()

    data = [{"product": p, "image": i} for p, i in zip(products, images)]
    
    return render_template('index.html', data=data)

@app.route('/where', methods=["GET"])
def index_filter():
    args = {
        request.args.get("key"): request.args.get("value")
    }

    ### get data from backend that matches search
    # get products
    prod_res = rq.get(f"{backend}/Products/where", params=args)
    products = prod_res.json()

    # get images of the products we got (this is gonna suck)
    images = []
    for prod in products:
        payload = {"ProductID": prod[0]}
        img_res = rq.get(f"{backend}/ProductImages/where", params=payload)
        images.append(img_res.json()[0])

    data = [{"product": p, "image": i} for p, i in zip(products, images)]
    
    return render_template('index.html', data=data)

# fuck this one
# @app.route('/where', methods=["GET"])
# def index_filter_prop():
#     args = {
#         request.args.get("key"): request.args.get("value")
#     }
#     print(args)

#     ### get data from backend that matches search
#     # get properties that match search
#     prop_res = rq.get(f"{backend}/Properties/where", params=args)
#     properties = prop_res.json()

#     # get product ids from those properties (this is gonna suck)


#     # get products of those properties
#     prod_res = rq.get(f"{backend}/Products/where", params=args)
#     products = prod_res.json()

#     # get images of the products we got
#     images = []
#     for prod in products:
#         payload = {"ProductID": prod[0]}
#         img_res = rq.get(f"{backend}/ProductImages/where", params=payload)
#         images.append(img_res.json()[0])

#     print(images)

#     data = [{"product": p, "image": i} for p, i in zip(products, images)]
    
#     return render_template('index.html', data=data)



@app.route('/product/<int:id>', methods=["GET"])
def product(id: int):
    # clickin on a product -> /product/<id> = detailed view of product and its properties, with buttons to add to cart

    ### get product and its associated properties
    prod_res = rq.get(f"{backend}/Products/where?ID={id}")
    product = prod_res.json()

    img_res = rq.get(f"{backend}/ProductImages/where?ProductID={id}")
    images = img_res.json()

    prop_res = rq.get(f"{backend}/Properties/where?ProductID={id}")
    properties = prop_res.json()

    return render_template('product.html', product=product, images=images, properties=properties)


@app.route('/cart', methods=["GET"])
def cart():
    # clickin on cart -> /cart = products and their quantities for this customer's order

    return render_template('cart.html')

@app.route('/cart', methods=["POST"])
def cart_purchase():
    # get cart info
    body = request.json

    # create order in backend, get orderID from that
    data = {"CustomerID": str(body.get("CustomerID"))}
    res = rq.post(f"{backend}/Orders", json=data)
    order_id = res.json()

    # create OrderDetails for each product
    for item in body.get("Cart"):
        data = {
            "OrderID": str(order_id),
            "ProductID": str(item.get("ProductID")),
            "Quantity": str(item.get("Quantity"))
        }
        res = rq.post(f"{backend}/OrderDetails", json=data)

    # (should also detract order quantities from stock in Products table but omgfuck that)

    return redirect(url_for('index'))

@app.route('/profile', methods=["GET"])
def profile():
    """page to change between customer profiles"""

    ### get list of customers in db
    cus_res = rq.get(f"{backend}/Customers")
    customers = cus_res.json()

    return render_template('profile.html', customers=customers)



######### from a previous project for reference


# @app.route('/', methods=["GET"])
# def index():
#     # if method was GET with id of product details to b displayed
#     details = None
#     if request.args:
#         id = request.args["id"]
#         res = rq.get(f"{URL_BASE}/api/product/{id}")
#         details = eval(res.content)[0]

#     # if method was post with either delete or update
#     if request.method == "POST":
#         id = request.form['id']
#         if request.form['action'] == "delete":
#             res = rq.delete(f"{URL_BASE}/api/product/{id}")

#     # get all products
#     res = rq.get(f"{URL_BASE}/api/products")
#     data = res.json()

#     return render_template('index.html')
