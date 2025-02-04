const puppeteer = require('puppeteer');
const { startScheduler } = require('./utils/scheduler');
const { followUser } = require('./commands/follow');
const { likeHashtag } = require('./commands/like');
const { autoReply } = require('./commands/reply');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('https://www.instagram.com/accounts/login/');
  await page.type('input[name="username"]', 'your_username');
  await page.type('input[name="password"]', 'your_password');
  await page.click('button[type="submit"]');
  await page.waitForNavigation();

  startScheduler();

  likeHashtag('nature', 10);
  followUser('target_user');
  autoReply();

  await browser.close();
})();
