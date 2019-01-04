import React, { Component } from 'react';
import './App.css';
import MessageList from './MessageList';

class App extends Component {
  render() {
    return (
      <div className="App">
		<link rel="stylesheet" href="//cdn.jsdelivr.net/npm/semantic-ui@2.4.0/dist/semantic.min.css"></link>
        <header>
		</header>
        <MessageList/> 
      </div>
    );
  }
}

export default App;
