const puppeteer = require('puppeteer');



// 常量
const CHROME_PATH = '/opt/google/chrome/chrome';

async function getBrowserParams(){
    return {
        // executablePath: CHROME_PATH, // uncomment if want to use chrome
        headless:false,
        ignoreHTTPSErrors: true,
        slowMo: 300,
        args:[
            '--safebrowsing-disable-download-protection',
            '--safebrowsing-disable-extension-blacklist',
        ]
    };
};


// /* ***** 打开浏览器访问google后关闭 ****** */

async function visitGoogle() {
    let parameter = await getBrowserParams();
    const browser = await puppeteer.launch(parameter);
    const page = await browser.newPage();
    await page.goto('https://www.google.com');

    await page.close();
    await browser.close();
}

visitGoogle();

/* ********************************** */


/* ****** 重新连接浏览器访问 ****** */


async function reconnectBrowser(){
    const browser = await puppeteer.launch(await getBrowserParams());
    const browserWSEndpoint = await browser.wsEndpoint();
    const page = await browser.newPage();
    
    await page.goto('https://www.google.com');
    await console.log(browserWSEndpoint);
    await console.log("disconnect...");
    browser.disconnect();

    const browser2 = await puppeteer.connect({browserWSEndpoint});
    const page2 = await browser2.newPage();
    await page2.goto('https://www.scut.edu.cn');
    await page2.close();
    await browser2.close();
};

reconnectBrowser().catch(function(err){
    console.log(err);
});

/* **************************** */