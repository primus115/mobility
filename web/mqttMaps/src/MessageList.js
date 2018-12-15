import React, { Component } from 'react';
import Map from 'pigeon-maps'
import Marker from 'pigeon-marker/react'
import Overlay from 'pigeon-overlay'
import man from './img/baseline.png'
import Mqtt from 'mqtt'
import { Button, Dropdown } from 'semantic-ui-react'

const id = "0Xasdf"

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
		appPos: { lat: 46.04318, lon: 14.49486},
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
      mqttClient.subscribe(`res/${id}/#`)
    })

    mqttClient.on('message', (topic, message) => {
      let msg
      try {
        msg = JSON.parse(message.toString())
//		console.log(msg)
		this.state.messageList.push(msg)
      } catch (e) {
        console.error('Json parsing fails！')
        return
      }

	  if (topic === 'pos/slovenia/ljubljana') {
		const newPos = {...this.state.pos, lat: msg.lat, lon: msg.lon}
		this.setState({ pos: newPos})
		console.log(this.state.pos)
	  }
	  if (topic === `res/${id}/duration`) {
//		const newPos = {...this.state.pos, lat: msgArray.lat, lon: msgArray.lon}
//		this.setState({ pos: newPos})
//		console.log(this.state.pos)
		console.log(msg)
		console.log(msg.duration.minutes)
		console.log(msg.duration.seconds)
	  }

    })

    this.client = mqttClient
}

//  				<Marker anchor={[lat, lon]} payload={1} />
//  				<Marker anchor={[this.state.pos.lat, this.state.pos.lon]} payload={1} />
//  		  <ul>
 // 			{this.props.data.value}
  //		  </ul>
  
  handleClick = () => {
	  const { value, appPos } = this.state
	  this.client.publish("req/slovenia/ljubljana", JSON.stringify({id:id, destLat: value[0], destLon: value[1], appLat: appPos.lat, appLon: appPos.lon }))
  }

  handleChange = (e, { value }) => this.setState({ value })
 
  render() {
	  const { value, pos, appPos } = this.state

  	  return (
  		<div>
  		  <h3>Messages</h3>
 			<div>map</div>
  			<Map center={[46.0438, 14.4947]} zoom={14} width={1200} height={600}>
  				<Marker anchor={[pos.lat, pos.lon]} payload={1} />
  			    <Overlay anchor={[appPos.lat, appPos.lon]} offset={[10, 5]}>
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
					multiple={true}
				/>
				<Button size='small' primary content='Request a Trip!' onClick={this.handleClick}/>
				<pre>Current value: {value}</pre>
			</div>
  		</div>
  	  )
  }
}


export default MessageList;
