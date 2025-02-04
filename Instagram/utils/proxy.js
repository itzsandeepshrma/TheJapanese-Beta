const puppeteer = require('puppeteer');
const { PROXY_URL } = require('../config');

async function getBrowserWithProxy() {
  const browser = await puppeteer.launch({
    headless: true,
    args: [`--proxy-server=${PROXY_URL}`],
  });
  return browser;
}

module.exports = { getBrowserWithProxy };
