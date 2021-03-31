/**
 * Route Mappings
 * (sails.config.routes)
 *
 * Your routes tell Sails what to do each time it receives a request.
 *
 * For more information on configuring custom routes, check out:
 * https://sailsjs.com/anatomy/config/routes-js
 */

module.exports.routes = {
  // favorite api
  'GET /favorites' : {controller: 'FavoritesController', action: 'getFavorites'},
  'POST /favorites' : {controller: 'FavoritesController', action: 'addFavorite'},
  'DELETE /favorites' : {controller: 'FavoritesController', action: 'deleteFavorite'},
  // get weather api
  'GET /weather/city' : {controller: 'WeatherController', action: 'getWeatherByName'},
  'GET /weather/coordinates' : {controller: 'WeatherController', action: 'getWeatherByCoord'}
};
