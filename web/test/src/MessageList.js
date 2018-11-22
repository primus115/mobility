import React from 'react';

export default ({data}) => {
  const dataList = data.map((d) => <li>{d}</li>)
//  const dataList = data;
  console.log("----------------");
  console.log(data);
//  const obj = JSON.parse(data);
  //console.log(obj);
  return (
    <div>
      <h3>Messages</h3>
      <ul>
        {dataList}
      </ul>
    </div>
  )
}
