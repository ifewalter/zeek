import logging
import os
import logger
import atexit
from pymongo import MongoClient
dataFd = None
errorFd = None


import uuid

def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.



def writeToFile(session, container):
    global dataFd, errorFd
    # try:
    if (not session.failed):
        if dataFd is None:
            filename = container.domain+'/output'+my_random_string(6)+'.txt'
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            dataFd = open(filename, 'w')
        dataFd.write(container.content.replace(",","").encode('utf-8') + "\n")

         #connect to database and fetch root urls
        client = MongoClient(host="192.168.207.47", port=27100)
        #client = MongoClient(host="127.0.0.1", port=27017)
        db = client["summer_db"]
        table = db["news_articles"]

        results = table.insert({"domain":container.domain,"news_content":container.content.replace(",","").encode('utf-8'),"news_title": container.title})
        client.close()



    elif session.failed:
        if errorFd is None:
            errorFd = open('error.txt', 'w')
        errorFd.write(str(session.returnCode).replace(",","") + "," + str(session.errorMsg).replace(",","") + "." + session.url.replace(",","") + "\n")
        #else:
        #    raise Exception("..")
    # except:
    #     logger.log(logging.ERROR, "Unhandled exception in storage.py")

def writeToDb(session, container):
    a = "Will come soon - Happy Halloween"

def atexitfct():
    """Cleanly closes file objects"""
    if dataFd is not None:
        dataFd.close()
    if errorFd is not None:
        errorFd.close()

atexit.register(atexitfct)