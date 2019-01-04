import React, { Component } from 'react';
import './App.css';
import MqttMap from './MqttMap';

class App extends Component {
  render() {
    return (
      <div className="App">
		<link rel="stylesheet" href="//cdn.jsdelivr.net/npm/semantic-ui@2.4.0/dist/semantic.min.css"></link>
        <header>
		</header>
        <MqttMap/> 
      </div>
    );
  }
}

export default App;
