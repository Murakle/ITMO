const cloudiness = ['Clear', 'Partly cloudy', 'Broken clouds', 'Cloudy'];
const directions = ['North', 'North-East', 'East', 'South-East', 'South', 'South-West', 'West', 'North-West'];
let majorCity = document.querySelector('.major-city');
let welcomePopup = document.querySelector('.welcome-pop-up');
let minorCityTemplate = document.querySelector('#minor-city-template');
let minorCitiesList = document.querySelector('.minor-cities-list');
// let cities = JSON.parse(localStorage.getItem('cities'));

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
    "icon": `https://openweathermap.org/img/wn/${info.weather[0].icon}@4x.png`
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
function request(requestString, resultBlock, resultHandler, type) {
  const data = null;
  const xhr = new XMLHttpRequest();
  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      resultHandler(resultBlock, this);
    }
  });
  xhr.open(type, requestString);
  xhr.send(data);
}
function getRequest(requestString, resultBlock, resultHandler) {
  request(requestString, resultBlock, resultHandler, "GET");
}
function postRequest(requestString, resultBlock, resultHandler) {
  request(requestString, resultBlock, resultHandler, "POST");
}
function deleteRequest(requestString, resultBlock, resultHandler) {
  request(requestString, resultBlock, resultHandler, "DELETE");
}
function geolocationError() {
  errorText = document.querySelector('.geoloc-error');
  errorText.classList.remove('hidden');
}
function geolocationSuccess(position) {
  getRequestWithLocation(position, majorCity, majorHandler);
}
function majorHandler(resultBlock, answer) {
  if (answer.status === 200) {
    let city = parseResponse(answer.responseText);
    refreshCity(resultBlock, city);
    let majorCityHid = majorCity.querySelectorAll('.shrink-block');
    majorCityHid.forEach(element => {
      element.classList.remove('hidden');
    });
    majorCity.querySelector('.loading-block').classList.add('hidden');
    closePopup();
  } else if (answer.status === 404) {
    errorText = welcomePopup.querySelector('.city-name-error');
    errorText.classList.remove('hidden');
  } else {
    alert("Something went wrong");
  }
}
function minorAddHandler(resultBlock, answer) {
  if (answer.status === 200) {
    let city = parseResponse(answer.responseText);
    refreshCity(resultBlock, city);
    resultBlock.querySelector('ul').classList.remove('hidden');
    resultBlock.querySelector('.loading-block').classList.add('hidden');
  } else if (answer.status === 404) {
    resultBlock.remove();
    alert("No city with this name");
  } else if (answer.status === 400) {
    resultBlock.remove();
    alert('City with this name is already in favorites');
  } else {
    resultBlock.remove();
    alert("Something went wrong");
  }
}

function minorStartHandler(resultBlock, answer) {
  if (answer.status === 200) {
    let city = parseResponse(answer.responseText);
    refreshCity(resultBlock, city);
    resultBlock.querySelector('ul').classList.remove('hidden');
    resultBlock.querySelector('.loading-block').classList.add('hidden');
  } else if (answer.status === 404) {
    alert("No city with this name");
  } else {
    alert("Something went wrong");
  }
}

function removeMinorCity(evt) {
  evt.preventDefault();
  block = this.parentNode.parentNode;
  cityName = block.getAttribute('cityName');
  deleteRequestWithCityName(cityName, block, function(block, answer){
    if (answer.status === 200) {
      block.remove();  
    } else {
      alert("Something went wrong");
    }
    
  });
}

function getRequestWithLocation(position, resultBlock, resultHandler) {
  const latitude  = position.coords.latitude;
  const longitude = position.coords.longitude;
  getRequest(`http://localhost:1337/weather/coordinates?lat=${latitude}&lon=${longitude}`, resultBlock, resultHandler);
  // https://community-open-weather-map.p.rapidapi.com/weather?lat=${latitude}&lon=${longitude}&lang=en&units=metric`, resultBlock, resultHandler);
}
function getRequestWithCityName(cityName, resultBlock, resultHandler) {
  getRequest(`http://localhost:1337/weather/city?cityName=${cityName}`, resultBlock, resultHandler);
}

function postRequestWithCityName(cityName, resultBlock, resultHandler) {
  postRequest(`http://localhost:1337/favorites?cityName=${cityName}`, resultBlock, resultHandler);
}
function deleteRequestWithCityName(cityName, resultBlock, resultHandler) {
  deleteRequest(`http://localhost:1337/favorites?cityName=${cityName}`, resultBlock, resultHandler);
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
  getRequestWithCityName(cityName, majorCity, majorHandler);
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
let cities = [];
function getFavorites() {
  getRequest("http://localhost:1337/favorites", null, function(resultBlock, answer){
    if (answer.status === 200) {
      let cities_obj = JSON.parse(answer.responseText);
      let cities_names = cities_obj.map(e => e.name);
      console.log(cities_names);
      cities = cities_names;
      initMinorCities();
    } else {
      alert("Something went wrong");
    }
  });
}


getFavorites();
function initMinorCities() {
  for (let i = 0; i < cities.length; i++) {
    let clone = document.importNode(minorCityTemplate.content.firstElementChild, true);
    clone.querySelector('.city-header').innerHTML = cities[i];
    clone.setAttribute('cityName', cities[i]);
    let closeButton = clone.querySelector('.minor-city-remove-button');
    closeButton.addEventListener('click', removeMinorCity);
    minorCitiesList.appendChild(clone);
  }
  for (let i = 0; i < cities.length; i++) {
    let clone = minorCitiesList.childNodes[i];
    getRequestWithCityName(cities[i], clone, minorStartHandler);
  }
}
// minor cities header 
let addForm = document.querySelector('.add-favorite');
addForm.addEventListener("submit", function (evt) {
  evt.preventDefault();
  let cityName = addForm.cityName.value.toLowerCase();
  addForm.cityName.value = "";
  let clone = document.importNode(minorCityTemplate.content.firstElementChild, true);
  clone.setAttribute('cityName', cityName);
  clone.querySelector('.city-header').innerHTML = cityName;
  let closeButton = clone.querySelector('.minor-city-remove-button');
  closeButton.addEventListener('click', removeMinorCity);
  minorCitiesList.appendChild(clone);
  postRequestWithCityName(cityName, clone, minorAddHandler);
});
