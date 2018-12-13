import React, { Component } from 'react';
import './App.css';
import MessageList from './MessageList';

//			<div>map</div>
//			<Map center={[46.056946, 14.505751]} zoom={14} width={1200} height={600}>
//				<Marker anchor={[46.05, 14.50]} payload={1} onClick={this.handleMarkerClick} />
//			</Map>

class App extends Component {
  render() {
    return (
      <div className="App">
		<link rel="stylesheet" href="//cdn.jsdelivr.net/npm/semantic-ui@2.4.0/dist/semantic.min.css"></link>
        <header>// className="App-header">
		</header>
        <MessageList/> 
      </div>
    );
  }
}

export default App;
