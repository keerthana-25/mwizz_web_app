from flask import Flask, request, jsonify
from db_connector import DBConnector

app = Flask(__name__)

db_obj = DBConnector()


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/processLog', methods=['POST', 'PUT'])
def process_log():
    data = request.args.to_dict()
    data['status'] = 'init'
    id = db_obj.db_insert('bug_info', data)
    response = jsonify({'status': 'Submitted log data for processing!', 'request id': id})
    return response


@app.route('/processLog/status',  methods=['GET'])
def get_status():
    request_id = request.args.get('requestId')
    status = db_obj.db_fetch_status_for_id('bug_info', request_id)
    response = jsonify({'requestId': request_id, 'stauts': status})
    return response


@app.route('/allRequestDetails', methods=['GET'])
def get_all_request_details():
    product_name = request.args.get('productName')
    result = db_obj.db_fetch_all_request_details('bug_info', product_name)
    response = jsonify({'data': result})
    return response