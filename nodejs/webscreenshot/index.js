const puppeteer = require('puppeteer');
const devices = require('puppeteer/DeviceDescriptors');
const readline = require('readline');
const fs = require('fs');

const iPhone6p = devices['iPhone 6 Plus'];
// chrome 参数
const BROWSER_LOC = {executablePath:'/opt/google/chrome/chrome', args: ['disable-client-side-phishing-detection']};
const PAGE_SIZE = {width:1280, height: 800};

/**
 * 给定url和文件名, 对网页截图
 */
const screenshot = async (browser, url, fname) =>{
    const page = await browser.newPage(); 
    // 模拟iPhone6p 的页面
    // await page.emulate(iPhone6p); 
    await page.setViewport(PAGE_SIZE);
    let status = 'OK'

    try {
        console.log('DEBUG: visiting ' + url);
        await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 60000});
    } catch (err) {
        console.log(['ERROR:', err.message, url].join(' '));
        status = err.message;
    }finally{
        await page.waitFor(5000); //wait for 5 seconds
        await page.screenshot({path: fname});
        
        // 将映射关系写到文件
        let page_url = await page.url();
        let message = 'INFO: ' + [fname, status, url, page_url].join(' --> ') + '\n';
        fs.appendFile('./log.txt', message, 'utf8',err =>{
            if(err){  
                console.log('ERROR: ' + err.message);  
            }
        });  

        await page.close();
    }    
};

const lineReading = readline.createInterface({
    input: fs.createReadStream('phishing.txt')
});

let arr_url = [];

// 读取url文件到数组中
lineReading.on('line', line=>{
    arr_url.push(line);
});

// 读取完url, 调用浏览器截取网页
lineReading.on('close', function(){
    puppeteer.launch(BROWSER_LOC).then(async browser=>{
        let promises = [];

        for(let i=0; i<arr_url.length; ++i){
            promises.push(new Promise(async (resolve, reject) => {
                await screenshot(browser, arr_url[i], "pictures/" + i + ".jpg");
                resolve();
            }));
            // every 50 url
            if( i % 50 == 49){
                await Promise.all(promises).then(async values=>{
                    promises.length = 0;
                }).catch(function (err){
                    console.log('Error: ' + err.message);
                });
            };
        };

        await Promise.all(promises).then(async values=>{
            await browser.close();            
        }).catch(function (err){
            console.log('Error: ' + err.message);
        });
    });
});
