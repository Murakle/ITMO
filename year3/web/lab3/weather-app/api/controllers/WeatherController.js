/**
 * WeatherController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */

module.exports = {
  
  getWeatherByName: async (req, res) => {
    let cityName = req.param('cityName');
    sails.log(cityName);
    if (cityName) {
      let weather = null;
      try {
        weather = await sails.helpers.getWeatherByName(cityName);
      } catch(err) {
        switch(err.code) {
          case 'cityNotFound': return res.notFound();
          default: return res.serverError();
        }
      }
      return res.json(weather);
    }
    return res.badRequest();
  },

  getWeatherByCoord: async (req, res) => {
    let lat = req.param('lat');
    let lon = req.param('lon');
    if (lat && lon) {
      let weather = null;
      try {
        weather = await sails.helpers.getWeatherByCoord(lon, lat);
      } catch(err) {
        switch(err.code) {
          case 'coordNotFound': return res.badRequest();
          default: return res.serverError();
        }
      }
      return res.json(weather);
    }
    return res.badRequest();
  }
};

