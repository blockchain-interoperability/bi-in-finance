from flask import Flask, render_template, request
from web3 import Web3

app = Flask(__name__)

# Define the ABI (Application Binary Interface) of the smart contract
ABI = [
    { "type": "constructor", "inputs": [], "stateMutability": "nonpayable" },
    {
      "type": "function",
      "name": "getPerson",
      "inputs": [],
      "outputs": [{ "name": "", "type": "string", "internalType": "string" }],
      "stateMutability": "view"
    },
    {
      "type": "function",
      "name": "updatePerson",
      "inputs": [
        {
          "name": "_data",
          "type": "tuple",
          "internalType": "struct ConnectToWeb3.Person",
          "components": [
            { "name": "name", "type": "string", "internalType": "string" },
            { "name": "age", "type": "uint256", "internalType": "uint256" },
            { "name": "country", "type": "string", "internalType": "string" }
          ]
        }
      ],
      "outputs": [],
      "stateMutability": "nonpayable"
    }
  ]

# Define the address of the smart contract
ADDRESS = "0x663F3ad617193148711d28f5334eE4Ed07016602"

# Connect to an Ethereum node
web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Change the URL to your Ethereum node

# Set the default account
web3.eth.defaultAccount = web3.eth.accounts[2]  # Change the index to the account you want to use

# Instantiate the contract
contract = web3.eth.contract(address=ADDRESS, abi=ABI)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/connect_metamask')
def connect_metamask():
    if web3.is_connected():
        return f"Connected to Metamask. Account is: {web3.eth.defaultAccount}"
    else:
        return "Failed to connect to Metamask"


@app.route('/connect_contract')
def connect_contract():
    if web3.is_connected():
        return "Connected to Smart Contract. Address: " + ADDRESS
    else:
        return "Failed to connect to Smart Contract"


@app.route('/read_word')
def read_word():
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
