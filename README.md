WEB CRAWLING PROJECT
--------------------
--------------------

This project can be used to crawl fresh jobs 
from hasjob.co and then extract information like job posting date, 
company_name, website etc from the html and finally put it 
in csv file.

How to run .
-------------
run the following command to get fresh jobs:

``python sc.py -o output_file.csv``

The directory where the script will run should contain 
xpath.json and file_cache.tx files.

PreRequisites
---------------

Python 2
Python libraries :  urllib2 BeautifulSoup json lxml csv
xpath.json file at working directory
file_cache.txt 

TODO: 
-----
Currently we are using file as cache but we can use 
some smart cache like redis in place of file