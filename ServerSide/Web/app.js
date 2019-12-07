var http = require("http");
var path = require("path");
var express = require("express");
var logger = require("morgan");
var bodyParser = require("body-parser");
var cors = require("cors");
var app = express();

app.set("views", path.resolve(__dirname, "views"));
app.set("view engine", "ejs");
app.use(express.static(path.resolve(__dirname, "public")));


var api = require('./api/api');
var indexRouter = require('./Routes/index');
app.use(logger("dev"));
app.use(cors())

app.use(bodyParser.urlencoded({limit: '50mb', extended: true,parameterLimit: 50000 }));
app.use(bodyParser.json({limit : '50mb'})); 
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.use('/api', api)
app.use('/',indexRouter)

app.use(function(request, response,next) {
  response.status(404).render("404");
});
   
http.createServer(app).listen(3000, function() {
  console.log("started on port 3000.");
});