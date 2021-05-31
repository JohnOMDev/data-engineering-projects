#	Introduction          
Bayer wants to increase the market share in Germany for its most important anti-allergy product, Snaffleflax®. A critical step in achieving this goal is understanding, measuring and predicting this market share against the three primary competitor products in the market which are Globberin, Beeblizox and Vorbulon.
### Data description
Eighteen months historical data was provided between 2019-01 and 2020-06. The data consists of historical market share and historical sales and marketing activity, i.e. receiving email newsletters or face-to-face visits with sales reps. The historical sales and marketing activity is stored in a Customer Relationship Management (CRM) database.
The historical market share are made up of the customer account UUID (acct_id), the product name as recorded by the distributor (product_name), the date of the sale (rounded to the month), the units sold for that account in the month and the creation timestamp of the record in the database.     
The CRM data has the following schema: the customer account UUID (acct_id), the event type (f2f, workplace event, or group call), and the date of the event. 

## Set up Environment
*   Install or Update your python - pip install postgres.
*   Install postgres python driver on your computer - Ubuntu user can follow the follwing link for quick setup - https://tecadmin.net/install-postgresql-server-on-ubuntu/.
*   Install ipython SQL simulator - pip install ipython-sql.

##  Functionality
### 1   Create Database
### 2   Drop table if exits
### 3   Create table if not exists
### 4   Insert into table
### 5   Build ETL Processes
### 6   Perform Analytic Query to clean the data and answer the business questions


### What is the use of each file
*   `create_tables.py`: The python script contain functions to automate the process of creating and dropping the database and table.
*   `sql_queries.py`: The file contains sql query that perform dropping, creation, and insertion of data into the table. 
*   `etl.py`: The python script contain the process of extracting the data, process and insert it into the tables.
*   `Analytic.ipynb`: Interractive environment for answering the business questions.
*   `test.ipynb`: Interractive environment for testing the create table process.
*   `data`:  The data folder.

### The data set structure.
The data folder contain json file for sales data and csv for crm data in the following structure.
*   `crm.csv`
*   `sales-2019-02-01.json`

### How to run the scripts
*   Set up the evenvironment.
*   Run `create_tables.py` in the console using `python create_tables.py`.
*   Run `etl.py` using `python etl.py`.
*	Open the `test.ipynb` for testing the table creation and insertion.
*   Finally, open `Analytics.ipynb` jupyter notebook using anaconda to check solution for the business questions.

![alt text](https://github.com/JohnOMDev/data-engineering-projects/blob/main/creating_timeseries_etl/images/bayer.jpg?raw=true)