/* ********callback hell********* */
const fs = require('fs');

fs.readFile('/etc/passwd', function (err, data) {
    if (err) throw err;
    console.log("********* callback *********");
    console.log(data.toString());

});
/* ***********promise*********** */

const readFile = require('fs-readfile-promise');

readFile('/etc/passwd').then(function(data){
    console.log("********* promise *********");
    console.log(data.toString());
})
.then(function(){
    return readFile('/etc/hosts');
})
.then(function(data){
    console.log(data.toString());
})
.catch(function(err){
    console.log(err);
});