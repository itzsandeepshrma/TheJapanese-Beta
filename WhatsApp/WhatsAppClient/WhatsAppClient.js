// src/whatsapp/whatsappClient.js
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const { whatsapp } = require('../../config/config');
const winston = require('winston');  // Structured logging
const fs = require('fs');

// Configure logging
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
        new winston.transports.File({ filename: 'whatsappClient.log' })
    ],
});

// Ensure the session directory exists for LocalAuth
const sessionDir = `./sessions/${whatsapp.sessionName}`;
if (!fs.existsSync(sessionDir)) {
    fs.mkdirSync(sessionDir, { recursive: true });
}

// Initialize WhatsApp Client
const whatsappClient = new Client({
    authStrategy: new LocalAuth({
        clientId: whatsapp.sessionName
    }),
    puppeteer: {
        headless: true, // Runs in the background
        args: ['--no-sandbox', '--disable-setuid-sandbox'] // For deployment environments like Docker
    }
});

// Event when QR code is generated
whatsappClient.on('qr', (qr) => {
    // We don't want to log the QR in production, log a message instead
    if (process.env.NODE_ENV !== 'production') {
        qrcode.generate(qr, { small: true });
        logger.info('Scan the QR code to log in.');
    } else {
        logger.info('QR Code generated. Scan to log in.');
    }
});

// Event when WhatsApp client is ready
whatsappClient.on('ready', () => {
    logger.info('WhatsApp is ready!');
});

// Event when a new message is received
whatsappClient.on('message', (msg) => {
    try {
        if (msg.body.toLowerCase() === 'ping') {
            msg.reply('pong');
        }

        // Handle any other message interactions here
        logger.info(`Message received: ${msg.body}`);
    } catch (error) {
        logger.error(`Error processing message: ${error.message}`);
    }
});

// Handle errors
whatsappClient.on('error', (error) => {
    logger.error(`WhatsApp Client encountered an error: ${error.message}`);
});

// Graceful shutdown
process.on('SIGINT', async () => {
    logger.info('Gracefully shutting down WhatsApp Client...');
    await whatsappClient.logout();
    process.exit(0);
});

module.exports = whatsappClient;
