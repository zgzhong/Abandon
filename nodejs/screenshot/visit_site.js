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
    await page.setViewport(PAGE_SIZE);

    try {
        // await page.goto('http://adin.lavanderia-llc.com/04/index.php', {timeout: 30000});
        await page.goto('http://93.182.172.8/css1/dz1/lopss/zz/SulprULwZ1/ll.php', {timeout: 30000});        
    } catch (err) {
        console.log(err.message);        
        if (!err.message.toLowerCase().includes('timeout')){
            await page.close();
            await browser.close();
            return;
        }
    }
    await page.waitFor(3000);
    const picture = await page.screenshot({ type: 'jpeg' });
    await page.close();


    let hashval = await md5(picture);
    await fs.writeFile(`${hashval}.jpg`, picture, (err) => {
        if (err) throw err;
        console.log(`The file "${hashval}.jpg" has been saved!`);
    });

    await browser.close();    
})();