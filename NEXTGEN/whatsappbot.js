const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const { whatsapp } = require('../config/config');
const fs = require('fs');
const path = require('path');

// Setup logging
const logFile = path.join(__dirname, 'bot.log');
const logStream = fs.createWriteStream(logFile, { flags: 'a' });
const log = (message) => {
    const timestamp = new Date().toISOString();
    logStream.write(`${timestamp} - ${message}\n`);
};

// Initialize WhatsApp Client
const client = new Client({
    authStrategy: new LocalAuth({
        clientId: whatsapp.sessionName || 'whatsapp-session',
    }),
});

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    log("QR code generated. Please scan it.");
});

client.on('ready', () => {
    log("WhatsApp is ready!");
});

client.on('message', (msg) => {
    if (msg.body === 'ping') {
        msg.reply('pong');
    }
});

client.on('auth_failure', (msg) => {
    log("Authentication failure, please check credentials.");
});

client.on('disconnected', (reason) => {
    log(`WhatsApp client disconnected: ${reason}`);
});

client.initialize();
