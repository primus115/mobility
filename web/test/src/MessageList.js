import React from 'react';
import Map from 'pigeon-maps'
import Marker from 'pigeon-marker/react'

export default ({data}) => {
  const dataList = data.map((d) => <li>{d}</li>)
//  const dataList = data;
  if (typeof data[0] != "undefined") {
	  const aaa = data[0].lat;
//	  const aaa = Object.keys(data[0]);
	  console.log("----------------");
	  console.log(aaa);
	  console.log(typeof aaa);
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
				<Marker anchor={[46.05, aaa]} payload={1} />
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
