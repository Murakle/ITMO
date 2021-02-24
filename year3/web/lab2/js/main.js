const cloudiness = ['Clear', 'Partly cloudy', 'Broken clouds', 'Cloudy'];
const directions = ['North', 'North-East', 'East', 'South-East', 'South', 'South-West', 'West', 'North-West'];
let majorCity = document.querySelector('.major-city');
let welcomePopup = document.querySelector('.welcome-pop-up');
let minorCityTemplate = document.querySelector('#minor-city-template');
let currentCities = new Map(); // cityName, cityBlock
let minorCitiesList = document.querySelector('.minor-cities-list');
let cities = JSON.parse(localStorage.getItem('cities'));

function parseWindDeg(deg) {
  degrees = Math.round(deg * 8 / 360);
  degrees = (degrees + 8) % 8
  return directions[degrees];
}

function closePopup() {
  welcomePopup.classList.add('hidden');
  document.body.classList.remove('body-noscroll');
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
    "cloud": `${cloudiness[Math.trunc(info.clouds.all / 25 - 1e-9)]}`,
    "icon": `http://openweathermap.org/img/wn/${info.weather[0].icon}@4x.png`
  };
  // console.log(city);
  return city;
}

function refreshCityParams(paramsBlock, city) {
  paramsBlock.querySelector('.weather-wind').querySelector('.weather-param-value').innerHTML = city.wind;
  paramsBlock.querySelector('.weather-cloud').querySelector('.weather-param-value').innerHTML = city.cloud;
  paramsBlock.querySelector('.weather-pressure').querySelector('.weather-param-value').innerHTML = city.pres;
  paramsBlock.querySelector('.weather-humidity').querySelector('.weather-param-value').innerHTML = city.hum;
  paramsBlock.querySelector('.weather-coord').querySelector('.weather-param-value').innerHTML = city.coord;
}

function refreshCity(cityBlock, city) {
  cityBlock.querySelector('.city-header').innerHTML = city.name;
  cityBlock.querySelector('.city-temperature').innerHTML = city.temp;
  cityBlock.querySelector('.city-weather-icon').src = city.icon;
  let paramsBlock = cityBlock.querySelector('ul');
  refreshCityParams(paramsBlock, city);
}
function getRequest(requestString, resultBlock, successFunc, errorFunc) {
  const data = null;
  const xhr = new XMLHttpRequest();
  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      if(this.status === 200) {
        let city = parseResponse(this.responseText);
        successFunc(resultBlock, city.name);
        refreshCity(resultBlock, city);
      } else {
        errorFunc();
      }
    }
  });
  xhr.open("GET", requestString);
  xhr.setRequestHeader("x-rapidapi-key", "dc1339089bmshce8aa1495e73b22p119cc5jsn2333ba2ed2b7");
  xhr.setRequestHeader("x-rapidapi-host", "community-open-weather-map.p.rapidapi.com");
  xhr.send(data);
}

function geolocationError() {
  errorText = document.querySelector('.geoloc-error');
  errorText.classList.remove('hidden');
}
function geolocationSuccess(position) {
  getRequestWithLocation(position, majorCity, majorSuccess, majorError);
}
function majorError() {
  errorText = welcomePopup.querySelector('.city-name-error');
  errorText.classList.remove('hidden');
}
function minorError() {
  alert("No city with this name");
}
function minorStartSuccess(clone, cityName) {
  
  localStorage.setItem('cities', JSON.stringify(Array.from(currentCities.keys())));
  clone.querySelector('ul').classList.remove('hidden');
  clone.querySelector('.loading-block').classList.add('hidden');
}
function minorSuccess(clone, cityName) {
  minorCitiesList.appendChild(clone);
  currentCities.set(cityName, clone);
  localStorage.setItem('cities', JSON.stringify(Array.from(currentCities.keys())));
  clone.querySelector('ul').classList.remove('hidden');
  clone.querySelector('.loading-block').classList.add('hidden');
}
function majorSuccess(clone, cityName) {
  let majorCityHid = majorCity.querySelectorAll('.shrink-block');
  majorCityHid.forEach(element => {
    element.classList.remove('hidden');
  });
  majorCity.querySelector('.loading-block').classList.add('hidden');
  closePopup();
}
function removeMinorCity(evt) {
  evt.preventDefault();
  block = this.parentNode.parentNode;
  cityName = block.getAttribute('cityName');
  block.remove();
  currentCities.delete(cityName);
  localStorage.setItem('cities', JSON.stringify(Array.from(currentCities.keys())));
}
function getRequestWithLocation(position, resultBlock, successFunc, errorFunc) {
  const latitude  = position.coords.latitude;
  const longitude = position.coords.longitude;
  getRequest(`https://community-open-weather-map.p.rapidapi.com/weather?lat=${latitude}&lon=${longitude}&lang=en&units=metric`, resultBlock, successFunc, errorFunc);
}
function getRequestWithCityName(cityName, resultBlock, successFunc, errorFunc) {
  getRequest(`https://community-open-weather-map.p.rapidapi.com/weather?q=${cityName}&lang=en&units=metric`, resultBlock, successFunc, errorFunc);  
}

// Major city 
let geoButton = document.querySelector('.use-geolocation-button');
let welcomeForm = document.querySelector('.pop-up-form');
let refreshButton = document.querySelector('.refresh-button');
geoButton.addEventListener('click', function (evt) {
  evt.preventDefault();
  if(!navigator.geolocation) {
    geolocationError();
  } else {
    console.log('Locating…');
    navigator.geolocation.getCurrentPosition(geolocationSuccess, geolocationError);
  }
});
welcomeForm.addEventListener('submit', function (evt) {
  evt.preventDefault();
  let cityName = welcomeForm.cityName.value;
  getRequestWithCityName(cityName, majorCity, majorSuccess, majorError);
});
refreshButton.addEventListener('click', function (evt) {
  evt.preventDefault();
  if(!navigator.geolocation) {
    geolocationError();
  } else {
    console.log('Locating…');
    navigator.geolocation.getCurrentPosition(geolocationSuccess, geolocationError);
  }
});

// Minor cities 
if(!cities) {
  cities = [];
  localStorage.setItem('cities', JSON.stringify(cities));
  citiesAmount = 0;
}
console.log(cities);
for (let i = 0; i < cities.length; i++) {
  let clone = document.importNode(minorCityTemplate.content.firstElementChild, true);
  clone.querySelector('.city-header').innerHTML = cities[i];
  clone.setAttribute('cityName', cities[i]);
  let closeButton = clone.querySelector('.minor-city-remove-button');
  closeButton.addEventListener('click', removeMinorCity);
  minorCitiesList.appendChild(clone);
  currentCities.set(cities[i], clone);
}
for (let i = 0; i < cities.length; i++) {
  let clone = minorCitiesList.childNodes[i];
  console.log(clone);
  getRequestWithCityName(cities[i], clone, minorStartSuccess, minorError);
}
// minor cities header 
let addForm = document.querySelector('.add-favorite');
addForm.addEventListener("submit", function (evt) {
  evt.preventDefault();
  let cityName = addForm.cityName.value;
  if (currentCities.has(cityName)) {
    alert("This city is already in favorites");
  } else {
    let clone = document.importNode(minorCityTemplate.content.firstElementChild, true);
    clone.setAttribute('cityName', cityName);
    let closeButton = clone.querySelector('.minor-city-remove-button');
    closeButton.addEventListener('click', removeMinorCity);
    getRequestWithCityName(cityName, clone, minorSuccess, minorError);
  }
});

// todo 
// 1. remove buttons √
// 2. refresh  button √
// 3. loading block 
// 4. css popup