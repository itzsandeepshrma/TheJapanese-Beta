require("dotenv").config();
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");

const client = new Client({
    authStrategy: new LocalAuth(),
});

client.on("qr", (qr) => {
    console.log("Scan this QR code to log in:");
    qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
    console.log("WhatsApp bot is ready!");
});

client.on("message", async (message) => {
    if (message.body.toLowerCase() === "hello") {
        message.reply("Hello! Welcome to Team Japanese.");
    }
});

client.initialize();
