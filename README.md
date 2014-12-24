PyEsReduce
==========

Python Map Reduce App for Elastic Search

This is a Simple Map Reduce Engine based on ElasticSearch as the backend storage engine and Redis as the temp storage.

Install Steps:
Install Python 2.7, pip, then install all the python dependency listed in requirements.txt

Install Redis:
And Also start the Redis by using the config inside the running directory.
Make sure it's running, you may change the config file a little bit, eg. The data dir, but one thing to make sure is DO NOT CHANGE the password

run ./server_startup.sh and you are ready to go

Following is Simple Architecture graph to show how it works:
![Simple Architecture](https://github.com/BlueStalker/PyEsReduce/blob/master/PyEsSimpleArch.png)

Better to have a preview in http://54.243.246.138
and use admin/Rene91970Tony6472 to pass the http base auth.
