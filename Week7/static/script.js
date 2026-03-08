let chart;

async function loadStock(){

const symbol = document.getElementById("symbol").value;


// Current price

const priceRes = await fetch(`/stock/${symbol}`)
const priceData = await priceRes.json()

if(priceData.error){
alert("Invalid Symbol")
return
}

document.getElementById("priceBox").innerHTML =

`
<h2>${priceData.symbol}</h2>
<p>Price: $${priceData.price}</p>
<p>Change: ${priceData.change}</p>
<p>Percent: ${priceData.percent}</p>
`


// Historical data

const historyRes = await fetch(`/history/${symbol}`)
const historyData = await historyRes.json()


if(chart){
chart.destroy()
}

chart = new Chart(document.getElementById("chart"),{

type:"line",

data:{

labels: historyData.dates,

datasets:[{

label:"1 Year Price",

data: historyData.prices,

borderColor:"#00ff88",

borderWidth:2,

fill:false

}]

},

options:{

responsive:true,

plugins:{
legend:{display:true}
},

scales:{
x:{display:false}
}

}

})


document.getElementById("yearChange").innerHTML =

`1 Year Change: $${historyData.year_change} (${historyData.year_percent}%)`

}