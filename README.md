# Mobility Platform  

### About the project
Inspired from and for the [Mobi Grand Challenge](https://mobihacks.devpost.com/).  
Goal is to make a mobility platform what will represent the point where different tehnologies can intersect. It can be used for testing, simulation and production.   

First stage is to confirm the desired interaction between different tehnologies.  
Status: Functional Test Mode

### Tehnologies
- [Ethereum](https://www.ethereum.org/) - Decentralized platform that runs smart contracts
- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [SUMO](http://sumo.dlr.de/index.html) - Simulation of Urban MObility
- [MQTT](http://mqtt.org/) - Machine-to-machine (M2M) "Internet of Things" connectivity protocol
- [web3.js](https://web3js.readthedocs.io/en/1.0/) - Ethereum JavaScript API
- [web3.py](https://web3py.readthedocs.io/en/stable/) - Ethereum Python API
- [Solidity](https://solidity.readthedocs.io/en/latest/) - Contract-oriented programming language for writing smart contracts
- [MetaMask](https://metamask.io/) - Browser plugin that allows you to run Ethereum dApps in your browser without running a full Ethereum node
- [ocean protocol](https://oceanprotocol.com/) - A protocol and network, on which data marketplaces can be built

### Structure of the repository
Simulation DApp sources: [./](./)  
- main app: [runner.py](./runner.py)  

Web DApp sources: [./web/mqttMaps](./web/mqttMaps/)  
- main app: [MqttMap.js](./web/mqttMaps/src/MqttMap.js)  

Ethereum sources: [./web/mqttMaps/src/ethereum/](./web/mqttMaps/src/ethereum)  
- contracts: [DecentralizedMobilitySystem_V01.sol](./web/mqttMaps/src/ethereum/contracts/DecentralizedMobilitySystem_V01.sol)

### Arhitecture
![](./pictures/Mobility_Platform_Architecture.png "Mobility Platform Architecture")


![](./pictures/Smart_contracts_architecture.png "Smart Contracts Architecture")

### Description of the architecture
#### 1. Ethereum smart contracts (Developed)  
Ethereum smart contracts where are all the rules and users are stored and ready for interaction.  

**1.1 First layer platform contracts**  
In the first layer are the contracts that set the rules for the platform and store the data. Functional part and storage part are seperated, so if there is a need for critical functionality update of the platform, only **MobilityRegistry.sol** is updated and with the consensus the address of the new version of the contract is pushed and stored in the **MobilityStorage.sol**. and have permissions to interect with the storage contract. MobilityVersions stores addresses of updated **MobilityRegistry.sol** contracts, so DApps can ask for the address of the latest version.  

Deployed smart contracts on the Rinkeby Ethereum test net:  

**MobilityVersions**: 0xd067c87b3a4f7fd82542e4e6884d6e34d80de7de   
**MobilityStorage**: 0xed65fce4eac8430631b2b3f1d449c5c1d115c17e  
**MobilityRegistry**: 0x273532806a1d3a38197Ba46358Ea5eED756de7C1  

**1.2 Second layer platform "constructor" contracts**  
For now **MobilityAccount.sol** is the only one. If you want to offer a transportation services (like a taxi driver or a owner of the autonomous vehicle) than you will create new instance of this contract, with the help of the MobilityRegistry contract, where new instances of this contract are deployed. In the contract are defined functions like payRide, setDistance, getDistance, getIsPaid, price...  

**On this layer additional smart contracts can be created, that expands transportation segment also to other segments, like gas station segment (e.g. Tank&Drive&Bonuses), insurance segment (e.g. publish data get discount), used cars market (e.g. publish driver behaviour profile and real distances - trusted seller), autonomous vehicle manufacturing segment (e.g. publish valuable data to desired company or brokerage company), car manufacturers segment (e.g. publish feedback data for specific vehicle model for the instant closed manufacturing loop & get bonuses or discount with new one)...**

**1.3 Third layer user contracts instances**  
Here are the instaces of the deployed accounts. Owner is the wallet that created the instance with the **MobilityRegistry** contract. Different DApps interact with specific account through this instance contract. Founds that collects on the contract with doing transportation service, can be tranfered at any time to any wallet only by the owner of the contract instance.  

**1.4 Fourth layer user wallets**  
Ethereum wallets are used for interaction with the deployed smart contracts and for the transfering ether (paying) to the MobilityAccount smart contract that will do (or is done) the transportation service for us.  

**Monetization**:  
Every contract has the funciton ownerRetriveDonations(address receiver), that can be executed at any time by the owner of the contract (the wallet that was used for creating the contract instance).
For the monetization testing was implemented functionality in the MobilityAccount that sends received_amount/10 to the MobilityStorage contract, the rest stays on the MobilityAccount contract instance.   
At the moment the amount the price for transportation request is hardcoded in the MobilityAccount contract (0.01 ether/km). But can be upgraded that can be changed by the owner of the contract instance.  

\*\* If there is a platform desire to have a very small percentage income from the transactions, than upgrade is needed. Becouse of the immutability reasons, reciving function must be implemented in the first layer contract, which forwards calculated amount to the MobilityAccount contract instance. sends whole amount to MobilityRegistry contract and the defined percentage is returend.  

#### 2. DApp (partially developed)
DApp (Decentralized application), that can be used in two modes:  
1. Requesting a transportation   
	1.1 Mobile application  
	1.2 Buisiness application
2. Offer a transportation   
	2.1 Mobile application (real user)  
	2.2 Embedded application (autonomous vehicle)  

**1. Requesting a transportation**  

	1.1 Mobile application (working prototype)   
	Enter destination and from available offers pick the one that is fastest or cheapest.
	todo:  
	- google.maps api requests for cusotm destinations  
	- Register new account for the mobility platform  

	1.2 Buisiness application (idea - not developed) 
	This can be different logistic application that needs transfers of any kind of goods. Probably MobilityAccount contract must be upgraded in some way that transporter stakes some ether, which is released back to him when specific rules are setisfied.

	
**2. Offer a transportation**   
	2.1 Mobile application - real user (idea - not developed)   
	Use application in the mode where the app listens to the published transportation requests. The app automatically response with the distance and the price. If you get chosen, do the transportation service.   
Long term goal is to have only autonomous vehicles in the transportation services. But in reality there will be a symbiosis with our cars and fully autonomous cars. And the app can help us to build the next generation transportation services and optimised travell routes (with the help of AI and IoT for smart traffic ligths). Besides the offer of the transportation services is also idea to have optimized navigation systems that we are already using it.   
	2.2 Embedded application - autonomous vehicle (developed in the simulation)  
	Application can be used for connecting autonomous vehicles with the mobility platform. Vehicle can get get route request, send the command to the navigation system, pick up a passenger or some item, do payment request and automatically when the payment is done finish the transportation service.  

#### 3. SUMO Simulation (simulation script developed)  
SUMO is an open source, highly portable, microscopic and continuous traffic simulation package designed to handle large road networks. It is mainly developed by employees of the Institute of Transportation Systems at the German Aerospace Center. SUMO is open source, licensed under the EPLv2.  
Sumo was chosen because of quick testing and quick evaluation of developed mobility platform features (on application layer and blockchain layer). In that way automated testing can be developed. It also supports any desired city plan import. For the demonstration I imported a map of Ljubljana, the capital of Slovenia. You can define speed of simulation, custom or repeatable vehicle trips. Additionally the simulation can be use for producing a lot of traffic data that is needed by the sophisticaded AI and machine learning tools, for traffic optimization.  

#### 3. MQTT protocol (used by the DApps and simulation)  
MQTT (Message Queuing Telemetry Transport) is an ISO standard (ISO/IEC PRF 20922) publish-subscribe-based messaging protocol. It works on top of the TCP/IP protocol. It is designed for connections with remote locations where a "small code footprint" is required or the network bandwidth is limited.  
It is ideal for publishing location data with high frequency. 


#### 4. Artificial intelligence (not developed)  


#### 5. Data market - Ocean protocol (not developed)  


### Usage  
Docker

Demo DApp: http://www.mobi-dapp.com


### Video

<a href="http://www.youtube.com/watch?feature=player_embedded&v=OEyzdEqacko" target="_blank"><img src="http://img.youtube.com/vi/OEyzdEqacko/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

### TO-DO


### Author
Primož Zajec  
[@115Primus](https://twitter.com/115primus)



