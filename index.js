// index.js
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const puppeteer = require('puppeteer');
require('dotenv').config();

// WhatsApp Bot Setup
const whatsappClient = new Client({
    authStrategy: new LocalAuth()
});

whatsappClient.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log("Scan the QR code to log in.");
});

whatsappClient.on('ready', () => {
    console.log("WhatsApp is ready!");
});

whatsappClient.on('message', msg => {
    if (msg.body === 'ping') {
        msg.reply('pong');
    }
});

whatsappClient.initialize();

// Instagram Bot Setup (Using Puppeteer)
const instagramLogin = async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    // Go to Instagram Login Page
    await page.goto('https://www.instagram.com/accounts/login/');

    // Wait for login form to load
    await page.waitForSelector('input[name="username"]');
    
    // Enter Credentials and Login
    await page.type('input[name="username"]', process.env.INSTAGRAM_USERNAME);
    await page.type('input[name="password"]', process.env.INSTAGRAM_PASSWORD);
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

instagramLogin().catch(console.error);
