const http = require('http');
const url = require('url');
const puppeteer = require('puppeteer');
const md5 = require('md5');
const fs = require('fs');
const log4js = require('log4js');

const logger = log4js.getLogger();
logger.level = 'debug';


// launch browser
async function getBrowser() {
    const CHROME_PATH = '/opt/google/chrome/chrome';
    const parameter = {
        // executablePath: CHROME_PATH, // uncomment if want to use chrome
        //headless: false,
        ignoreHTTPSErrors: true,
        args: [
            '--safebrowsing-disable-download-protection',
            '--safebrowsing-disable-extension-blacklist',
            '--no-sandbox'
        ]
    };

    const browser = await puppeteer.launch(parameter);
    return browser;
};


// create http server
getBrowser().then(async browser => {
    logger.info("Browser launched");

    // use query string to atain the url
    http.createServer(async (request, response) => {
        let req_url = url.parse(request.url, true);
        let query_string = req_url.query;

        logger.info('incomimg  | ' + query_string.url);
        
        let result;

        try {
            result = await extract_site_feature(browser, query_string.url);
        }catch(err){
            logger.warn(`Error happened: on ${query_string.url}`, err.reason, err.stack);
            result = {
                status: 'error',
                reason: err.reason,
                trace: err.stack,
                origin_url: query_string.url,
            };
            response.writeHead(200, {'Content-Type': 'application/json'});
            response.write(JSON.stringify(result));
            response.end();
            return;
        }

        response.writeHead(200, { 'Content-Type': 'application/json' });
        response.write(JSON.stringify(result));
        response.end();
    }).listen(8080);

    logger.info("Http server listening at: localhost:8080");
});


async function extract_site_feature(browser, url) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    await page.authenticate({ username: 'username', password: 'password' });  // 跳过认证

    const time_beg = new Date();
    logger.debug(`Begin visit: ${url}`)

    let response;
    try {
        response = await page.goto(url, { timeout: 60000, waitUntil: 'networkidle0' });
    } catch (err) {
        logger.debug(`${err.message}: ${present_url(url)}`);
        await page.close();
        return {
            status: 'failed',
            reason: err.message,
            origin_url: url
        };
    }

    // get time spent
    const time_spent = new Date() - time_beg;
    logger.debug(`End visit: ${url}`);
    logger.debug(`Time spent: ${time_spent} ms.`);

    if (response == undefined){
        logger.debug(`Navigate to about:blank => ${present_url(url)}`);
        logger.debug('close page');
        await page.close();
        return {
            status: 'failed',
            reaseon: 'navigate to about:blank',
            origin_url: url,
        };
    }
    
    // get page status
    logger.debug('get page status');
    const status_code = await response.status();
    const landed_url = await response.url();

    // get ca information
    logger.debug('get ca information');
    const security_conn = await response.securityDetails();
    let ca_issuer = null;
    let ca_subject = null;
    let ca_valid_from = null;
    let ca_valid_to = null;
    if (security_conn != null) {
        ca_issuer = security_conn.issuer();
        ca_subject = security_conn.subjectName();
        ca_valid_from = security_conn.validFrom();
        ca_valid_to = security_conn.validTo();
    }

    // get icon link
    logger.debug('get icon href');
    let icon_href = null;
    if (await page.$('link[rel*="icon"]')){
        const icon_href = await page.$eval('link[rel*="icon"]', icon=>icon.href);
        logger.debug('icon url', icon_href);
    }else{
        logger.debug('Can not find favicon in the page');
    }

    // get page content
    logger.debug('get page html');
    const html = await response.text();

    // screen shot
    logger.debug('take screenshot');
    let picture = await page.screenshot({ type: 'jpeg' });
    
    // store information
    logger.debug('saving screenshot and html');
    let pic_md5 = await md5(picture);
    let url_md5 = await md5(url);
    let pic_name = `${pic_md5}_${url_md5}.jpg`;
    let html_name = `${pic_md5}_${url_md5}.html`;
    let pic_path = `picture/${pic_name}`;
    let html_path = `html/${html_name}`

    fs.writeFile(pic_path, picture, (err) => {
        if (err) throw err;
        logger.info(`Saved ${present_url(url)} to => ${pic_path}`);
    });

    fs.writeFile(html_path, html, (err)=>{
        if (err) throw err;
        logger.info(`Saved ${present_url(url)} to => ${html_path}}`);
    });

    logger.debug('close page');
    await page.close();
    return {
        'status': 'success',
        'origin_url': url,
        'landed_url': landed_url,
        'status_code': status_code,
        'time_spent': time_spent,
        'ca_issuer': ca_issuer,
        'ca_subject': ca_subject,
        'ca_valid_from': ca_valid_from,
        'ca_valid_to': ca_valid_to,
        'icon_href': icon_href,
        'fpath': pic_path,
        'html': html_path,
    };
};

function present_url(url) {
    if (url.length < 100){
        return url.padEnd(100, ' ');
    }
    return url.slice(0, 97).padEnd(100, '.');
}
