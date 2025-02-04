const puppeteer = require('puppeteer');
const { INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD } = require('../config');
const { getBrowserWithProxy } = require('../utils/proxy');

async function followUser(username) {
  const browser = await getBrowserWithProxy();
  const page = await browser.newPage();

  await page.goto('https://www.instagram.com/accounts/login/');
  await page.type('input[name="username"]', INSTAGRAM_USERNAME);
  await page.type('input[name="password"]', INSTAGRAM_PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForNavigation();

  await page.goto(`https://www.instagram.com/${username}/`);
  await page.waitForSelector('button');

  const followButton = await page.$('button');
  const followText = await page.evaluate(button => button.textContent, followButton);

  if (followText === 'Follow') {
    await followButton.click();
    console.log(`Successfully followed ${username}`);
  } else {
    console.log(`Already following ${username}`);
  }

  await browser.close();
}

module.exports = { followUser };
