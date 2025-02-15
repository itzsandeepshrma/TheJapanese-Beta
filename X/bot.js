require("dotenv").config();
const { TwitterApi } = require("twitter-api-v2");

const client = new TwitterApi({
    appKey: process.env.TWITTER_API_KEY,
    appSecret: process.env.TWITTER_API_SECRET,
    accessToken: process.env.TWITTER_ACCESS_TOKEN,
    accessSecret: process.env.TWITTER_ACCESS_SECRET,
});

async function tweetMessage() {
    try {
        const tweet = await client.v2.tweet("Hello! Welcome to Team Japanese.");
        console.log("Tweet sent successfully:", tweet);
    } catch (error) {
        console.error("Error sending tweet:", error);
    }
}

tweetMessage();
