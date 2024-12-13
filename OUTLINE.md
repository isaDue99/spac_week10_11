outline / specification of this 2-week project

# specification

2 weeks to create a fullstack solution, consisting of a database, api to interact with it, and a frontend

FOCUS: project structure, modularity, maintainability, scaleability, integration between db, api and frontend
AFTER THAT: user authentication (login for customers/admin), unit and integration testing, CI/CD pipeline

run mysql db/flask api in docker, react frontend? or flask frontend if too scary

## database/api

 must support CRUD operations

 3 tables:
 - Products
 - Customers
 - table to store picture-data

 populate with example data

## frontend
 
 a user should be able to:
 - see a list of products with pictures
 - click on product to shower further details
 - add products to and remove products from a cart
 - confirm purchase, where user's info and purchase details are added to database

# timeline

### week 1

**mon:** X get project set up: (db server running, get all (1) items in products table, show in frontend)?

**tues:** db: populate with data, api: CRUD

**wed:** frontend: show prodcts list with pictures, add user ability to add/remove to cart and confirm purchase

**thurs:** api: receive and process user actions

**fri:**

### week 2

**mon:** (figure out later, potentially: security/constraints and maybe auth, testing, CI/CD)

**tues:**

**wed:**

**thurs:** make powerpoint !!

**fri:** presentation of powerpoint showcasing the project


# (notes to self) project structure

backend/main.py starts a server listening on endpoints defined in backend/api.py, which interact with the database thru connectors in backend/database.py

# (notes to self) links
https://www.fullstackpython.com/react.html
https://developer.okta.com/blog/2018/12/20/crud-app-with-python-flask-react
https://flask.palletsprojects.com/en/stable/patterns/javascript/