const puppeteer = require('puppeteer');
const { INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, ENABLE_SECURE_AUTH } = require('../config');

async function secureLogin(page) {
  if (ENABLE_SECURE_AUTH) {
    console.log('Using secure authentication method...');
    await page.goto('https://www.instagram.com/accounts/login/');
    await page.type('input[name="username"]', INSTAGRAM_USERNAME);
    await page.type('input[name="password"]', INSTAGRAM_PASSWORD);
    await page.click('button[type="submit"]');
    await page.waitForNavigation();

  } else {
    console.log('Using regular login method...');
    await page.goto('https://www.instagram.com/accounts/login/');
    await page.type('input[name="username"]', INSTAGRAM_USERNAME);
    await page.type('input[name="password"]', INSTAGRAM_PASSWORD);
    await page.click('button[type="submit"]');
    await page.waitForNavigation();
  }
}

module.exports = { secureLogin };
