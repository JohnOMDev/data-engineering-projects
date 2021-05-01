#	PROJECT DESCRIPTION
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

The goal of the current project is to build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

In this project, we will create an ETL pipeline to build a data warehouses hosted on Redshift.


#	Data Description
*	Song Data Path --> s3://udacity-dend/song_data 
*	Log Data Path --> s3://udacity-dend/log_data Log Data JSON Path --> s3://udacity-dend/log_json_path.json

##	Song Dataset
The first dataset is a subset of real data from the Million Song Dataset(https://labrosa.ee.columbia.edu/millionsong/). Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example:

`song_data/A/B/C/TRABCEI128F424C983.json song_data/A/A/B/TRAABJL12903CDCF1A.json`

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

`{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}`
##	Event Dataset
The second dataset consists of log files in JSON format. The log files in the dataset with are partitioned by year and month. For example:

`log_data/2018/11/2018-11-12-events.json log_data/2018/11/2018-11-13-events.json`

And below is an example of what a single log file, 2018-11-13-events.json, looks like.

`{"artist":"Pavement", "auth":"Logged In", "firstName":"Sylvie", "gender", "F", "itemInSession":0, "lastName":"Cruz", "length":99.16036, "level":"free", "location":"Klamath Falls, OR", "method":"PUT", "page":"NextSong", "registration":"1.541078e+12", "sessionId":345, "song":"Mercy:The Laundromat", "status":200, "ts":1541990258796, "userAgent":"Mozilla/5.0(Macintosh; Intel Mac OS X 10_9_4...)", "userId":10}`


#	Project Data Modelling
* users - users in the app
				`user_id, first_name, last_name, gender, level`
* songs - songs in music database
				`song_id, title, artist_id, year, duration`
* artists - artists in music database 
				`artist_id, name, location, lattitude, longitude`
* time - timestamps of records in songplays broken down into specific units 
				`start_time, hour, day, week, month, year, isweekends`

songplays (fact table) - records in event data associated with song plays i.e. records with page NextSong
				`songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent`







#	HOW TO RUN

*	Import all the necessary libraries
*	Write the configuration of AWS Cluster, store the important parameter in the config file `dwh.cfg` 
*	Configuration of boto3 which is an AWS SDK for Python
*	Run `create_AWS_resources_iaac.py` to create an IAM User Role, Assign appropriate permissions and create the Redshift Cluster
*	This will also save the Value of Endpoint and Role for put into main configuration file automatically and uuthorize Security Access Group to Default TCP/IP Address
*	Launch database connectivity configuration
*	Go to Terminal write the command `python create_tables.py` and then `etl.py`
*	Should take around 10 minutes in total
*	You can checxk it in jupyter noteboook `test.ipynb` everything is working fine
*	Now can delete the cluster, roles and assigned permission by running `delete_AWS_resources_iaac.py`