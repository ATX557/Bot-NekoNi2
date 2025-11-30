const fs = require("fs");
const { Client, GatewayIntentBits, Partials, Collection } = require("discord.js");
const { token, prefix } = require("./config.json");

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers
    ]
});

client.commands = new Collection();
client.slash = new Collection();
client.prefix = prefix;

// Load commands
const folders = fs.readdirSync("./commands");
for (const folder of folders) {
    const files = fs.readdirSync(`./commands/${folder}`).filter(f => f.endsWith(".js"));
    for (const file of files) {
        const cmd = require(`./commands/${folder}/${file}`);
        client.commands.set(cmd.name, cmd);
        if (cmd.slash) client.slash.set(cmd.slash.data.name, cmd.slash);
    }
}

// Load events
const eventFiles = fs.readdirSync("./events");
for (const file of eventFiles) {
    const event = require(`./events/${file}`);
    client.on(event.name, (...args) => event.run(client, ...args));
}

client.login(token);
