# spac_week10_11

Assignment for week 10 and 11: fullstack project consisting of a frontend application that users can send API-requests to a database through.
 
## installation and usage

Start by installing dependencies: from the top-level of project directory, do `pip install -r requirements.txt`

Ensure you have Docker and docker-compose installed. Docker should be running and ready to start new containers.

### start database

change to backend directory `cd backend`

start docker container `docker-compose up`

### start api

in a new terminal, change to backend directory `cd backend`

start the server with `python src/main.py`, the server should then display the url it is reachable at, such as "http://127.0.0.1:5000"

you can confirm whether you can send HTTP-requests to the server and receive responses by doing `curl "http://127.0.0.1:5000"` in another terminal

### start frontend

(start frontend)