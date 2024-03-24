import os
import typing_extensions
from flask import Flask, render_template, request, jsonify
from web3 import Web3
import util
import json
import threading


app = Flask(__name__)

web3s = [Web3(Web3.HTTPProvider('http://localhost:8545')),
        Web3(Web3.HTTPProvider('http://localhost:8546')),
        Web3(Web3.HTTPProvider('http://localhost:8547')),
        Web3(Web3.HTTPProvider('http://localhost:8548'))]

# web3_1.eth.defaultAccount = web3_1.eth.accounts[0]
# web3_2.eth.defaultAccount = web3_2.eth.accounts[9]

CHAIN_IDs = [555, 666, 777, 888]

ACCOUNT_TO_SC_ADDRESS = {}

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
CONTRACT_ADDRESSES = []


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

        return jsonify({'full_message': str(content), 'summary': str(dbtr_instruction)}), 200

    else:
        return jsonify({'error': 'File not processed'}), 400



def make_initiate_transfer_transaction(target_contract, chain_idx, anvil_acct_index, dbtr_instruction):
   
    web3 = web3s[chain_idx]

    tx = target_contract.functions.initiate_transfer(dbtr_instruction).build_transaction({
        'chainId': CHAIN_IDs[chain_idx],
        'nonce': web3.eth.get_transaction_count(web3.eth.accounts[anvil_acct_index]),
        'from': web3.eth.accounts[anvil_acct_index]
    })

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEYS[anvil_acct_index])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt


def make_make_transfer_transaction(target_contract, chain_idx, anvil_acct_index, msg_details):
   
    web3 = web3s[chain_idx]

    tx = target_contract.functions.make_transfer(msg_details).build_transaction({
        'chainId': CHAIN_IDs[chain_idx],
        'nonce': web3.eth.get_transaction_count(web3.eth.accounts[anvil_acct_index]),
        'from': web3.eth.accounts[anvil_acct_index]
    })

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEYS[anvil_acct_index])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt


def make_create_account_transaction(target_contract, chain_idx, anvil_acct_index, acct_type, acct):
   
    web3 = web3s[chain_idx]

    tx = target_contract.functions.create_account(acct_type, acct).build_transaction({
        'chainId': CHAIN_IDs[chain_idx],
        'nonce': web3.eth.get_transaction_count(web3.eth.accounts[anvil_acct_index]),
        'from': web3.eth.accounts[anvil_acct_index]
    })

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEYS[anvil_acct_index])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    if tx_receipt.status != 1:
        print("Transaction failed!")


def make_deposit_transaction(target_contract, chain_idx, anvil_acct_index, acct, value):
    
    web3 = web3s[chain_idx]

    tx = target_contract.functions.deposit(acct).build_transaction({
        'chainId': CHAIN_IDs[chain_idx],
        'nonce': web3.eth.get_transaction_count(web3.eth.accounts[anvil_acct_index]),
        'from': web3.eth.accounts[anvil_acct_index],
        'value': value
    })

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEYS[anvil_acct_index])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    if tx_receipt.status != 1:
        print("Transaction failed!")


def execute_smart_contract(agent, iso_message, updated_iso_message):

        tx_receipt = ''
        
        if agent == 'debtor-area':
            dbtr_instruction = util.get_debtor_instructions(iso_message)
            target_contract = web3s[0].eth.contract(address=CONTRACT_ADDRESSES[0], abi=ABI)
            tx_receipt = make_initiate_transfer_transaction(target_contract, 0, 0, dbtr_instruction)

            arrow_to_activate = 'arrow1'
            area_to_populate = 'interm1-area'

        elif agent == 'interm1-area':
            msg_info = util.get_msg_info(iso_message, updated_iso_message)
            target_contract = web3s[1].eth.contract(address=CONTRACT_ADDRESSES[1], abi=ABI)
            tx_receipt = make_make_transfer_transaction(target_contract, 1, 1, msg_info)
            
            arrow_to_activate = 'arrow2'
            area_to_populate = 'interm2-area'

        elif agent == 'interm2-area':
            msg_info = util.get_msg_info(iso_message, updated_iso_message)
            target_contract = web3s[2].eth.contract(address=CONTRACT_ADDRESSES[2], abi=ABI)
            tx_receipt = make_make_transfer_transaction(target_contract, 2, 2, msg_info)
            
            arrow_to_activate = 'arrow3'
            area_to_populate = 'creditor-area'

        elif agent == 'creditor-area':
            msg_info = util.get_msg_info(iso_message, updated_iso_message)
            target_contract = web3s[3].eth.contract(address=CONTRACT_ADDRESSES[3], abi=ABI)
            tx_receipt = make_make_transfer_transaction(target_contract, 3, 3, msg_info)
            
            arrow_to_activate = 'none'
            area_to_populate = 'none'

        if tx_receipt.status == 1:
            event_filter = target_contract.events.PassISOMessageAlong.create_filter(fromBlock='latest')
            new_events = event_filter.get_all_entries()
            
            if new_events:
                last_event = new_events[-1]
                # print(last_event['args']['updatedIsoMsg'])
                # print(last_event['args']['receiver'])
                # print("yay!!!")
            else:
                print("No events found")

            messages = jsonify({'full_message': last_event['args']['updatedIsoMsg'], 
                'summary': util.get_summary(last_event['args']['updatedIsoMsg']),
                'arrow_to_activate': arrow_to_activate, 
                'area_to_populate': area_to_populate
            })

            return messages

        else:
            print("Transaction failed!")
            return "Transaction failed!"



@app.route('/init_contracts', methods=['POST'])
def init_contracts():
    data = request.get_json(force=True)
    init_contracts_info = json.loads(data.get('init_contracts_info'))
    
    if not init_contracts_info:
        return jsonify({'error': 'No init-contract-info'}), 400
    
    DA_contract = web3s[0].eth.contract(address=init_contracts_info['SmartContractAddresses'][0], abi=ABI)
    I1_contract = web3s[1].eth.contract(address=init_contracts_info['SmartContractAddresses'][1], abi=ABI)
    I2_contract = web3s[2].eth.contract(address=init_contracts_info['SmartContractAddresses'][2], abi=ABI)
    CA_contract = web3s[3].eth.contract(address=init_contracts_info['SmartContractAddresses'][3], abi=ABI)

    make_create_account_transaction(DA_contract, 0, 0, "general", init_contracts_info['DbtrAcct'])
    make_deposit_transaction(DA_contract, 0, 0, init_contracts_info['DbtrAcct'], init_contracts_info['D_to_DA_DepositAmt'])

    make_create_account_transaction(I1_contract, 1, 1, "nostro", init_contracts_info['DbtrAgtAcct'])
    make_deposit_transaction(I1_contract, 1, 1, "", init_contracts_info['DA_to_I1_DepositAmt'])

    make_create_account_transaction(I2_contract, 2, 2, "nostro", init_contracts_info['I1Acct'])
    make_deposit_transaction(I2_contract, 2, 2, "", init_contracts_info['I1_to_I2_DepositAmt'])

    make_create_account_transaction(I2_contract, 2, 4, "nostro", init_contracts_info['CdtrAgtAcct'])

    make_create_account_transaction(CA_contract, 3, 5, "general", init_contracts_info['CdtrAcct'])

    return jsonify({'msg': "Initialization successful!"}), 200


@app.route('/get_dc_info', methods=['POST'])
def get_dc_info():

    sc_init_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sc_init.json')
    
    try:
        with open(sc_init_file_path, 'r') as file:
            init_contracts_info = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {sc_init_file_path}")
    except json.JSONDecodeError:
        print("Error decoding JSON")
    except Exception as e:
        print(f"An error occurred: {e}")

    if not init_contracts_info:
        return jsonify({'error': 'No init-contract-info'}), 400
    
    DA_contract = web3s[0].eth.contract(address=init_contracts_info['SmartContractAddresses'][0], abi=ABI)
    I1_contract = web3s[1].eth.contract(address=init_contracts_info['SmartContractAddresses'][1], abi=ABI)
    I2_contract = web3s[2].eth.contract(address=init_contracts_info['SmartContractAddresses'][2], abi=ABI)
    CA_contract = web3s[3].eth.contract(address=init_contracts_info['SmartContractAddresses'][3], abi=ABI)

    DbtrAcct_balance = DA_contract.functions.get_balance(init_contracts_info['DbtrAcct']).call()
    DbtrAgtAcct_balance = I1_contract.functions.get_balance(init_contracts_info['DbtrAgtAcct']).call()
    I1Acct_balance = I2_contract.functions.get_balance(init_contracts_info['I1Acct']).call()
    CdtrAgtAcct_balance = I2_contract.functions.get_balance(init_contracts_info['CdtrAgtAcct']).call()
    CdtrAcct_balance = CA_contract.functions.get_balance(init_contracts_info['CdtrAcct']).call()

    info_string = f"Debtor's Balance in Debtor Agent          : {DbtrAcct_balance} ETH\n"
    info_string += f"Debtor Agent's Balance in Intermediary 1  : {DbtrAgtAcct_balance} ETH\n"
    info_string += f"Intermediary 1's Balance in Intermediary 2: {I1Acct_balance} ETH\n"
    info_string += f"Creditor Agent's Balance in Intermediary 2: {CdtrAgtAcct_balance} ETH\n"
    info_string += f"Creditor's Balance in Creditor Agent      : {CdtrAcct_balance} ETH"

    return jsonify({'msg': info_string}), 200


# def listen_to_events():
   
#     while True:

#         filter = web3.eth.filter({
#             "fromBlock": "latest",
#             "address": ADDRESS,
#         })

#         new_events = filter.get_all_entries()
#         for event in new_events:
#             print("Received event:", event)


@app.route('/make_transaction', methods=['POST'])
def make_transaction():
    data = request.get_json(force=True)
    iso_message = data.get('iso_message')
    updated_iso_message = data.get('updated_iso_message')
    agent = data.get('agent')

    if not iso_message:
        return jsonify({'error': 'No ISO Message'}), 400

    return execute_smart_contract(agent, iso_message, updated_iso_message), 200
    
    


if __name__ == '__main__':
    
    # event_thread = threading.Thread(target=listen_to_events)
    # event_thread.daemon = True
    # event_thread.start()

    sc_init_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sc_init.json')

    try:
        with open(sc_init_file_path, 'r') as file:
            data = json.load(file)
            CONTRACT_ADDRESSES = data.get('SmartContractAddresses', [])  # Safely extract SmartContractAddresses
    except FileNotFoundError:
        print(f"File not found: {sc_init_file_path}")
    except json.JSONDecodeError:
        print("Error decoding JSON")
    except Exception as e:
        print(f"An error occurred: {e}")

    for i in range(0,  4):
        ACCOUNT_TO_SC_ADDRESS[web3s[0].eth.accounts[i+1]] = CONTRACT_ADDRESSES[i]

    app.run(debug=True)
