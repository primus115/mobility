import React, { Component } from 'react';
import Map from 'pigeon-maps'
import Marker from 'pigeon-marker/react'
import Overlay from 'pigeon-overlay'
import man from './img/baseline.png'
import Mqtt from 'mqtt'
import { Button, Dropdown, List } from 'semantic-ui-react'
import web3 from './ethereum/web3';
import Account from './ethereum/account';

const id = "0Xasdf"

const options = [
  { key: 1, text: 'Koseskega ulica 30', value: 1 },
  { key: 2, text: 'Two', value: 2 },
  { key: 3, text: 'Three', value: 3 }
]



class MqttMap extends Component {


  constructor(props) {
    super(props);
	this.state = {
		value: [ 46.03966, 14.49439 ],
		messageList: [],
		pos: { lat: null, lon: null},
		appPos: { lat: 46.04494, lon: 14.47917},
		rides: [],
		listVisible: 0
	}
  };

  async componentDidMount() {
    this.mqttInit()
//	const profile = await Account(address);
	const profile = await Account('0xf1080ce12d54d5d8076D3FA5A8aA48FaA2Ef0e17');
	const distance = await profile.methods.getDistance().call();
	console.log(distance)
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
		//console.log("MQTT:" + msg)
//		this.state.messageList.push(msg)
//		console.log("liiiiiiisssstaaaaa:::")
/		console.log(this.state.messageList)
      } catch (e) {
        console.error('Json parsing fails！')
        return
      }

	  if (topic === 'pos/slovenia/ljubljana') {
		const newPos = {...this.state.pos, lat: msg.lat, lon: msg.lon}
		this.setState({ pos: newPos})
//		console.log(this.state.pos)
	  }
	  if (topic === `res/${id}/duration`) {
//		const newPos = {...this.state.pos, lat: msgArray.lat, lon: msgArray.lon}
//		this.setState({ pos: newPos})
//		console.log(this.state.pos)
//asdf		this.setState({ })
//		this.state.rides.push(msg)
		const newRides = [...this.state.rides, msg]
		this.setState({ rides: newRides})
		console.log("riddddeeesss:")
		console.log(this.state.rides)
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
  
  generalRequestClick = () => {
	this.setState({ listVisible: 1 })
	const { value, appPos } = this.state
	this.setState({ rides: [] })
	this.client.publish("req/slovenia/ljubljana", JSON.stringify({id:id, destLat: value[0], destLon: value[1], appLat: appPos.lat, appLon: appPos.lon }))
  }

  handleChange = (e, { value }) => {
	this.setState({ rides: [] })
	if (value === 1) this.setState({ value: [ 46.03966, 14.49439 ] })
	if (value === 2) this.setState({ value: [ 46.03966, 14.49439 ] })
	if (value === 3) this.setState({ value: [ 46.03966, 14.49439 ] })
  }

  rideClick = (name) => {
	const { value, appPos } = this.state
	console.log("-------------")
	console.log("Ride click: " + name)
	this.client.publish(`req/${name}`, JSON.stringify({id:id, destLat: value[0], destLon: value[1], appLat: appPos.lat, appLon: appPos.lon }))
	this.setState({ listVisible: 0 })
  }

  renderList = (rides) => {
	if(this.state.listVisible){
		return(
			<div>
				<h3>Pick a ride:</h3>
				{rides.map((item, index) => (
					<List selection verticalAlign='middle' key={index}>
					  <List.Item onClick={() => this.rideClick(item.name)}>
						<List.Content>
						  <List.Header>{item.name}: {item.duration.minutes} minutes, {item.duration.seconds} seconds</List.Header>
						</List.Content>
					  </List.Item>
					</List>
				))}
			</div>
		)
	}
  }

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
					multiple={false}
				/>
				<Button size='small' primary content='Request a Ride!' onClick={this.generalRequestClick}/>
				{this.renderList(this.state.rides)}
			</div>
  		</div>
  	  )
  }
}


export default MqttMap;
