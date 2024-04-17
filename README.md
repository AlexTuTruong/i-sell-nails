# I Sell Nails

I sell nails is a web application and API which a user can run a nail selling business.

## Description:

I sell nails is a project I started inspired by [I-Sell-Hammers](https://github.com/tarang5757/I-Sell-Hammers).

I wanted to have more experience writing full stack applications so I sell nails

It uses [FastAPI](https://fastapi.tiangolo.com/) to provide endpoints in which a user can manipulate a database to add, sell and buyback nails


## Getting started

### Dependencies

* Python3
* FastAPI
* Jinja2
* uvicorn
* numpy

### Installing and running

* Clone this respository
* Run the command `python3 run.py` within the `app` directory
    * This should run a web server in which you can access from `http://localhost:8000/` or `http://127.0.0.1:8000/`


## This project is a work in progress

Some things I'd like to or will implement:

* A reset button which will bring the database back to an empty state
* Dummy data to populate the database when created
* A ledger which keeps track of transactions
* Hover over the total sales for a breakdown of what hammers were sold and how many
    * This will require the ledger
* Add a stock of nails, so infinite nails cannot be sold, this will probably replace rating as Strength rating is not really neccessary