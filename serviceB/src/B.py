import logging
import requests
import os
from flask import Flask, Response

app = Flask(__name__)
logging.basicConfig(format='%(name)s - %(message)s')

getrequest = os.environ.get("GET_REQUEST")

@app.route('/api/serviceB')
def getServiceA():
    res = requests.get(getrequest)
    if str(res.status_code) == '500':
       logging.warning(str(res.content))
    return(str(res))


@app.route('/health')
def hello_world():
    return "I am healthy"


#if __name__ == '__main__':
#    app.run('0.0.0.0', 8080)
