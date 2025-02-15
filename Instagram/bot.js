
require("dotenv").config();
const { IgApiClient } = require("instagram-private-api");

const ig = new IgApiClient();

async function startBot() {
    ig.state.generateDevice(process.env.IG_USERNAME);
    await ig.account.login(process.env.IG_USERNAME, process.env.IG_PASSWORD);
    console.log("Instagram bot is ready!");

    // Example: Send a message
    const userId = await ig.user.getIdByUsername("example_username");
    await ig.directThread([userId]).broadcastText("Hello! Welcome to Team Japanese.");
}

startBot();
