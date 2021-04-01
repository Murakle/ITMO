/**
 * FavoritesController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */

module.exports = {
  getFavorites: async (req, res) => {
    
    Favorites.find().exec(function (err, name) {
        if (err) return res.serverError();
        return res.json(name);
    })
  },
  
  addFavorite: async (req, res) => {
    let cityName = req.param('cityName');
    if (!cityName) {
        return res.badRequest();
    }
    var weather = null;
    try {
      weather = await sails.helpers.getWeatherByName(cityName);
    } catch(err) {
      switch(err.code) {
        case 'cityNotFound': return res.notFound();
        default: return res.serverError();
      }
    }
    cityName = weather.name;
    var amountCityName = await Favorites.count({name: cityName});
    if (amountCityName == 0) {
      Favorites.create({name: cityName}).fetch().exec(function (err, name) {
        if (err) return res.serverError();
        sails.log("add ", cityName);
        return res.json(weather);
      })
    } else {
      return res.badRequest();
    }
    
  },

  deleteFavorite: async (req, res) => {
    let cityName = req.param('cityName');
    if (!cityName) {
      return res.badRequest();
    }
    Favorites.destroy({name: cityName}).fetch().exec(function (err, name) {
        if (err) return res.serverError();
        sails.log("delete ", name);
        return res.json(name);
    })
  }
};

