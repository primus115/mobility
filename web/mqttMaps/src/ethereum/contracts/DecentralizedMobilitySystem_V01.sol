/*
decentralized Mobility System
Copyright (C) 2018 Primoz Zajec

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation in version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

pragma solidity ^0.4.24;

contract MobilityVersions {

	// owner
	address owner;
	
	address[] public deployedRegistries;
    
	modifier restricted() {
		require(msg.sender == owner);
		_;
	}
    
	constructor() public {
		owner = msg.sender;
	}
    
    function pushNewVersion(address _newVersion) public restricted {
            deployedRegistries.push(_newVersion);
    }

	function getAllVersions() public view returns(address[]) {
	    return deployedRegistries;
	}
	
	function getLastVersion() public view returns(address) {
	    return deployedRegistries[deployedRegistries.length -1];
	}

	function ownerRetrieveDonations(address receiver) public restricted {
		receiver.transfer(address(this).balance);
	}
	
	function getBalance() public view restricted returns(uint balance) {
        balance = address(this).balance;
	}

}

contract MobilityStorage {
    
    // mappings to look up account names, account ids and addresses
	mapping (address => address) senderAddressToAccountAddress;
	mapping (uint => address) accountIdToAccountAddress;
	
	// might be interesting to see how many people use the system
	uint numberOfAccounts;
	
	address owner;
	address registry;
	
	//**********************************
	address[] public deployedAccounts;
	
	modifier restrictedToOwner() {
		require(msg.sender == owner);
		_;
	}
	
	modifier restrictedToRegistry() {
		require(msg.sender == registry);
		_;
	}
	
	constructor() public {
		owner = msg.sender;
		numberOfAccounts = 0;
	}
	
	function () public payable {	}
	
	function getNumberOfAccounts() public view returns (uint _numberOfAccounts) {
		_numberOfAccounts = numberOfAccounts;
	}

	function getAddressOfId(uint id) public view returns (address addr) {
		addr = accountIdToAccountAddress[id];
	}

	function getAddressOfSenderAddress(address senderAddr) public view returns 
		(address addr) {
		addr = senderAddressToAccountAddress[senderAddr];
	}
	
	function getDeployedAccounts() public view returns(address[]) {
		return deployedAccounts;
	}
	
	function getRegistryAddress() public view returns(address _registry) {
	    _registry = registry;
	}

	function pushDeployedAccount(address newAccount) public restrictedToRegistry {
        deployedAccounts.push(newAccount);
	}

	function setAccountIdToAccountAddress(address newAccount) 
	    public restrictedToRegistry {
        accountIdToAccountAddress[numberOfAccounts] = newAccount;
	}
	
	function setSenderAddressToAccountAddress(address sender, address newAccount)
	    public restrictedToRegistry {
        senderAddressToAccountAddress[sender] = newAccount;
	}
	
	function incNumberOfAccounts() public restrictedToRegistry {
	    numberOfAccounts++;
	}
	
	function setRegistryAddress(address _registry) public restrictedToOwner {
	    registry = _registry;
	}

	function ownerRetrieveDonations(address receiver) public restrictedToOwner {
		receiver.transfer(address(this).balance);
	}
	
	function getBalance() public view restrictedToOwner returns(uint balance) {
        balance = address(this).balance;
	}
	
}

contract MobilityRegistry {
    

    MobilityStorage mobilityStorage;
	//address storageAddress;    
    
    // if a newer version of this registry is available, force users to use it
	bool registrationDisabled;

	// owner
	address owner;


	event returnStatus (int status);
	
	modifier restricted() {
		require(msg.sender == owner);
		_;
	}
	
	constructor(address _storageAddress) public {
		owner = msg.sender;
		registrationDisabled = false;
		mobilityStorage = MobilityStorage(_storageAddress);
	}
	
	function () public payable {	}
	
	function createAccount() public returns (int result) {
		if (registrationDisabled){
			// registry is disabled because a newer version is available
			result = -1;
		} else if (mobilityStorage.getAddressOfSenderAddress(msg.sender) != address(0)){
			// your profile already registered
			result = -2;
		} else {
			address newAccount = new MobilityAccount(msg.sender, mobilityStorage);
			mobilityStorage.pushDeployedAccount(newAccount);
			mobilityStorage.setAccountIdToAccountAddress(newAccount);
			mobilityStorage.setSenderAddressToAccountAddress(msg.sender, newAccount);
			mobilityStorage.incNumberOfAccounts();
			result = 0; // success
		}

		emit returnStatus(result);
	}
	
	function adminSetRegistrationDisabled(bool _registrationDisabled) public restricted {
		// currently, the code of the registry can not be updated once it is
		// deployed. if a newer version of the registry is available, account
		// registration can be disabled
		registrationDisabled = _registrationDisabled;
	}
	
	function ownerRetrieveDonations(address receiver) public restricted {
		receiver.transfer(address(this).balance);
	}
	
	function getBalance() public view restricted returns(uint balance) {
        balance = address(this).balance;
	}

}

contract MobilityAccount {
    
	MobilityStorage mobilityStorage; 
	MobilityAccount mobilityAccount;
    
    // mapping for random trip id
	mapping (uint => bool) isPaid;
	uint distance;
	
	address public owner;
	
	event returnSetDistance (bool _status);
	
	modifier restricted() {
		require(msg.sender == owner);
		_;
	}
	
    modifier costs(uint _amount) {
        require(
            msg.value >= _amount,
            "Not enough Ether provided."
        );
        _;
        if (msg.value > _amount) {
            msg.sender.transfer(msg.value - _amount);
            address(mobilityStorage).transfer(_amount / 10);
            address(this).transfer(9 * _amount / 10);
        }
        else {
            address(mobilityStorage).transfer(_amount / 10);
            address(this).transfer(9 * _amount / 10);
        }
    }

    constructor(address creator, address storageAddress) public {
		owner = creator;
		mobilityStorage = MobilityStorage(storageAddress);
		distance = 0;
	}

    // client first setDistance then generates number for isPaid[number]
    function setDistance(uint _distance) public restricted {
        distance = _distance;
        emit returnSetDistance(true);
    }

    // distance is in meters, price is cca. 0.01 ether/km
	function payRide(uint number) public payable costs(distance * 0.00001 ether) {
	    isPaid[number] = true;
	}
	
	function getDistance() public view returns(uint _distance) {
	    _distance = distance;
	}
	
	function getIsPaid(uint id) public view returns(bool _isPaid) {
	    _isPaid = isPaid[id];
	}
	
	function () public payable {	}

	function ownerRetrieveDonations(address receiver) public restricted {
		receiver.transfer(address(this).balance);
	}
	
	function getBalance() public view restricted returns(uint balance) {
        balance = address(this).balance;
	}
}
//TO-DO:
// 
