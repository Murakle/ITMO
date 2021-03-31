
module.exports = {


  friendlyName: 'Get weather by name',


  description: '',


  inputs: {
    cityName: {
        type: 'string',
        example: 'Moscow',
        description: 'The name of the city',
        required: true
    }
  },

  exits: {
    cityNotFound: {
      status: 404,
      description: "City not found"
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
        params: {q: inputs.cityName, lang: 'en', units: 'metric'},
        
        headers: {
        'x-rapidapi-key': '7f6c7b7f57msh8c957df57e3703bp115534jsn1145a5c9ed37',
        'x-rapidapi-host': 'community-open-weather-map.p.rapidapi.com',
        'x-rapidapi-ua' : 'RapidAPI-Playground'
        }
     };
    axios.request(options).then(function (response) {
      return exits.success(response.data);
    }).catch(function (error) {
      if (error.response.status == 404) {
        return exits.cityNotFound();
      } else {
        sails.log(error.response.data);
        return exits.internalError();
      }
    });

  }


};

