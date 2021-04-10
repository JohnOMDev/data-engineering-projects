# ETL on music streaming dataset with MySQL
The project involves analyses of data collected on songs and user activity on their new music streaming app. 
The aim is to understand what songs users are listening to. 
The dataset used in the project is a subset of real data from the Million Song  https://labrosa.ee.columbia.edu/millionsong/. 
Each file is in JSON format and contains metadata about a song and the artist of that song. 
The files are partitioned by the first three letters of each song's track ID. 
For example, here are filepaths to two files in this dataset.
## Set up Environment
*   Install or Update your python - `pip install python -m pip install mysql-connector-python`
*   Install ipython SQL simulator - pip install ipython-sql

##  Functionality
### 1   Create Database: 
### 2   Drop table if exits
### 3   Create table if not exists
### 4   Insert into table
### 5   Build ETL Processes
### 6   Query and test


### What is the use of each file in your submission
*   `create_tables.py`: The python script contain functions to automate the process of creating and dropping the database and table.
*   `sql_queries.py`: The file contains sql query that perform dropping, creation, and insertion of data into the table. 
*   `etl.py`: The python script contain the process of extracting the data, process and insert it into the tables.
*   `etl.ipynb`: Interractive environment for testing the etl process.
*   `test.ipynb`: Interractive environment for testing the create table process.
*   `data`:  The data folder.

### The data set structure.
The data folder contain json file for log data and song data in the following structure
*   `log_data/2018/11/2018-11-12-events.json`
*   `song_data/A/A/A/TRAAAAW128F429D538.json`
### How to run the scripts
*   Set up the evenvironment
*   Run `create_tables.py` in the console using `python create_tables.py`
*   Finally, run `etl.py` using `python etl.py`.
*   For more user interraction, you can also run the `test.ipynb` and `etl.ipynb` jupyter notebook using anaconda


![alt text](https://github.com/JohnOMDev/data-engineering-projects/blob/main/etl-project-with-postgres/images/song_table.png?raw=true)


![alt text](https://github.com/JohnOMDev/data-engineering-projects/blob/main/etl-project-with-postgres/images/fact_table.png?raw=true)
