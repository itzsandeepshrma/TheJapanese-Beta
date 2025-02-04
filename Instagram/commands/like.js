const puppeteer = require('puppeteer');
const { INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD } = require('../config');
const { getBrowserWithProxy } = require('../utils/proxy');

async function likeHashtag(hashtag, amount = 10) {
  const browser = await getBrowserWithProxy();
  const page = await browser.newPage();

  await page.goto('https://www.instagram.com/accounts/login/');
  await page.type('input[name="username"]', INSTAGRAM_USERNAME);
  await page.type('input[name="password"]', INSTAGRAM_PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForNavigation();

  await page.goto(`https://www.instagram.com/explore/tags/${hashtag}/`);

  let liked = 0;
  while (liked < amount) {
    await page.waitForSelector('article');
    const posts = await page.$$('article > div:nth-child(1) img');
    if (posts.length > 0) {
      const post = posts[liked % posts.length];
      await post.click();
      await page.waitForSelector('svg[aria-label="Like"]');
      await page.click('svg[aria-label="Like"]');
      liked++;
      console.log(`Liked ${liked} post(s)`);
    }
    await page.goBack();
  }

  await browser.close();
}

module.exports = { likeHashtag };
