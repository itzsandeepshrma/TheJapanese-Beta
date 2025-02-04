const puppeteer = require('puppeteer');
const { secureLogin } = require('../utils/auth');
const { getBrowserWithProxy } = require('../utils/proxy');
const fs = require('fs');
const path = require('path');

async function postPhoto(photoPath, caption) {
  if (!fs.existsSync(photoPath)) {
    console.log("Photo not found");
    return;
  }

  const browser = await getBrowserWithProxy();
  const page = await browser.newPage();

  await secureLogin(page);

  await page.goto('https://www.instagram.com/create/style/');
  const fileInput = await page.$('input[type="file"]');
  await fileInput.uploadFile(photoPath);

  await page.waitForSelector('textarea');
  await page.type('textarea', caption);
  await page.click('button[type="submit"]');
  console.log('Photo posted successfully');
  
  await browser.close();
}

module.exports = { postPhoto };
