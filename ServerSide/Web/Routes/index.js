var express = require('express');
var Router = express.Router();


    
Router.get("/", function(request, response,next) {

    response.render("index");
});

Router.get("/CoffeePick", function(req,res,next){
	res.render("CoffeePick");
});

Router.get("/CoffeeLabel", function(req,res,next){
          
	res.render("CoffeeLabel");
});

Router.get("/CoffeeRecord", function(req,res,next){
	res.render("CoffeeRecord");
});
module.exports = Router