import logging
import logger
import atexit

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
            dataFd = open(container.domain+'/output'+my_random_string(6)+'.txt', 'w')
        dataFd.write(container.content.replace(",","").encode('utf-8') + "\n")
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