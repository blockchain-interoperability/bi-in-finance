import os
from flask import Flask, render_template, request, jsonify
from web3 import Web3
import util
import json

app = Flask(__name__)

web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
web3.eth.defaultAccount = web3.eth.accounts[0]

ABI = util.get_contract_abi(file_name = "ConnectToWeb3", contract_name = "ConnectToWeb3")
ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

contract = web3.eth.contract(address=ADDRESS, abi=ABI)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_msg_file', methods=['POST'])
def upload_msg_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        content = file.read().decode('utf-8')
        
        summary = util.get_summary(content)
        # summary = "dummy"

        return jsonify({'full_message': content, 'summary': summary}), 200
    else:
        return jsonify({'error': 'File not processed'}), 400



@app.route('/connect_contract')
def connect_contract():
    if web3.is_connected():
        return "Connected to Smart Contract. Address: " + ADDRESS
    else:
        return "Failed to connect to Smart Contract"


@app.route('/read_data')
def read_data():
    if web3.is_connected():
        data = contract.functions.getPerson().call()
        return f"Fetched data: {data}"
    else:
        return "Failed to read data from Smart Contract"


@app.route('/update_data', methods=['POST'])
def update_data():
    if web3.is_connected():
        json_data = request.json
        tx_hash = contract.functions.updatePerson(json_data).transact()
        return f"Transaction Hash: {tx_hash.hex()}"
    else:
        return "Failed to update data on Smart Contract"


if __name__ == '__main__':
    app.run(debug=True)
