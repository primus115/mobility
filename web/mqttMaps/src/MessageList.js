import React, { Component } from 'react';
import Map from 'pigeon-maps'
import Marker from 'pigeon-marker/react'
import Overlay from 'pigeon-overlay'
import man from './img/baseline.png'
import Mqtt from 'mqtt'
import { Button, Dropdown } from 'semantic-ui-react'


const options = [
  { key: 1, text: 'Koseskega ulica 30', value: [ 46.03966, 14.49439 ] },
  { key: 2, text: 'Two', value: 2 },
  { key: 3, text: 'Three', value: 3 },
]

class MessageList extends Component {


  constructor(props) {
    super(props);
	this.state = {
		value: [ 46.03966, 14.49439 ],
		messageList: [],
		pos: { lat: null, lon: null},
		myPos: { lat: 46.04318, lon: 14.49486},
	}
  };

  componentDidMount() {
    this.mqttInit()
}

  componentWillUnmount() {
    // UnSubscribe mqtt
    if (this.client) {
      this.client.end(() => {
        console.log('Disconnect')
      })
    }
}

  mqttInit = () => {
    let mqttClient

    mqttClient = Mqtt.connect(`ws:178.62.252.50:9001`, {
	  rejectUnauthorized: false,
	  username: 'test',
  	  password: 'test',
    })

    mqttClient.on('connect', () => {
      this.setState({
        mqttError: true,
      })
      mqttClient.subscribe('pos/slovenia/ljubljana/#')
    })

    mqttClient.on('message', (topic, message) => {
      let msgArray
      try {
        msgArray = JSON.parse(message.toString())
//		console.log(msgArray)
		this.state.messageList.push(msgArray)
      } catch (e) {
        console.error('Json parsing fails！')
        return
      }

	  if (topic === 'pos/slovenia/ljubljana') {
		const newPos = {...this.state.pos, lat: msgArray.lat, lon: msgArray.lon}
		this.setState({ pos: newPos})
		console.log(this.state.pos)
	  }
//	  console.log(this.state.pos.lat);
//	  console.log(this.state.pos.lon);
    })

    this.client = mqttClient
}

//  				<Marker anchor={[lat, lon]} payload={1} />
//  				<Marker anchor={[this.state.pos.lat, this.state.pos.lon]} payload={1} />
//  		  <ul>
 // 			{this.props.data.value}
  //		  </ul>
  
  handleClick = () => {
	  const { value, myPos } = this.state
	  this.client.publish("req/slovenia/ljubljana", JSON.stringify({id:"0xABCD", lat: value[0], lon: value[1], myLat: myPos.lat, myLon: myPos.lon }))
  }

  handleChange = (e, { value }) => this.setState({ value })
 
  render() {
	  const { value, pos, myPos } = this.state

  	  return (
  		<div>
  		  <h3>Messages</h3>
 			<div>map</div>
  			<Map center={[46.0438, 14.4947]} zoom={14} width={1200} height={600}>
  				<Marker anchor={[pos.lat, pos.lon]} payload={1} />
  			    <Overlay anchor={[myPos.lat, myPos.lon]} offset={[10, 5]}>
  					<img src={man} width={60} height={40} alt='' />
  				</Overlay>
  			</Map>
 			<div>
				<Dropdown
					onChange={this.handleChange}
					options={options}
					placeholder='Choose an option'
					selection
					defaultValue={1}
					value={value}
				/>
				<Button size='small' primary content='Request a Trip!' onClick={this.handleClick}/>
				<pre>Current value: {value}</pre>
			</div>
  		</div>
  	  )
  }
}


export default MessageList;
