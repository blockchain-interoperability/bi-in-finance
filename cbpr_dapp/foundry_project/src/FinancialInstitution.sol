// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// [30, "0x2222222222222222222222222222222222222222", "0x8888888888888888888888888888888888888888", "0x4444444444444444444444444444444444444444", "Please process the transaction"]

contract FinancialInstitution{

    address _ownerAddress;
    string _ownerName;

    address public federalReserveAddress;

    mapping(address => string) private nostroAccountNo;
    mapping(address => mapping(string => bool)) private generalAccountExists;
    mapping(string => uint256) public balances;

    enum TransactionStatus { Pending, Confirmed }

    struct Amount
    {
        string Ccy;
        uint256 Amt;
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
        string FullMsgToForward;
    }

    constructor(string memory ownerName) {

        _ownerAddress = msg.sender;
        _ownerName = ownerName;
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
        else generalAccountExists[msg.sender][get_fresh_account_number(wantedAcctNo)] = true;
    }

    function deposit(string memory acctNo) public payable
    {
        //general account
        if (keccak256(abi.encodePacked(acctNo)) != keccak256(abi.encodePacked("")))
        {
            require(generalAccountExists[msg.sender][acctNo], "Depositor is not an account holder of this institution!");
            
            balances[acctNo] += msg.value;
        }
        //nostro account
        else
        {
            string  memory account = nostroAccountNo[msg.sender];
            require(bytes(account).length != 0, "Couldn't verify depositor");
            
            balances[account] += msg.value;
        }
    }

    function makeTransfer(MsgInfo memory msgDetails) public 
    {
        if(_ownerAddress != msgDetails.DbtrAgt)
        {
            require(msg.sender == msgDetails.InstgAgt, "Couldn't verify message sender!");
            require(_ownerAddress == msgDetails.InstdAgt, "Current contract is not supposed to make this transaction!");
        }

        uint256 totalAmount = msgDetails.TtlIntrBkSttlmAmt.Amt+msgDetails.IntrBkSttlmAmt.Amt+msgDetails.InstdAmt.Amt;
        require(msgDetails.CtrlSum == totalAmount, "Transaction couldn't be verified!");


        // acting as debtor agent
        if(_ownerAddress == msgDetails.DbtrAgt)
        {
            require(generalAccountExists[msgDetails.DbtrAgt][msgDetails.DbtrAcct], "Sender (Debtor) is not an account holder of this institution!");
            require(balances[msgDetails.DbtrAcct] >= msgDetails.IntrBkSttlmAmt.Amt, "Sender (Debtor) doesn't have sufficient balance in their account!" );

            balances[msgDetails.DbtrAcct] -= msgDetails.IntrBkSttlmAmt.Amt;

            //TO_DO: send msg to next entity
        }

        // acting as creditor agent
        else if(_ownerAddress == msgDetails.CdtrAgt)
        {
            require(generalAccountExists[msgDetails.CdtrAgt][msgDetails.CdtrAcct], "Receiver (Creditor) is not an account holder of this institution!");
            
            balances[msgDetails.CdtrAcct] += msgDetails.InstdAmt.Amt;

            //TO_DO: send confirmation to previous entity
        }

        // acting as intermediary
        else
        {
            string memory sender_account = nostroAccountNo[msg.sender];
            require(bytes(sender_account).length != 0, "Sender is not a nostro account holder of this institution!");

            require(balances[sender_account] >= msgDetails.IntrBkSttlmAmt.Amt, "Sender agent doesn't have sufficient amount in it's nostro account!");
            balances[sender_account] -= msgDetails.IntrBkSttlmAmt.Amt;

            if (keccak256(abi.encodePacked(msgDetails.SttlmAcct)) != keccak256(abi.encodePacked("")))
            {    
                string memory cdtr_agt_account = nostroAccountNo[msgDetails.CdtrAgt];
                require(bytes(cdtr_agt_account).length != 0, "Receiver (Creditor Agent) is not a nostro account holder of this institution!");
                
                balances[cdtr_agt_account] += msgDetails.IntrBkSttlmAmt.Amt;
            }

            //TO_DO: send confirmation to previous entity
            //TO_DO: modify msg and send it to next entity
        }
    }

}
