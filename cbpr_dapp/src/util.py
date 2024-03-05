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


def get_summary(xml_data):
    data = xmltodict.parse(xml_data)

    debtor = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["Dbtr"]["Nm"]
    debtor_account = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["DbtrAcct"]["Id"]["Othr"]["Id"]
    debtor_agent = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["DbtrAgt"]["FinInstnId"]["Nm"]
    creditor = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["Cdtr"]["Nm"]
    creditor_account = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["CdtrAcct"]["Id"]["IBAN"]
    creditor_agent = data["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["CdtrAgt"]["FinInstnId"]["Nm"]
    control_sum = data["Document"]["FIToFICstmrCdtTrf"]["GrpHdr"]["CtrlSum"]
    settlelment_method = data["Document"]["FIToFICstmrCdtTrf"]["GrpHdr"]["SttlmInf"]["SttlmMtd"]
    current_institution = data["Document"]["FIToFICstmrCdtTrf"]["GrpHdr"]["InstgAgt"]["FinInstnId"]["Nm"]
    next_institution = data["Document"]["FIToFICstmrCdtTrf"]["GrpHdr"]["InstdAgt"]["FinInstnId"]["Nm"]

    info_string = f"Debtor: {debtor}\n"
    info_string += f"Debtor Account: {debtor_account}\n"
    info_string += f"Debtor Agent: {debtor_agent}\n\n"
    info_string += f"Creditor: {creditor}\n"
    info_string += f"Creditor Account: {creditor_account}\n"
    info_string += f"Creditor Agent: {creditor_agent}\n\n"
    info_string += f"Control Sum: {control_sum}\n"
    info_string += f"Settlement Method: {settlelment_method}\n\n"
    info_string += f"Current Institution: {current_institution}\n"
    info_string += f"Next Institution: {next_institution}"

    

    return info_string