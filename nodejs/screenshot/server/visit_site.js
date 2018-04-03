const puppeteer = require('puppeteer');
const md5 = require('md5');
const fs = require('fs');

const PAGE_SIZE = {width:1280, height: 800};


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


(async () => {
    const browser = await puppeteer.launch(await getBrowserParams());
    const page = await browser.newPage();

    page.on('response', response=>{
        console.log('on response');
        console.log(response.ok);
    });

    page.on('requestfinished', req=>{
        console.log('request finished');
    });

    page.on('request', req=>{
        console.log('send request');
    });
    
    page.on('requestfailed', req=>{
        console.log('request failed');
    });

    await page.setViewport(PAGE_SIZE);
    await page.authenticate({username: 'fuck', password: 'you'});

    try {
        await page.goto('http://quatangluuniemhue.com/ACH-FORM/OTL-7372377976509/', {timeout: 30000});
    } catch (err) {
        console.log(err.message);        
        if (!err.message.toLowerCase().includes('timeout')){
            await page.close();
            await browser.close();
            return;
        }
    }
    await page.waitFor(500);
    console.log('try to screenshot');
    const picture = await page.screenshot({ type: 'jpeg' });
    await page.close();


    let hashval = await md5(picture);
    await fs.writeFile(`${hashval}.jpg`, picture, (err) => {
        if (err) throw err;
        console.log(`The file "${hashval}.jpg" has been saved!`);
    });

    await browser.close();    
})();
