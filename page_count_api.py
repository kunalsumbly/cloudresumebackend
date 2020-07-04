#
# please configure aws cli before using this program
#
import os, traceback, sys
from bottle import Bottle, request, post, response, static_file, run
from os import path
import json
import boto3
import datetime
import dynamodb_client
listeningPort = "9098"
app = Bottle()


@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

# this method is called when any request is posted to /visitcount URL
@app.route('/visitcount', method=['GET'])
def increment_visit_count():
    printRequestHeaders(request)
    try:
        return dynamodb_client.increment_page_visit_count()
    except:
        return "NOK"
    
# this method prints all the headers in the request
def printRequestHeaders(request):
    print(dict(request.headers))    


if __name__ == '__main__':
    port = int(os.environ.get('PORT', listeningPort))
    run(app,host="0.0.0.0", port=port, debug=True)
    



