# module exposing endpoints to interact with database, which is done through connectors in backend/database.py

from database import Database

from flask import Flask, json, request

api = Flask(__name__)

##### Routes for operations:
### Product-associated:
#   GET             /products                       = find_all()
#   GET             /products/<id: int>             = find(id)
#   GET             /products/<search term: str>    = find_all(ids that have term as a value in Products or Properties)
#   POST            /products                       = create(**stuff)
#   PUT(PATCH?)     /products/<id: int>             = update(id, **stuff)
#   DELETE          /products/<id: int>             = delete(id)

### Customer-associated: analogous to products, but with base url as /customers/... instead
### same for orders at /orders/...

@api.route("/<string:table>", methods=["GET"])
def get_table(table: str):
    payload = Database().get_table(table)
    return json_response(payload)

@api.route("/<string:table>/id=<int:id>", methods=["GET"])
def find_id(table: str, id: int):
    payload = Database().find_id(table, id)
    return json_response(payload)

@api.route("/<string:table>/where", methods=["GET"])
def find_params(table: str):
    args = request.args.to_dict()
    print(args)
    payload = Database().find_params(table, args)
    return json_response(payload)

@api.route("/testadd", methods=["GET"])
def test_add():
    # quick and dirty adding a basic product
    payload = Database().test_add()

    return json_response(payload)

# fully copied from https://developer.okta.com/blog/2018/12/20/crud-app-with-python-flask-react
def json_response(payload, status=200):
    """Wraps response from database nicely into json object, with http-like status code and header"""
    return (json.dumps(payload), status, {'content-type': 'application/json'})