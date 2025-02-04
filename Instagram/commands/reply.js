const puppeteer = require('puppeteer');
const { INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD } = require('../config');
const { getBrowserWithProxy } = require('../utils/proxy');

async function autoReply() {
  const browser = await getBrowserWithProxy();
  const page = await browser.newPage();

  await page.goto('https://www.instagram.com/accounts/login/');
  await page.type('input[name="username"]', INSTAGRAM_USERNAME);
  await page.type('input[name="password"]', INSTAGRAM_PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForNavigation();

  await page.goto('https://www.instagram.com/direct/inbox/');

  const messages = await page.$$('div[role="dialog"]');
  for (let msg of messages) {
    const text = await msg.evaluate(el => el.innerText);
    if (text.includes('Hello')) {
      console.log('Replying to message');
      await msg.click();
      await page.type('textarea[placeholder="Message..."]', 'Thanks for reaching out!');
      await page.keyboard.press('Enter');
    }
  }

  await browser.close();
}

module.exports = { autoReply };
