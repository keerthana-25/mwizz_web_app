from flask import Flask, request, jsonify
from flask_cors import CORS
from db_connector import DBConnector
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

db_obj = DBConnector()


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/processLog', methods=['POST'])
def process_log():
    productName = request.form['productName']
    logFileName = request.form['logFileName']
    error_file = request.files['stacktraceFile']
    data = {'productName':productName, 'logFileName':logFileName, 'state':'init'}
    id = db_obj.db_insert('bug_info', data)
    filename = id + '.' + '.'.join(error_file.filename.split('.')[1:])
    error_file.save(os.path.join('/logs_to_be_processed', filename))
    response = jsonify({'status': 'Submitted log data for processing!', 'requestId': id})
    return response


@app.route('/processLog/status',  methods=['GET'])
def get_status():
    request_id = request.args.get('requestId')
    print("get status info for request - ", request_id)
    state = db_obj.db_fetch_state_for_id('bug_info', request_id)
    response = jsonify({'requestId': request_id, 'state': state})
    return response


@app.route('/allRequestDetails', methods=['GET'])
def get_all_request_details():
    product_name = request.args.get('productName')
    result = db_obj.db_fetch_all_request_details('bug_info', product_name)
    response = jsonify({'data': result})
    return response