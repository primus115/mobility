import React from 'react';
import Map from 'pigeon-maps'
import Marker from 'pigeon-marker/react'

export default ({data}) => {
  const dataList = data.map((d) => <li>{d}</li>)
//  const dataList = data;
  if (typeof data[0] != "undefined") {
	  const lat = data[0].lat;
	  const lon = data[0].lon;
//	  const aaa = Object.keys(data[0]);
	  console.log("----------------");
	  console.log(typeof lat);
	  console.log(data[0]);
	  //const obj = JSON.parse(data[0]);
	  //console.log(obj);
	  return (
		<div>
		  <h3>Messages</h3>
		  <ul>
			{data.value}
		  </ul>
			<div>map</div>
			<Map center={[46.056946, 14.505751]} zoom={14} width={1200} height={600}>
				<Marker anchor={[lat, lon]} payload={1} />
			</Map>
		</div>
	  )
  }
  else {
	  return (
		  <div>
		  <h3>Messages</h3>
			<Map center={[46.056946, 14.505751]} zoom={14} width={1200} height={600}  />

		  </div>
	  )
  }
}
