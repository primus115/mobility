import React, { Component } from 'react';
import './App.css';
import Map from 'pigeon-maps'
import Marker from 'pigeon-marker/react'
import { Connector } from 'mqtt-react';
import { subscribe } from 'mqtt-react';
import _MessageContainer from './MessageContainer';

//import mqtt from 'mqtt';

//componentDidMount(){
//  var client  = mqtt.connect('178.62.252.50:9001')
//  console.log(client);
//  // Don't call this.setState() here!
//  this.state = { counter: 0 };
//  this.handleClick = this.handleClick.bind(this);
//}

const MessageContainer = subscribe({topic: 'pos/#'})(_MessageContainer);

class App extends Component {
  render() {
    return (
      <Connector mqttProps="ws:178.62.252.50:9001">
      <div className="App">
        <header className="App-header">
			<div>map</div>
			<Map center={[46.056946, 14.505751]} zoom={14} width={1200} height={600}>
				<Marker anchor={[46.05, 14.50]} payload={1} onClick={this.handleMarkerClick} />
			</Map>
		</header>
      </div>
	    </Connector>
    );
  }
}

export default App;
