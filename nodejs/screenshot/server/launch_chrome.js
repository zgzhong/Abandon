/* use child process to launch */
const execFile = require('child_process').execFile

function launchHeadlessChrome(url, callback){
    const CHROME = 'node_modules/puppeteer/.local-chromium/linux-536395/chrome-linux/chrome';
    execFile(CHROME, ['--headless', '--disable-gpu', '--remote-debugging-port=9222', url], callback);
}

/* ****use chrome-launcher*** */
const chromeLauncher = require('chrome-launcher');

function launchChrome(headless=true) {
    return chromeLauncher.launch({
        port: 9222,
        chromePath: 'node_modules/puppeteer/.local-chromium/linux-536395/chrome-linux/chrome',
        chromeFlags: [
            '--disable-gpu',
            headless? '--headless': ''
        ],
        logLevel: 'debug',
        startingUrl: 'http://localhost:9222'
    });
}


/* **********call the function*********** */

// launchHeadlessChrome('https://www.chromestatus.com', (err, stdout, stderr)=>{
//     console.log(stderr);
// });

launchChrome(false).then(chrome =>{
    console.log(`Chrome debuggable on port: ${chrome.port}`);
    // chrome.kill();
})