/** 
 * Module responsible for communication directly with database.
 * @module Db */

const pg = require("pg");
const configDB  = require("./config");

const pool = new pg.Pool(configDB.config)


module.exports = {pool};