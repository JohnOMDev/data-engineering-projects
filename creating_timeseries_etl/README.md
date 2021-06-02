#	Introduction          
Marketing team needs to know the current total available volume in the platform by project and recent development over the recent period for Exporo Financing (https://exporo.de/finanzierung/).
### Data description
In order to get the information, our product team has provided us with the following endpoint: https://read.financing.exporo.io/v1/projects/meta/active

This endpoint shows the current/active projects (also called financing entities) in the financing section as of now. 

###	Assumptions:
You can assume that DWH contains already the below tables
*	Funding Target
*	Intermediated Capital

### Business Requirements:
The idea is to have 2 basic reports that should provide:
*	Current available projects and volume in the platform
*	Development of each project over time: total volume available in the last 90 days

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