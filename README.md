# I Sell Nails

I sell nails is a **Project** web application and API which a user can run a nail selling business.

It uses [FastAPI](https://fastapi.tiangolo.com/) to provide endpoints in which a user can manipulate a database to add, sell and buyback nails.


## Getting started

### Dependencies

* Python3
* FastAPI
* Jinja2
* uvicorn
* numpy

### Installing and running

* Clone this respository
    * HTTPS: `git clone https://github.com/AlexTuTruong/i-sell-nails.git`
    * SSH: `git clone git@github.com:AlexTuTruong/i-sell-nails.git`
    * Github CLI: `gh repo clone AlexTuTruong/i-sell-nails`
* Navigate to the src folder in this repository
    * `cd /path/to/folder/src`
* Install the dependencies
    * `pip install -r requirements.txt`
* Run the application
    * `python3 run.py` within the `src` directory
        * This should run a web server in which you can access from `http://localhost:8000/` or `http://127.0.0.1:8000/`
        * A `nails.db` will generate itself in `src/db` if one doesn't exist already

## This project is a work in progress

Some things I'd like to or will implement:

* ~~A reset button which will bring the database back to an empty state~~
    * Reset ledger button is now implemented
* ~~Dummy data to populate the database when created~~
    * Dummy data is now created on application-run when no data is present
* ~~A ledger which keeps track of transactions~~
    * Ledger is now implemented
* ~~Hover over the total sales for a breakdown of what hammers were sold and how many~~
    * ~~This will require the ledger~~
        * Ledger and Breakdown is now implemented
* ~~Add a stock of nails, so infinite nails cannot be sold, this will probably replace rating as Strength rating is not really neccessary~~
    * Rating is now replaced by stock
* Docker file for easy deployment

## Demo Video

https://github.com/AlexTuTruong/i-sell-nails/assets/53573114/2bee352a-492f-4565-8de9-d451adc804da

## License

This project is licensed under the MIT License - see the LICENSE.md file for details