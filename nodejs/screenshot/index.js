'use strict';
// 模块
const fastCsv = require('fast-csv');
const puppeteer = require('puppeteer');
const events = require('events');
const md5 = require('md5');
const fs = require('fs');

// 常量
const CHROME_PATH = '/opt/google/chrome/chrome';
const PAGE_SIZE = { width: 1280, height: 800 };


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
        // executablePath: CHROME_PATH, // uncomment if want to use chrome
        headless: false,
        ignoreHTTPSErrors: true,
        slowMo: 100,
        args: [
            '--safebrowsing-disable-download-protection',
            '--safebrowsing-disable-extension-blacklist',
        ]
    };
};

async function screenshot(browser, url, dirname) {
    dirname = await dirname || './';
    const page = await browser.newPage();
    await page.setViewport(PAGE_SIZE);
    let response
    try {
        response = await page.goto(url);
    } catch (err) {
        console.log(err.message);
        if (!err.message.toLowerCase().includes('timeout')) {
            await page.close();
            return `${url}: ${err.message}`;
        }
    }
    if (response && !response.ok()) {
        await page.close();
        return `${url}: Not OK`;
    }

    await page.waitFor(5000);
    const picture = await page.screenshot({ type: 'jpeg' });
    await page.close();

    const hashval = await md5(picture);
    await fs.writeFile(`${dirname}${hashval}.jpg`, picture, (err) => {
        if (err) throw err;
        console.log(`OK: pic: ${hashval}.jpg | url: ${url}`);
    });
    return `${url}: ${hashval}.jpg`;
};


event.on('end', async url_list => {
    process.on("uncaughtException", (e) => {
        console.error("Unhandled exeption:", e);
    });
    process.on("unhandledRejection", (reason, p) => {
        console.error("Unhandled Rejection at: \n\tPromise", p, "\n\treason:", reason);
    });

    const browser = await puppeteer.launch(await getBrowserParams());

    let step = 10;
    for (let idx = 0; idx < url_list.length; idx += step) {
        let urls = url_list.slice(idx, idx + step);


        let promises = urls.map(function (url) {
            return new Promise(async function (resolve, reject) {
                const result = await screenshot(browser, url, 'picture/');
                resolve(result);
            });
        });

        const result = await Promise.all(promises).catch((err) => {
            console.log(err.message);
        });
        console.log(result);

    };
    await browser.close();
});
