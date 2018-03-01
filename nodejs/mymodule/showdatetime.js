var http = require('http');
var dt = require('./myfirstmodule.js')


// create a server object
http.createServer(function (req, res){
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write('The date and time currently is: ' + dt.myDateTime()); // write response to client
    res.end(); // end the response
}).listen(8080); // the server object listen on 8080
