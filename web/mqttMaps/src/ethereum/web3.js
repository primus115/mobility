import Web3 from 'web3';

let web3; // for reassigning the variable

if (typeof window !== 'undefined' && typeof window.web3 !== 'undefined') {
	// we are in the browser and metamask is running
	web3 = new Web3(window.web3.currentProvider); // whatever provider is metamask using
} else {
	// we are in the server *OR* the user is not running metamask
	const provider = new  Web3.providers.HttpProvider(
		'https://rinkeby.infura.io/v3/21eac8c7060f4f6584478c7aa44ffb87'
	);
	web3 = new Web3(provider);
}

export default web3;
