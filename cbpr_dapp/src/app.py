import os
from flask import Flask, render_template, request, jsonify
from web3 import Web3
import util
import json
import threading


app = Flask(__name__)

web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
web3.eth.defaultAccount = web3.eth.accounts[0]

PRIVATE_KEYS = [0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80, 
                0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d,
                0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a,
                0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6,
                0x47e179ec197488593b187f80a00eb0da91f1b9d0b13f8733639f19c30a34926a,
                0x8b3a350cf5c34c9194ca85829a2df0ec3153be0318b5e2d3348e872092edffba,
                0x92db14e403b83dfe3df233f83dfa3a0d7096f21ca9b0d6d6b8d88b2b4ec1564e,
                0x4bbbf85ce3377467afe5d46f804f221813b2bb87f24d81f60f1fcdbf7cbf4356,
                0xdbda1821b80551c9d65939329250298aa3472ba22feea921c0cf5d620ea67b97,
                0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6]


ABI = util.get_contract_abi(file_name = "FinancialInstitution", contract_name = "FinancialInstitution")
ADDRESS = "0x700b6A60ce7EaaEA56F065753d8dcB9653dbAD35"

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

                # return jsonify({'full_message': last_event['args']['updatedIsoMsg'], 'summary': last_event['args']['receiver']}), 200
                return jsonify({'full_message': str(content), 'summary': str(dbtr_instruction)}), 200
            else:
                print("Transaction failed!")
                return "Transaction failed!"
        else:
            return "Failed to read data from Smart Contract"

    else:
        return jsonify({'error': 'File not processed'}), 400



def make_create_account_transaction(target_contract, anvil_acct_index, acct_type, acct):
   
    tx = target_contract.functions.create_account(acct_type, acct).build_transaction({
        'chainId': 31337,
        'nonce': web3.eth.get_transaction_count(web3.eth.accounts[anvil_acct_index]),
        'from': web3.eth.accounts[anvil_acct_index]
    })

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEYS[anvil_acct_index])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    if tx_receipt.status != 1:
        print("Transaction failed!")


def make_deposit_transaction(target_contract, anvil_acct_index, acct, value):
    tx = target_contract.functions.deposit(acct).build_transaction({
        'chainId': 31337,
        'nonce': web3.eth.get_transaction_count(web3.eth.accounts[anvil_acct_index]),
        'from': web3.eth.accounts[anvil_acct_index],
        'value': web3.to_wei(value, 'ether')
    })

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEYS[anvil_acct_index])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    if tx_receipt.status != 1:
        print("Transaction failed!")



@app.route('/init_contracts', methods=['POST'])
def init_contracts():
    data = request.get_json(force=True)
    print(data)
    init_contracts_info = json.loads(data.get('init_contracts_info'))
    
    if not init_contracts_info:
        return jsonify({'error': 'No init-contract-info'}), 400
    
    DA_contract = web3.eth.contract(address=init_contracts_info['SmartContractAddresses'][0], abi=ABI)
    I1_contract = web3.eth.contract(address=init_contracts_info['SmartContractAddresses'][1], abi=ABI)
    I2_contract = web3.eth.contract(address=init_contracts_info['SmartContractAddresses'][2], abi=ABI)

    make_create_account_transaction(DA_contract, 0, "general", init_contracts_info['DbtrAcct'])
    make_deposit_transaction(DA_contract, 0, init_contracts_info['DbtrAcct'], init_contracts_info['D_to_DA_DepositAmt'])

    make_create_account_transaction(I1_contract, 1, "nostro", init_contracts_info['DbtrAgtAcct'])
    make_deposit_transaction(I1_contract, 1, "", init_contracts_info['DA_to_I1_DepositAmt'])

    make_create_account_transaction(I2_contract, 2, "nostro", init_contracts_info['I1Acct'])
    make_deposit_transaction(I2_contract, 2, "", init_contracts_info['I1_to_I2_DepositAmt'])

    make_create_account_transaction(I2_contract, 5, "general", init_contracts_info['CdtrAcct'])

    print("------------_> Successfull")

    return jsonify({'msg': "Initialization successful!"}), 200



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
