const puppeteer = require('puppeteer');
const { secureLogin } = require('../utils/auth');
const { getBrowserWithProxy } = require('../utils/proxy');

async function unfollowUser(username) {
  const browser = await getBrowserWithProxy();
  const page = await browser.newPage();

  await secureLogin(page);

  await page.goto(`https://www.instagram.com/${username}/`);
  await page.waitForSelector('button');
  
  const followButton = await page.$('button');
  const followText = await page.evaluate(button => button.textContent, followButton);
  
  if (followText === 'Following') {
    await followButton.click();
    await page.waitForSelector('button');
    await page.click('button');
    console.log(`Successfully unfollowed ${username}`);
  } else {
    console.log(`You are not following ${username}`);
  }

  await browser.close();
}

module.exports = { unfollowUser };
