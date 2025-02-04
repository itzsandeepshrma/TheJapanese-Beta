const puppeteer = require('puppeteer');
const { secureLogin } = require('../utils/auth');
const { getBrowserWithProxy } = require('../utils/proxy');
const fs = require('fs');
const path = require('path');

async function uploadStory(photoPath) {
  if (!fs.existsSync(photoPath)) {
    console.log("Photo not found");
    return;
  }

  const browser = await getBrowserWithProxy();
  const page = await browser.newPage();

  await secureLogin(page);

  await page.goto('https://www.instagram.com/create/story/');
  const fileInput = await page.$('input[type="file"]');
  await fileInput.uploadFile(photoPath);

  await page.waitForSelector('button[type="submit"]');
  await page.click('button[type="submit"]');
  console.log('Story uploaded successfully');
  
  await browser.close();
}

module.exports = { uploadStory };
