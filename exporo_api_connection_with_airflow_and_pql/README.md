#	Introduction          
Marketing team needs to know the current total available volume in the platform by project and recent development over the recent period for Exporo Financing `https://exporo.de/finanzierung`.
## Data description
In order to get the information, our product team has provided us with the following endpoint: `https://read.financing.exporo.io/v1/projects/meta/active`

This endpoint shows the current/active projects (also called financing entities) in the financing section as of now. 

##	Assumptions:
You can assume that DWH contains already the below tables
*	Funding Target
*	Intermediated Capital

### Business Requirements:
The idea is to have 2 basic reports that should provide:
*	Current available projects and volume in the platform
*	Development of each project over time: total volume available in the last 90 days

## Set up Environment
*   Install or Update your python
*   Install postgres python driver on your computer - Ubuntu user can follow the follwing link for quick setup - `https://tecadmin.net/install-postgresql-server-on-ubuntu/.`
*   Install ipython SQL simulator - pip install ipython-sql.
* 	Install airflow - `https://airflow.apache.org`
*	Install Virtualenv

##  Functionality
### 1   Drop table if exits
### 2   Create table if not exists
###	3	Establish conncetion to the API
### 4   Insert into table
### 5   Build ETL Processes

### Environment Start-up
*	Place your dags directory into your `airflow.cfg`
*	Open two terminals and `cd` into the dag directory
* 	A virtual environment with all the library and packages used is provided, therefore actiavte the virtual environment by typing `source exporo-venv/bin/activate` in the two terminals.
*	In the first terminal, type `airflow webserver -p 8080`
*	In the second terminal, type `airflow scheduler`
*	Finally, you can visit `localhost:8080` or just `localhost` on your browser

### What is the use of each file
*   `create_tables.py`: The python script contain functions to automate the process of creating and dropping the database and table.
*   `sql_queries.py`: The file contains sql query that perform dropping, creation, and insertion of data into the table. 
*   `etl.py`: The python script contain the process of extracting data from extracting and inserting data into the available volume table.
*   `api_connection.py`: Class client that interract with the `exporo_api.py` and the dag.
*   `exporo_api.py`: Custom class handler for making connecting to the api.
*   `exporo-dag.py`:  The airflow file for the pipeline management.


![alt text](https://github.com/JohnOMDev/data-engineering-projects/blob/main/creating_timeseries_etl/images/exporo_dag.png?raw=true)