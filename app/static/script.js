

function bar() {
  const el = document.getElementById("button-light-switch");
  console.log("Хуй Полуэктова")
  let req = new XMLHttpRequest();
  if (flag == 1) {
	  el.innerHTML = "ON";
	  req.open("GET", "/apiOn");
	  flag = 0;
  } else {
	  el.innerHTML = "OFF";
	  req.open("GET", "/apiOff");
	  flag = 1;
  }
  req.send();
}

function reqestData() {
	let req = new XMLHttpRequest();
	
	req.open("GET", "/api");
	req.send();
	
	req.onreadystatechange = function () {
    if (this.readyState == "4" && this.status == "200") {
      const resp = JSON.parse(req.responseText);
      
      const humidity = document.getElementById("humidity");
      humidity.innerHTML = resp["humidity"];
      
      const temp = document.getElementById("temp");
      temp.innerHTML = resp["temp"];
      
      const soilMoistrue = document.getElementById("soil-moistrue");
      soilMoistrue.innerHTML = resp["soilMoistrue"];
      
      const lighting = document.getElementById("lighting");
      lighting.innerHTML = resp["lighting"];
    }
  };
}

const button = document.getElementById("button-light-switch");
button.addEventListener("click", bar);

var flag = 1

setInterval(reqestData, 2000);
