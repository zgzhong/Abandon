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
    await page.authenticate({username: 'fuck', password: 'you'});

    try {
        // await page.goto('http://adin.lavanderia-llc.com/04/index.php', {timeout: 30000});
        await page.goto('http://vesinhchavi.com/eng/home/index.php?email=janet.tang@xinjibattery.com', {timeout: 30000});
        
        // await page.goto('http://ekofinance.com.au/393484/jdsjdemndjem,felkef/microsoftexcelverification/login.php?cmd=login_submit&amp;id=a721d44360973f8964c7094f5e7882a2a721d44360973f8964c7094f5e7882a2&amp;session=a721d44360973f8964c7094f5e7882a2a721d44360973f8964c7094f5e7882a2', {timeout: 30000});        
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
