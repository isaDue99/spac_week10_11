# spac_week10_11

Assignment for week 10 and 11: fullstack project consisting of a frontend application that users can send API-requests to a database through.
 
 
## first-time installation and usage

Start by installing dependencies: from the top-level of project directory, do `pip install -r requirements.txt`

Ensure you have Docker and docker-compose installed. Docker should be running and ready to start new containers.

### start database

change to backend directory `cd backend`

start docker container `docker-compose up`

### start api

in a new terminal, change to backend's source directory `cd backend/src`

populate the database with some data by running the script `python populate_database.py`

start the server with `python main.py`, the server should then display the url it is reachable at, such as "http://127.0.0.1:5000"
(or start the server in debug mode with `flask --app main run --debug`)

you can confirm whether you can send HTTP-requests to the server and receive responses by using `curl` or `Invoke-WebRequest` in another terminal

### start frontend

in a new terminal, change to frontend directory `cd frontend`

since port 5000 is already in use by the backend, start the frontend with `flask --app main run -p 3000` (or another port number, if 3000 is already in use) (and optionally include `--debug` to run it in debug mode)
the server should now display the url it is reachable at, such as "http://127.0.0.1:3000", open this link in your browser

## subsequent usage

start the database container using either `docker-compose up` or the Docker Desktop GUI

start the backend API-server, and start the frontend GUI-server