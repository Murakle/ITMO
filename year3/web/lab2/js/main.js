const cloudiness = ['Sunny', 'Partly cloudy', 'Broken clouds', 'Cloudy'];
const directions = ['North', 'North-East', 'East', 'South-East', 'South', 'South-West', 'West', 'North-West'];

function parseWindDeg(deg) {
  degrees = Math.round(deg * 8 / 360);
  degrees = (degrees + 8) % 8
  return directions[degrees];
}

function parseResponse(responseText) {
  let info = JSON.parse(responseText);
  city = {
    "name": `${info.name}`,
    "temp": `${Math.round(info.main.temp)}ºC`,
    "wind": `${info.wind.speed} m/s, ${parseWindDeg(info.wind.deg)}`,
    "pres": `${info.main.pressure} hpa`,
    "hum": `${info.main.humidity} %`,
    "coord": `[${info.coord.lat}, ${info.coord.lon}]`,
    "cloud": `${cloudiness[Math.trunc(info.clouds.all * 4 - 1e-9)]}`,
    "icon": `http://openweathermap.org/img/wn/${info.weather[0].icon}@4x.png`
  };
  console.log(city);
  return city;
}

function refreshCityParams(paramsBlock, city) {
  paramsBlock.querySelector('.weather-wind').querySelector('.weather-param-value').innerHTML = city.wind;
  paramsBlock.querySelector('.weather-cloud').querySelector('.weather-param-value').innerHTML = city.cloud;
  paramsBlock.querySelector('.weather-pressure').querySelector('.weather-param-value').innerHTML = city.pres;
  paramsBlock.querySelector('.weather-humidity').querySelector('.weather-param-value').innerHTML = city.hum;
  paramsBlock.querySelector('.weather-coord').querySelector('.weather-param-value').innerHTML = city.coord;
}

function refreshMajorCity(city) {
  let majorCity = document.querySelector('.major-city');
  let majorCityHeader = majorCity.querySelector('.major-city-header');
  let majorCityTemp = majorCity.querySelector('.major-city-temperature');
  let majorCityIcon = majorCity.querySelector('.major-city-weather-icon');
  majorCityHeader.innerHTML = city.name;
  majorCityTemp.innerHTML = city.temp;
  majorCityIcon.src = city.icon;
  let paramsBlock = majorCity.querySelector('ul');
  refreshCityParams(paramsBlock, city);
}

function getRequestWithLocation(position) {
  const latitude  = position.coords.latitude;
  const longitude = position.coords.longitude;
  console.log(`Latitude: ${latitude} °, Longitude: ${longitude} °`);
  const data = null;
  const xhr = new XMLHttpRequest();
  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      console.log(this.responseText);
      city = parseResponse(this.responseText);
      refreshMajorCity(city);
    }
  });
  xhr.open("GET", `https://community-open-weather-map.p.rapidapi.com/weather?lat=${latitude}&lon=${longitude}&lang=en&units=metric`);
  xhr.setRequestHeader("x-rapidapi-key", "dc1339089bmshce8aa1495e73b22p119cc5jsn2333ba2ed2b7");
  xhr.setRequestHeader("x-rapidapi-host", "community-open-weather-map.p.rapidapi.com");
  xhr.send(data);
}
function geolocationError() {
  errorText = document.querySelector('.error-text');
  errorText.classList.remove('hidden');
}
function geolocationSuccess(position) {
  let welcomPopup = document.querySelector('.welcome-pop-up');
  welcomPopup.classList.add('hidden');
  document.body.classList.remove('body-noscroll');
  getRequestWithLocation(position);
}

function getRequestWithCityName() {
  city_name = "Kazan";
  const data = null;
  const xhr = new XMLHttpRequest();
  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      console.log(this.responseText);
      city = parseResponse(this.responseText);
      refreshMajorCity(city);
    }
  });
  xhr.open("GET", "https://community-open-weather-map.p.rapidapi.com/weather?q=Moscow,ru&lang=en&units=metric");
  xhr.setRequestHeader("x-rapidapi-key", "dc1339089bmshce8aa1495e73b22p119cc5jsn2333ba2ed2b7");
  xhr.setRequestHeader("x-rapidapi-host", "community-open-weather-map.p.rapidapi.com");
  xhr.send(data);
}


let showButton = document.querySelector('.show-weather-button');
let geoButton = document.querySelector('.use-geolocation-button');

geoButton.addEventListener("click", function (evt) {
  evt.preventDefault();
  if(!navigator.geolocation) {
    geolocationError();
  } else {
    console.log('Locating…');
    navigator.geolocation.getCurrentPosition(geolocationSuccess, geolocationError);
  }
});
showButton.addEventListener("click", function (evt) {
  evt.preventDefault();
  
});


