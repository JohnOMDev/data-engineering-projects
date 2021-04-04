# ETL on music streaming dataset with postgreSQL
The project involves analyses of data collected on songs and user activity on their new music streaming app. 
The aim is to understand what songs users are listening to. 
The dataset used in the project is a subset of real data from the Million Song  https://labrosa.ee.columbia.edu/millionsong/. 
Each file is in JSON format and contains metadata about a song and the artist of that song. 
The files are partitioned by the first three letters of each song's track ID. 
For example, here are filepaths to two files in this dataset.
## Set up Environment
*   Install or Update your python - pip install postgres
*   Install postgres python driver on your computer - Ubuntu user can follow the follwing link for quick setup - https://tecadmin.net/install-postgresql-server-on-ubuntu/
*   Install ipython SQL simulator - pip install ipython-sql

##  Functionality
### 1   Create Database
### 2   Drop table if exits
### 3   Create table if not exists
### 4   Insert into table
### 5   Build ETL Processes
### 6   Query and test

![alt text](https://github.com/JohnOMDev/data-engineering-projects/etl-project-with-postgres/blob/main/song_table.png?raw=true)



![alt text](https://github.com/JohnOMDev/data-engineering-projects/etl-project-with-postgres/blob/main/fact_table.png?raw=true)
