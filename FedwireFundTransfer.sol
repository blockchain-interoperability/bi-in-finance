// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// [30, "0x2222222222222222222222222222222222222222", "0x8888888888888888888888888888888888888888", "0x4444444444444444444444444444444444444444", "Please process the transaction"]

contract FedwireFundTransferContract {
    address public federalReserveAddress;

    mapping(address => mapping(address => bool)) private hasAccountInBank;
    mapping(address => mapping(address => uint256)) public bankBalances;
    mapping(address => uint256) private reserveBalances;
    mapping(address => bool) private isFedwireParticipant;

    enum TransactionStatus { Pending, Confirmed }
    mapping(address => mapping(address => TransactionStatus)) private transactionStatus;

    
    struct PaymentOrder {
        uint256 amount;
        address senderBank;
        address recipientAccount;
        address recipientBank;
        string instruction;
    }

    struct FedwireMessage {
        uint256 amount;
        address senderAccount;
        address senderBank;
        address recipientAccount;
        address recipientBank;
        string note;
    }

    constructor() {

        federalReserveAddress = msg.sender;

        initializeFRBParticipants();
        initializeBankAccountsAndBalances();
    }

    function initializeBankAccountsAndBalances() private 
    {
        address Alice = 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4;
        address BankA = 0x2222222222222222222222222222222222222222;
        address Bob   = 0x8888888888888888888888888888888888888888;
        address BankB = 0x4444444444444444444444444444444444444444;

        hasAccountInBank[Alice][BankA] = true;
        hasAccountInBank[Bob][BankB] = true;

        bankBalances[Alice][BankA] = 500;
        bankBalances[Bob][BankB] = 500;
    }

    function initializeFRBParticipants() private
    {
        address[] memory participants = new address[](5);
        participants[0] = 0x1111111111111111111111111111111111111111;
        participants[1] = 0x2222222222222222222222222222222222222222;
        participants[2] = 0x3333333333333333333333333333333333333333;
        participants[3] = 0x4444444444444444444444444444444444444444;
        participants[4] = 0x5555555555555555555555555555555555555555;

        uint256 initialReserveBalance = 1000;

        for (uint256 i = 0; i < participants.length; i++) {
            isFedwireParticipant[participants[i]] = true;
            reserveBalances[participants[i]] = initialReserveBalance;
        }
    }

    function initiateTransfer(PaymentOrder memory payOrder) public  {
        
        require(hasAccountInBank[msg.sender][payOrder.senderBank], "Sender is not an account holder of this bank");
        require(bankBalances[msg.sender][payOrder.senderBank] >= payOrder.amount, "Sender doesn't have sufficient balance in this bank account");

        transactionStatus[msg.sender][payOrder.recipientAccount] = TransactionStatus.Pending;

        bankBalances[msg.sender][payOrder.senderBank] -= payOrder.amount;

        FedwireMessage memory fedwireMsg = FedwireMessage(payOrder.amount, msg.sender, payOrder.senderBank, payOrder.recipientAccount, payOrder.recipientBank, "Please process the transaction.");

        federalReserveProcessMessage(fedwireMsg);

        require(transactionStatus[msg.sender][payOrder.recipientAccount] == TransactionStatus.Confirmed, "Transaction Failed 1!");
    }


    function federalReserveProcessMessage(FedwireMessage memory fedwireMsg) internal {
     
        require(isFedwireParticipant[fedwireMsg.senderBank], "Sending Bank is not a fedwire participant");
        require(isFedwireParticipant[fedwireMsg.recipientBank], "Receiving Bank is not a fedwire participant");

        require(reserveBalances[fedwireMsg.senderBank] >= fedwireMsg.amount, "Sending bank does not have sufficient reserve balance");
        require(transactionStatus[fedwireMsg.senderAccount][fedwireMsg.recipientAccount] == TransactionStatus.Pending, "Transaction Failed 2!");

        reserveBalances[fedwireMsg.senderBank] -= fedwireMsg.amount;
        reserveBalances[fedwireMsg.recipientBank] += fedwireMsg.amount;

        FedwireMessage memory confirmationFedwireMsg = FedwireMessage(fedwireMsg.amount, msg.sender, fedwireMsg.senderBank, fedwireMsg.recipientAccount, fedwireMsg.recipientBank, "Transfer successful ! Please credit the amount to receivers bank account.");


        receiverBankProcessMessage(confirmationFedwireMsg);

        require(transactionStatus[fedwireMsg.senderAccount][fedwireMsg.recipientAccount] == TransactionStatus.Confirmed, "Transaction Failed 3!");
    }

    function receiverBankProcessMessage(FedwireMessage memory confirmationFedwireMsg) internal {
        
        require(transactionStatus[confirmationFedwireMsg.senderAccount][confirmationFedwireMsg.recipientAccount] == TransactionStatus.Pending, "Transaction Failed!");
        
        bankBalances[confirmationFedwireMsg.recipientAccount][confirmationFedwireMsg.recipientBank] += confirmationFedwireMsg.amount;
        
        transactionStatus[confirmationFedwireMsg.senderAccount][confirmationFedwireMsg.recipientAccount] = TransactionStatus.Confirmed;
    }
}
