'use strict';
// 模块
const fastCsv = require('fast-csv');
const puppeteer = require('puppeteer');
const events = require('events');
const md5 = require('md5');
const fs = require('fs');

// 常量
const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';


function readCsv(filepath, emitter) {
    let csv_stream = fastCsv.fromPath(filepath);
    let url_list = [];
    csv_stream.on('data', data => {
        url_list.push(data[1]);
    }).on('end', () => {
        url_list.shift();
        emitter.emit('end', url_list);
    });
};

var event = new events.EventEmitter();
readCsv('online-valid.csv', event);


async function getBrowserParams() {
    return {
        executablePath: CHROME_PATH, // uncomment if want to use chrome
        // headless: false,
        ignoreHTTPSErrors: true,
        args: [
            '--safebrowsing-disable-download-protection',
            '--safebrowsing-disable-extension-blacklist',
            '--no-sandbox',
        ]
    };
};

async function gotoUrl(page, url) {        
    try {
        console.log('Debug [ goto | ' + url + ']');
        await page.goto(url, {timeout: 10000, waitUntil: 'networkidle2'});
    } catch (err) {
        console.log('Error [ error | ' + url + ' | ' + err.message + ']');
    }
    return page;

};


event.on('end', async url_list => {
    process.on("uncaughtException", (e) => {
        console.error("Unhandled exeption:", e);
    });
    process.on("unhandledRejection", (reason, p) => {
        console.error("Unhandled Rejection at: \n\tPromise", p, "\n\treason:", reason);
    });

    
    const browser = await puppeteer.launch(await getBrowserParams());
    
    let step = 20;

    for (let idx = 0; idx < url_list.length; idx += step) {
        console.log('===============' + Date() + ' new loop' + '===============');
        let urls = url_list.slice(idx, idx + step);

        let dirname = 'picture/';
        
        const page_pool = await Promise.all(new Array(step).fill({}).map(async function(){
            let page = await browser.newPage();
                await page.authenticate({username: 'fuck', password: 'you'});
                return page;
            })
        );

        console.log('goto Url');
        const pages = await Promise.all(page_pool.map(
            async (page, idx) => {
                return new Promise(async (resolve, reject)=>{
                    const result = await gotoUrl(page, urls[idx]);
                    resolve(result);
                });
            }
        ));

        console.log('save screenshot');
        const result = await Promise.all(pages.map(
            async (page) =>{
                if (typeof page == 'undefined'){
                    return;
                }

                const picture = await page.screenshot({ type: 'jpeg' });
                const hashval = await md5(picture);
                
                await fs.writeFile(`${dirname}${hashval}.jpg`, picture, (err) => {
                    if (err) throw err;
                    console.log('Debug [ saving'  + ' | '+ page.url() + ' | ' + `${hashval}.jpg` + ']');
                });
                return `${hashval}.jpg`;
            }
        ));

        await Promise.all(page_pool.map(
            async (page)=>{
                await page.close();
            }
        ));
    };

    await browser.close();
});
