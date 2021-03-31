module.exports = {




  friendlyName: 'Get weather by coordinates',


  description: '',


  inputs: {
    lon: {
      type: 'string',
      example: '12,1',
      required: true
    },
    lat: {
      type: 'string',
      example: '11,2',
      required: true
    }
  }, 

  exits: {
    coordNotFound: {
      status: 400,
      description: "Wrong coord"
    },
    internalError: {
      status: 500,
      description: "Some Internal error"
    }
  },

  fn: async function (inputs, exits) {
    var axios = require("axios").default;
    var options = {
        method: 'GET',
        url: 'https://community-open-weather-map.p.rapidapi.com/weather',
        params: { lat: inputs.lat, lon: inputs.lon, lang: 'en', units: 'metric'},
        headers: {
        'x-rapidapi-key': '7f6c7b7f57msh8c957df57e3703bp115534jsn1145a5c9ed37',
        'x-rapidapi-host': 'community-open-weather-map.p.rapidapi.com',
        'x-rapidapi-ua' : 'RapidAPI-Playground'
        }
     };
    axios.request(options).then(function (response) {
      return exits.success(response.data);
    }).catch(function (error) {
      if (error.response.status == 400) {
        return exits.coordNotFound();
      } else {
        sails.log(error.response.data);
        return exits.internalError();
      }
    });

  }


};

