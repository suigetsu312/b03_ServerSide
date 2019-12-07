var express = require('express');
var request = require('request');
var path = require('path');
//get app's root path
var root = path.dirname(require.main.filename)
//file system
var fs = require('fs');
//gets db
const { pool } = require("../db/index");
var api = express.Router();

api.get('/takePic', function(req,res,next){
	req.pipe(request.get('http://140.137.132.172:2004/cur_shot', { json: true, body: req.body }), { end: false }).pipe(res);
});

api.post('/StoreSample',function(req,res,next){
	var data = JSON.parse(req.body.Samples)
	var image = data.imageBase64;
	var Samples = data.Samples;

	var now = Date.now();
	var imagePath = root+'/Public/Sample/' + now + ".png";
	fs.writeFile('./public/Sample/'+ now +'.png', image, {encoding: 'base64',flag:'w+'},function(err) {
		console.log(err);
	});

	pool.connect((err, client, done) => {
		if (err) throw new Error(err);
		client.query('INSERT INTO "B03_Coffee"."Samples"("Sample_ImagePath", "Sample_Data", "Sample_Date") VALUES ($1, $2, to_timestamp($3));',[imagePath,JSON.stringify(data.Samples), now], (err, res) => {
		  done()
		  if (err) {
			console.log(err.stack)
		  } else {
			console.log(res.rows[0])
		  }
		})
	})	
})

module.exports = api