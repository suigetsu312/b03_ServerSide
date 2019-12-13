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
	req.pipe(request.get('http://140.137.132.59:2004/cur_shot', { json: true, body: req.body }), { end: false }).pipe(res);
});

api.get('/detectBean', function(req,res,next){
	req.pipe(request.get('http://192.168.88.95:5000/detectBean', { json: true, body: req.body }), { end: false }).pipe(res);
});

api.post('/pick_bean', function(req,res,next){
	req.pipe(request.get('http://140.137.132.59:2004/pick_bean', { json: true, body: req.body }), { end: false }).pipe(res);
});

api.post('/StoreRecord', function(req,res,next){
	var data = req.body;
	//origin image path
	var OriImagePath = '/home/leeyihan/b03/ServerSide/imageLog/image/' + data.image;
	//record
	var beanRecord = JSON.stringify(data.Data);
	//detect time
	var nowTime = data.Date;
	//defect rate = amount of abnormal bean / amount of bean
	var DefectRate = data.defectRate;	

	pool.connect((err, client, done) => {
		if (err) throw new Error(err);
		client.query('INSERT INTO "B03_Coffee"."Record"( "Record_DefectRate", "Record_ImagePath", "Record_Data", "Record_Date") VALUES ($1, $2, $3, to_timestamp($4));',[DefectRate,OriImagePath,beanRecord, nowTime/1000], (error, result) => {
		  done()
		  if (error) {
			console.log('查詢失敗')
			console.log(error.stack)
			res.sendStatus(400)
		  } else {
			res.send(200,result.rows);
		  }
		})
	})
})

api.post('/GetRecord', function(req,res,next){
	var reqdata = req.body;
	var startDate = reqdata.start;
	var endDate = reqdata.end;
	console.log(startDate,endDate)

	pool.connect((err, client, done) => {
		if (err) throw new Error(err);
		client.query('SELECT "Record_DefectRate", "Record_Data", "Record_Date" FROM "B03_Coffee"."Record" WHERE "Record_Date" BETWEEN to_timestamp($1) AND to_timestamp($2)',[startDate/1000,endDate/1000], (error, result) => {
		  done()
		  if (error) {
			console.log('查詢失敗')
			console.log(error.stack)
			res.sendStatus(400)
		  } else {
			res.send(200,result.rows);
		  }
		})
	})	

})

api.post('/StoreSample',function(req,res,next){
	var resdata = req.body
	var image = resdata.imageBase64;
	var Samples = resdata.beans;
	var now = Date.now();
	var imagePath = root+'/Public/Sample/' + now + ".png";
	fs.writeFile('./public/Sample/'+ now +'.png', image, {encoding: 'base64',flag:'w+'},function(err) {
		console.log(err);
	});

	pool.connect((err, client, done) => {
		if (err) throw new Error(err);
		client.query('INSERT INTO "B03_Coffee"."Samples"("Sample_ImagePath", "Sample_Data", "Sample_Date") VALUES ($1, $2, to_timestamp($3))',[imagePath,Samples, now/1000], (error, result) => {
		  done()
		  if (error) {
			console.log('查詢失敗')
			console.log(error.stack)
			res.sendStatus(400)
		  } else {
			res.send(200,result.rows);
		  }
		})
	})	
})

module.exports = api