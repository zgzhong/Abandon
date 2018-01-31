/* *
 * This js file will read the string of url
 * after the domain name 
 * */

var http = require('http');

http.createServer(function(req, res){
    res.write(req.url);
    res.end();
}).listen(8080);
