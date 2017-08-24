from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response

from flask_cors import CORS, cross_origin

import sys
sys.path.append('../')

from learning import eval

def remove_special_characters(string):
    out = ''
    string.encode("utf8").decode("utf8")
    string = string.lower()

    for c in string:
        if c is ' ':
            out += c
        num = ord(c)
        if num >= 97 and num <= 122:
            out += c

    out = ' '.join(out.split())
    return out

app = Flask(__name__)
CORS(app)

services = [
    {
        'id': 1,
        'title': u'List of Services',
        'description': u'Returns a list of all the services provided'
    },
    {
        'id': 2,
        'title': u'Evaluate',
        'description': u'Given a string input, returns which category it fits best in'
    }
]

@app.route('/todo/api/v1/services',methods=['GET'])
def get_all_services():
    return jsonify({'services': services})

@app.route('/todo/api/v1/services/<int:service_id>',methods=['GET'])
def get_service(service_id):
    service = [service for service in services if service['id'] == service_id]
    if len(service) == 0:
        abort(404)
    return jsonify({'service': service[0]})

@app.route('/todo/api/v1/eval/',methods=['GET'])
def request_without_query():
    abort(400)

@app.route('/todo/api/v1/eval/q=<request>',methods=['GET'])
def evaluate(request):
    if len(request) == 0:
        abort(400)
    array = request.split(',')
    for x in range(0,len(array)):
        array[x] = remove_special_characters(array[x])
    if len(array) == 0:
        abort(400)
    j = eval.evaluate(array)
    return jsonify(j)

@app.errorhandler(404)
def not_found_404(error):
    return make_response(jsonify({'Error': 'Not Found'}), 404)

@app.errorhandler(400)
def not_found_400(error):
    return make_response(jsonify({'Error': 'Bad Request'}), 400)

app.run()