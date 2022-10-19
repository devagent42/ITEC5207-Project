# Project 4 - Backend

## Minimum Requirements
- Modern computer (4 cores, 8GB of RAM)
- Internet connection
- Latest Docker Engine
- Latest Docker Compose

## Once you have Docker Engine and Docker Compose installed
You need a docker network called `stack` and *MUST* be created externally. To create this network run `docker network create stack`

## Running the Elastic and Kibana stack
In a terminal switch to the `Backend Stack` folder and run `docker-compose up`. This will spin up the Elastic database on port 9200 along with Kibana (the frontend) on 5601. Wait a few minutes and you can run a few sanity checks by opening a browser to `http://localhost:9200` and `http://localhost:5601`, which will open Elastic and Kibana respectively. 

## Stopping the stack
If you want to stop the stack
- `control + c`
- `docker-compose down`

Docker uses persistent volumes for storage, which allows for Elastic and Kibana to store data between restarts of the stack. If it is desired to remove the saved data (for a full reset), you can run the following command `docker-compose down -v` in the same folder where you ran the `docker-compose up` command.


## Data Ingest Container
A data ingest container has been provided to simplify index creation and document ingest. It's a Python script that takes in the CSVs and for each reccord, it generates a JSON document and adds it to the Elastic database. To build the container, in the `Backend Data Ingest` folder, run the following command `docker build -t backend .`

To run the container, run the following command ion the `Backend Data Ingest` folder `docker run --rm --network="stack" -it -v "$(PWD):/opt/" backend /bin/bash`. You will be presented with a Linux terminal prompt, as a sanity check, while in this prompt run the following command `python sanity.py`. If it does not fail, then you are safe to ingest data. Do do this, run `python run.py`.