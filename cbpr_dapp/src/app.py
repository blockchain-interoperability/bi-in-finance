import os
from flask import Flask, render_template, request, jsonify
from web3 import Web3
import util
import json
import threading


app = Flask(__name__)

web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
web3.eth.defaultAccount = web3.eth.accounts[0]

ABI = util.get_contract_abi(file_name = "FinancialInstitution", contract_name = "FinancialInstitution")
ADDRESS = "0x322813Fd9A801c5507c9de605d63CEA4f2CE6c44"

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
        dbtr_instruction = util.get_debtor_instructions(content)

        if web3.is_connected():
         
            tx_hash = contract.functions.initiate_transfer(dbtr_instruction).transact()
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            
            if tx_receipt.status == 1:
                event_filter = contract.events.PassISOMessageAlong.create_filter(fromBlock='latest')
                new_events = event_filter.get_all_entries()
              
                if new_events:
                    last_event = new_events[-1]
                    # print(last_event['args']['updatedIsoMsg'])
                    # print(last_event['args']['receiver'])
                else:
                    print("No events found")

                return jsonify({'full_message': last_event['args']['updatedIsoMsg'], 'summary': last_event['args']['receiver']}), 200
            else:
                print("Transaction failed!")
                return "Transaction failed!"
        else:
            return "Failed to read data from Smart Contract"

    else:
        return jsonify({'error': 'File not processed'}), 400




def listen_to_events():
    # event_filter = contract.events.PassISOMessageAlong.create_filter(fromBlock='latest')
    # print("=============> ", event_filter)
    
    while True:

        filter = web3.eth.filter({
            "fromBlock": "latest",
            "address": ADDRESS,
        })

        new_events = filter.get_all_entries()
        for event in new_events:
            print("Received event:", event)




@app.route('/make_transaction', methods=['POST'])
def make_transaction():
    data = request.get_json(force=True)
    iso_message = data.get('iso_message')
    
    if not iso_message:
        return jsonify({'error': 'No ISO Message'}), 400
    
    iso_message_interm1 = iso_message
    iso_message_interm2 = iso_message
    iso_message_creditor = iso_message

    messages = jsonify({'interm1_full_message': iso_message_interm1, 
        'interm1_summary': util.get_summary(iso_message_interm1),
        'interm2_full_message': iso_message_interm2, 
        'interm2_summary': util.get_summary(iso_message_interm2),
        'creditor_full_message': iso_message_creditor, 
        'creditor_summary': util.get_summary(iso_message_creditor)
    })

    return messages, 200




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
    
    # event_thread = threading.Thread(target=listen_to_events)
    # event_thread.daemon = True
    # event_thread.start()

    app.run(debug=True)
