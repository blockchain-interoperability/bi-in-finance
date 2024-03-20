// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FinancialInstitution{

    address _ownerAddress;
    address _testAddress;

    mapping(address => string) private nostroAccountNo;
    mapping(string => mapping(address => bool)) private generalAccountExists;
    mapping(string => bool) private accountNoExists;
    mapping(string => uint256) public balances;

    struct Amount
    {
        string Ccy;
        uint256 Amt;
    }
    
    struct DbtrIntruction {
        Amount IntrBkSttlmAmt;
        address DbtrAgt;
        string DbtrAcct;
        string DbtrAgtIsoMsg;
        address NxtAgt;
    }

    struct MsgInfo {
        uint256 CtrlSum;
        Amount TtlIntrBkSttlmAmt;
        address InstgAgt;
        address InstdAgt;
        Amount IntrBkSttlmAmt;
        Amount InstdAmt;
        uint256 XchgRate;
        address DbtrAgt;
        string DbtrAcct;
        address CdtrAgt;
        string CdtrAcct;
        string SttlmMtd;
        string SttlmAcct;
        string UpdtdMsg;
        address NxtAgt;
    }

    event MakeTransfer(string isoMsg);
    event PassISOMessageAlong(string updatedIsoMsg, address receiver);

    constructor() payable{
        _ownerAddress = msg.sender;
    }

    function set_sender() public
    {
        _testAddress = msg.sender;
    }
    function get_sender() public view returns (address)
    {
        return _testAddress;
    }

    function initiate_transfer(DbtrIntruction memory dbtrIntruction) public
    {
        // acting as debtor agent

        require(generalAccountExists[dbtrIntruction.DbtrAcct][msg.sender], "Sender (Debtor) is not an account holder of this institution!");
        require(balances[dbtrIntruction.DbtrAcct] >= dbtrIntruction.IntrBkSttlmAmt.Amt, "Sender (Debtor) doesn't have sufficient balance in their account!" );

        balances[dbtrIntruction.DbtrAcct] -= dbtrIntruction.IntrBkSttlmAmt.Amt;

        emit PassISOMessageAlong(dbtrIntruction.DbtrAgtIsoMsg, dbtrIntruction.NxtAgt);
    }

    function process_iso_message(string memory isoMsg) public
    {
        emit MakeTransfer(isoMsg);
    }

    function get_fresh_account_number(string memory wantedAcctNo) private pure returns (string memory)
    {
        if (keccak256(abi.encodePacked(wantedAcctNo)) != keccak256(abi.encodePacked("")))
        {
            return wantedAcctNo; //for testing purposes, allowing users to ask for a specific account number
        }
        return "AX0000"; // dummy value. a ramdom fresh account number will be generated here.
    }

    function create_account(string memory acctType, string memory wantedAcctNo) public
    {
        if (keccak256(abi.encodePacked(acctType)) == keccak256(abi.encodePacked("nostro")))
        {
            nostroAccountNo[msg.sender] = get_fresh_account_number(wantedAcctNo);
        }
        else 
        {
            generalAccountExists[get_fresh_account_number(wantedAcctNo)][msg.sender] = true;
            accountNoExists[get_fresh_account_number(wantedAcctNo)] = true;
        }
    }

    function deposit(string memory acctNo) public payable
    {
        //general account
        if (keccak256(abi.encodePacked(acctNo)) != keccak256(abi.encodePacked("")))
        {
            require(generalAccountExists[acctNo][msg.sender], "Depositor is not an account holder of this institution!");
            
            balances[acctNo] += msg.value;
        }
        //nostro account
        else
        {
            string memory account = nostroAccountNo[msg.sender];
            require(bytes(account).length != 0, "Couldn't verify depositor");
            
            balances[account] += msg.value;
        }
    }

    function get_balance(string memory acctNo) view public returns (uint256)
    {
        return balances[acctNo];
    }

    function make_transfer(MsgInfo memory msgDetails) public 
    {
        require(msg.sender == msgDetails.InstgAgt, "Couldn't verify message sender!");
        require(_ownerAddress == msgDetails.InstdAgt, "Current contract is not supposed to make this transaction!");

        uint256 totalAmount = msgDetails.TtlIntrBkSttlmAmt.Amt+msgDetails.IntrBkSttlmAmt.Amt+msgDetails.InstdAmt.Amt;
        require(msgDetails.CtrlSum == totalAmount, "Transaction couldn't be verified!");

        // acting as creditor agent
        if(_ownerAddress == msgDetails.CdtrAgt)
        {
            require(accountNoExists[msgDetails.CdtrAcct], "Receiver (Creditor) is not an account holder of this institution!");
            
            balances[msgDetails.CdtrAcct] += msgDetails.InstdAmt.Amt;
        }

        // acting as intermediary
        else
        {
            string memory senderAccount = nostroAccountNo[msgDetails.InstgAgt];
            require(bytes(senderAccount).length != 0, "Sender is not a nostro account holder of this institution!");

            require(balances[senderAccount] >= msgDetails.IntrBkSttlmAmt.Amt, "Sender agent doesn't have sufficient amount in it's nostro account!");
            balances[senderAccount] -= msgDetails.IntrBkSttlmAmt.Amt;

            if (keccak256(abi.encodePacked(msgDetails.SttlmAcct)) != keccak256(abi.encodePacked("")))
            {    
                string memory cdtrAgtAccount = nostroAccountNo[msgDetails.CdtrAgt];
                require(bytes(cdtrAgtAccount).length != 0, "Receiver (Creditor Agent) is not a nostro account holder of this institution!");
                
                balances[cdtrAgtAccount] += msgDetails.IntrBkSttlmAmt.Amt;
            }
        }

        emit PassISOMessageAlong(msgDetails.UpdtdMsg, msgDetails.NxtAgt);
    }

}
