# module exposing endpoints to interact with database, which is done through connectors in backend/database.py

from database import Database

from flask import Flask, json, request

api = Flask(__name__)

### Pseudo-code overview of routes:
#   GET       /<table>                        = find_all()
#   GET       /<table>/<id>                   = (shortcut for /where?ID=id)
#   GET       /<table>/where?<query string>   = find_matches(query string)
#   POST      /<table>                        = create(request body)
#   PUT       /<table>/where?<query string>   = update_matches(query string, request body)
#   DELETE    /<table>                        = delete_all_rows()
#   DELETE    /<table>/where?<query string>   = delete_matches(query string)


# C - create
@api.route("/<string:table>", methods=["POST"])
def create_in_table(table: str):
    """
    Adds a new row to table, using body of request.

    Request-body must contain a dict-like JSON object with keys corresponding to the names of the columns in the table's schema
    """
    body = request.json
    payload = Database().create(table, body)
    return json_response(payload)


# R - read
@api.route("/<string:table>", methods=["GET"])
def read_table(table: str):
    """Get all rows in table"""
    payload = Database().get_table(table)
    return json_response(payload)

@api.route("/<string:table>/<int:id>", methods=["GET"])
def read_table_id(table: str, id: int):
    """
    Shortcut for "/(table)/where?ID=(id)"
    """
    args = {"ID": str(id)}
    payload = Database().find_by_params(table, args)
    return json_response(payload)

@api.route("/<string:table>/where", methods=["GET"])
def read_table_where(table: str):
    """Get rows in table that match the query string key=value pairs. e.g. get Products/where?Stock=15&Currency=DKK"""
    args = request.args.to_dict()
    payload = Database().find_by_params(table, args)
    return json_response(payload)


# U - update
@api.route("/<string:table>/where", methods=["PUT"])
def update_in_table(table: str):
    """
    Updates rows in table with that match the query string, using body of request.

    Request-body must contain a dict-like JSON object with keys corresponding to the names of the columns that are to be changed, and the values being the new values to insert
    """
    args = request.args.to_dict()
    body = request.json
    payload = Database().update(table, args, body)
    return json_response(payload)


# D - delete
@api.route("/<string:table>", methods=["DELETE"])
def delete_all_in_table(table: str):
    """Deletes all rows in table"""
    payload = Database().delete(table, None)
    return json_response(payload, status=204)

@api.route("/<string:table>/where", methods=["DELETE"])
def delete_in_table(table: str):
    """Deletes row from table that match the query string"""
    args = request.args.to_dict()
    payload = Database().delete(table, args)
    return json_response(payload, status=204)


### helpers

# fully copied from https://developer.okta.com/blog/2018/12/20/crud-app-with-python-flask-react
def json_response(payload, status=200):
    """Wraps response from database nicely into json object, with http-like status code and header"""
    return (json.dumps(payload), status, {'content-type': 'application/json'})