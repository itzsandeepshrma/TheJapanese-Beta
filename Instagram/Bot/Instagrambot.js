// src/instagram/instagramBot.js
const puppeteer = require('puppeteer');
const { instagram } = require('../../config/config');
const winston = require('winston');

// Configure structured logging
const logger = winston.createLogger({
    level: 'info',
    transports: [
        new winston.transports.Console({
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.colorize(),
                winston.format.simple()
            ),
        }),
        new winston.transports.File({ filename: 'instagramBot.log' })
    ],
});

// Function to login to Instagram
const instagramLogin = async () => {
    try {
        logger.info('Starting Instagram login process...');

        // Launch Puppeteer in headless mode for production
        const browser = await puppeteer.launch({
            headless: true,  // Change to false for debugging purposes
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });

        const page = await browser.newPage();

        // Open Instagram login page
        await page.goto('https://www.instagram.com/accounts/login/');
        logger.info('Navigating to Instagram login page...');

        // Wait for login form to load
        await page.waitForSelector('input[name="username"]');
        logger.info('Login form loaded.');

        // Enter Credentials and Login
        await page.type('input[name="username"]', instagram.username);
        await page.type('input[name="password"]', instagram.password);
        await page.click('button[type="submit"]');
        logger.info('Logging in with credentials...');

        // Wait for navigation after login
        await page.waitForNavigation();
        logger.info('Logged in successfully to Instagram!');

        // Perform further actions if needed
        // Example: Go to a specific post (uncomment below)
        // await page.goto('https://www.instagram.com/p/CQeU1VeFZY6/');
        
        // Close the browser after the action is completed
        await browser.close();
        logger.info('Instagram bot completed and browser closed.');
    } catch (error) {
        logger.error(`Instagram bot encountered an error: ${error.message}`);
    }
};

// Export the Instagram login function
module.exports = instagramLogin;
