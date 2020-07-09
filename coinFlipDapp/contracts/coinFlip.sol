pragma solidity 0.5.12;

contract Flip {

    address public owner;
    uint public contractBalance;

    constructor() public{
        owner = msg.sender;
        contractBalance = address(this).balance;
    }

    event coinFlipped(address user, uint bet, bool);
    event funded(address owner, uint funding);
    event lowBalance(address owner, uint contractBalance);

    modifier nonZero(){
        require(msg.value > 0, "Amount must be greater than zero!");
        _;
    }

    modifier onlyOwner(){
        require(msg.sender ==  owner, "You do not have access rights");
        _;
    }

    // Coin flip function
    function coinFlip(uint betAmt) public payable nonZero returns (bool, bool) {
        require(address(this).balance >= msg.value, "The contract does not have enough funds");

        bool betResult;
        bool reqFund;

        if(now % 2 == 0){
            // Bet is won, send amount equal to bet to user
            contractBalance -= msg.value;
            msg.sender.transfer(betAmt * 2);
            betResult = true;
        }
        else{
            // Bet is lost, take bet amount away from user
            contractBalance += msg.value;
            betResult = false;
        }
        emit coinFlipped(msg.sender, msg.value, betResult);

        if(contractBalance < 1 ether){
            reqFund = true;
            emit lowBalance(msg.sender, contractBalance);
        }
        else{
            reqFund = false;
        }
        return (betResult, reqFund);
    }

    // Function to fund the contract
    function fundContract() public payable onlyOwner nonZero returns(uint){
        require(msg.value != 0);
        contractBalance += msg.value;
        emit funded(msg.sender, msg.value);
        //assert(contractBalance == address(this).balance);
        return contractBalance;
    }

    // Function to show current balance
    function getBalance() public view onlyOwner returns(uint, uint){
        return (address(this).balance, contractBalance);
    }

    // Function to withdraw funds from contract
    function withdraw(uint amt) public onlyOwner returns(uint, bool) {
        require(amt > 0, "Withdrawal amount must be greater than zero");

        uint toTransfer = amt;
        contractBalance -= amt;
        msg.sender.transfer(toTransfer);

        bool reqFund;

        if(contractBalance < 1 ether){
           reqFund = true;
           emit lowBalance(msg.sender, contractBalance);
        }
        else{
           reqFund = false;
        }

        return (contractBalance, reqFund);
   }

   // Function to withdraw all funds from contracts
   function withdrawAll() public onlyOwner returns(uint, bool) {

       uint toTransfer = contractBalance;
       contractBalance = 0;
       bool reqFund = true;

       msg.sender.transfer(toTransfer);

       return (toTransfer, reqFund);
   }

}
