const puppeteer = require('puppeteer');
const devices = require('puppeteer/DeviceDescriptors');
const readline = require('readline');
const fs = require('fs');

const iPhone = devices['iPhone6'];
const BROWSER_LOC = {executablePath:'/opt/google/chrome/chrome', headless: false};
const PAGE_SIZE = {width:1280, height: 800};

// 给定url和文件名
const screenshot = async (browser, url, fname) =>{
    console.log(url);
    const page = await browser.newPage();
    
    await page.setViewport(PAGE_SIZE);
    try {
        await page.goto(url, {waitUntil: 'domcontentloaded'});
    } catch (error) {
        console.log("visit pages failed: " + error.message);
    }finally{
        await page.waitFor(1000);
        await page.screenshot({path: fname});
        await page.close();
    }    
};

const lineReading = readline.createInterface({
    // input: fs.createReadStream('phishing.txt')
    input: fs.createReadStream('/home/zgzhong/VMshare/screenshot/urls/2/2.txt')
});

let arr_url = [];

lineReading.on('line', line=>{
    arr_url.push(line);
});

lineReading.on('close', function(){
    puppeteer.launch(BROWSER_LOC).then(async browser=>{
        let promises = [];

        for(let i=0; i<arr_url.length; ++i){
            promises.push(new Promise(async (resolve, reject) => {
                await screenshot(browser, arr_url[i], "pictures/" + i + ".jpg");
                resolve();
            }));

            if( i % 20 == 19){
                await Promise.all(promises).then(async values=>{
                    promises.length = 0;
                }).catch(function (e){
                    console.log(e);
                });
            };
        };

        await Promise.all(promises).then(async values=>{
            await browser.close();            
        }).catch(function (e){
            console.log(e);
        });
    });
});
