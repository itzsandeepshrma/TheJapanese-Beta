// src/instagram/instagramBot.js
const puppeteer = require('puppeteer');
const { instagram } = require('../../config/config');

const instagramLogin = async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    // Go to Instagram Login Page
    await page.goto('https://www.instagram.com/accounts/login/');

    // Wait for login form to load
    await page.waitForSelector('input[name="username"]');
    
    // Enter Credentials and Login
    await page.type('input[name="username"]', instagram.username);
    await page.type('input[name="password"]', instagram.password);
    await page.click('button[type="submit"]');

    // Wait for the page to load after login
    await page.waitForNavigation();
    console.log('Logged in to Instagram!');

    // Optionally: Like a post or perform other actions on Instagram
    // Example: Go to a specific post
    // await page.goto('https://www.instagram.com/p/CQeU1VeFZY6/');
    
    // Close browser after action
    await browser.close();
};

module.exports = instagramLogin;
