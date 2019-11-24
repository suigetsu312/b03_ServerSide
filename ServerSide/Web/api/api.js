var express = require('express');
var request = require('request')
var api = express.Router();

api.get('/takePic', function(req,res,next){
	req.pipe(request.get('http://140.137.132.172:2004/cur_shot', { json: true, body: req.body }), { end: false }).pipe(res);
});

module.exports = api