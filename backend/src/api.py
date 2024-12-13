# module exposing endpoints to interact with database, which is done through connectors in backend/database.py

from database import Database, MySQLAdapter

from flask import Flask, json

api = Flask(__name__)

### Routes for operations:
#   GET             /(products? items?) = find_all()
#   GET             /(^)/<id: int>      = find(id)
#   POST            /(^)                = create(**stuff)
#   PUT(PATCH?)     /(^)/<id: int>      = update(id, **stuff)
#   DELETE          /(^)/<id: int>      = delete(id)

@api.route("/", methods=["GET"])
def test():
    # testing whether we can get all rows in products table
    payload = Database(MySQLAdapter).get_table("Products")

    return json_response(payload)

@api.route("/testadd", methods=["GET"])
def test_add():
    # quick and dirty adding a basic product
    payload = Database(MySQLAdapter).test_add()

    return json_response(payload)

# fully copied from https://developer.okta.com/blog/2018/12/20/crud-app-with-python-flask-react
def json_response(payload, status=200):
    """Wraps response from database nicely into json object, with http-like status code and header"""
    return (json.dumps(payload), status, {'content-type': 'application/json'})