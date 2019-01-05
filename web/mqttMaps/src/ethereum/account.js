// api for returning abi from adress from whitin our app
import web3 from './web3';
import MobilityAccount from './build/MobilityAccountABI.json';

export default address => {
  return new web3.eth.Contract(MobilityAccount, address);
};
