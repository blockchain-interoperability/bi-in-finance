import json

def get_contract_abi(file_name, contract_name):
    contract_file_path = '../foundry_project/out/'+file_name+'.sol/'+contract_name+'.json'
    try:
        with open(contract_file_path, 'r') as file:
            data = json.load(file)
            abi = data.get('abi')
            if abi:
                return abi
            else:
                raise ValueError("ABI not found in JSON file")
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None
