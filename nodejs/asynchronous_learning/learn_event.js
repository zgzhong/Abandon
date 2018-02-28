const EventEmitter = require('events').EventEmitter;

let event = new EventEmitter();

event.on('some_event', function(){
    console.log('事件触发');
});

setTimeout(function(){
    event.emit('some_event');
}, 1000);