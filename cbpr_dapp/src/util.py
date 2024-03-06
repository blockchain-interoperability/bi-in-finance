import json
import xmltodict

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


def replace_keys(data, key_from, key_to):
    if isinstance(data, dict):
        for key in list(data.keys()):
            if key == key_from:
                data[key_to] = data.pop(key)
            else:
                replace_keys(data[key], key_from, key_to)
    elif isinstance(data, list):
        for item in data:
            replace_keys(item, key_from, key_to)


def get_summary(xml_data):

    data = xmltodict.parse(xml_data)

    replace_keys(data, "@Ccy", "Ccy")
    replace_keys(data, "#text", "Amt")

    debtor = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["Dbtr"]["Nm"]
    debtor_account = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["DbtrAcct"]["Id"]["Othr"]["Id"]
    debtor_agent = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["DbtrAgt"]["FinInstnId"]["Nm"]
    creditor = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["Cdtr"]["Nm"]
    creditor_account = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["CdtrAcct"]["Id"]["IBAN"]
    creditor_agent = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["CdtrAgt"]["FinInstnId"]["Nm"]
    intr_bank_sttlm_amount = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["IntrBkSttlmAmt"]
    settlelment_method = data["Document"]["FIToFICstmrCdtTrf"]["GrpHdr"]["SttlmInf"]["SttlmMtd"]
    settlement_account = data.get("Document", {}).get("FIToFICstmrCdtTrf", {}).get("GrpHdr", {}).get("SttlmInf", {}).get("SttlmAcct", {}).get("Id", {}).get("Othr", {}).get("Id", '')
    transfer_amount = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["InstdAmt"]
    xchange_rate = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["XchgRate"]
    current_institution = data["Document"]["FIToFICstmrCdtTrf"]["GrpHdr"]["InstgAgt"]["FinInstnId"]["Nm"]
    next_institution = data["Document"]["FIToFICstmrCdtTrf"]["GrpHdr"]["InstdAgt"]["FinInstnId"]["Nm"]


    info_string = f"Debtor: {debtor}\n"
    info_string += f"Debtor Account: {debtor_account}\n"
    info_string += f"Debtor Agent: {debtor_agent}\n\n"

    info_string += f"Creditor: {creditor}\n"
    info_string += f"Creditor Account: {creditor_account}\n"
    info_string += f"Creditor Agent: {creditor_agent}\n\n"

    info_string += f"Inter Bank Settlement Amount: {intr_bank_sttlm_amount}\n"
    info_string += f"Settlement Method: {settlelment_method}\n"
    info_string += f"Settlement Account: {settlement_account}\n\n"
    
    info_string += f"Transfer Amount: {transfer_amount}\n"
    info_string += f"Exchange Rate: {xchange_rate}\n\n"

    info_string += f"Current Institution: {current_institution}\n"
    info_string += f"Next Institution: {next_institution}"

    return info_string