console.log("Beep Beep !!")

const Discord = require('discord.js');
const client = new Discord.Client();
targt = getRandomInt(1000);



client.login("TOKEN");

client.on('ready', readyDiscord);
client.on('message', gotMessage);

function readyDiscord() {
	console.log(`logged in! ${client.user.tag}!`);
}

function gotMessage(msg) {
	if (msg.channel.id === 'YOUR_CHANNEL_ID') {
		if (msg.content === 'pony') {
			msg.reply('Fluttershy')
		}
		x = parseInt(msg.content);
		if (x !== NaN) {
			if (x > targt)
				msg.reply('Lower!');
			if (x < targt)
				msg.reply('Higher!');
			if (x === targt) {
				msg.reply('Exactly, generating a new number..');
				targt = getRandomInt(1000);
				msg.reply('new number has been generated!');
			}
		}
	}
}

function getRandomInt(max) {
	return Math.floor(Math.random() * Math.floor(max));
}