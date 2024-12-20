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
 - click on product to show further details
 - add products to and remove products from a cart
 - confirm purchase, where user's info and purchase details are added to database

# todos on timeline

**mon:** X api: crud, X db: populate Products and Properties with dataset, images in ProductImages

**tues:** X smiles

**wed:** X frontend: quick prototype that can interact with api. then make pretty

**thurs:** X frontend: user selection and add to cart, backend: make search/finding better with logic operators and stuff?, X db: vary input data a bit in currencies and stock amounts etc, make powerpoint !!

**fri:** presentation of powerpoint showcasing the project


# (notes to self) project structure

backend/main.py starts a server listening on endpoints defined in backend/api.py, which interact with the database thru connectors in backend/database.py

# (notes to self) links
https://www.fullstackpython.com/react.html
https://developer.okta.com/blog/2018/12/20/crud-app-with-python-flask-react
https://flask.palletsprojects.com/en/stable/patterns/javascript/

# (notes to self) example requests to backend
POST: `invoke-webrequest -Method "POST" -Uri "http://127.0.0.1:5000/Orders" -Body '{"CustomerID": "1"}' -ContentType "application/json"`

GET: `invoke-webrequest "http://127.0.0.1:5000/Orders"`