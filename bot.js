console.log("Beep Beep !!")

const Discord = require('discord.js');
const client = new Discord.Client();

targt = getRandomInt(1000);
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

const ponies = [
	'Fluttershy',
	'Rainbow Dash',
	'Pinkie Pie',
	'Twighlight Sparkle',
	'Rarity',
	'Apple Jack'
];
const when_answers = [
	'in about 10 days',
	'tomorrow',
	'in 60 seconds',
	'in a week',
	'you just need to wait for another year',
	'you just need to wait, it will happen',
	'wait for another, like, umm..., 1000 years or so',
	'on the first day oh the next month',
	'already, you should just check',
	'never, it will never happen',
	'when you take your next sip of water',
	'3... 2... 1... yep)'
];

client.login(process.env.BOT_TOKEN);
tags='';
client.on('ready', readyDiscord);
client.on('message', gotMessage);

function readyDiscord() {
	console.log(`logged in! ${client.user.tag}!`);
}

function gotMessage(msg) {
	try {
		if (msg.channel.id === '778238197049065512' || msg.channel.id === '781662768130424836') {
			if (msg.content.toLowerCase() == '!nuke-this-channel') {
				if (msg.member.roles.cache.has('783397190327468044') || msg.member.roles.cache.has('721018563179053066')) {
					async function wipe() {
						var msg_size = 100;
						while (msg_size == 100) {
							await msg.channel.bulkDelete(100)
								.then(messages => msg_size = messages.size)
								.catch(console.error);
						}
						msg.channel.send(`<@${msg.author.id}>\n> ${msg.content}`, { files: ['http://www.quickmeme.com/img/cf/cfe8938e72eb94d41bbbe99acad77a50cb08a95e164c2b7163d50877e0f86441.jpg'] })
					}
					tags='';
					wipe()
				}
				else {
					msg.channel.send('not enough permissions');
				}
			}

			if (msg.content.toLowerCase() == '!nuke-all') {
				if (msg.member.roles.cache.has('783397190327468044') || msg.member.roles.cache.has('721018563179053066')) {
					async function wipe() {
						var msg_size = 100;
						console.log("started")
						while (msg_size == 100) {
							await msg.channel.messages.fetch({ limit: 100 }).then(messages => {
								msg_size = messages.size;
								messages.forEach(message => message.delete())
							}).catch(console.error);
						}
						msg.channel.send(`<@${msg.author.id}>\n> ${msg.content}`, { files: ['http://www.quickmeme.com/img/cf/cfe8938e72eb94d41bbbe99acad77a50cb08a95e164c2b7163d50877e0f86441.jpg'] })
					}
					tags='';
					wipe()
				}
				else {
					msg.channel.send('not enough permissions');
				}
			}
			if (msg.content === '!Pony') {
				msg.channel.send(ponies[Math.floor(Math.random() * ponies.length)]);
			}
			if (msg.content.substring(0, 5) === '!when') {
				msg.channel.send(when_answers[Math.floor(Math.random() * when_answers.length)]);
			}
			if (msg.content.substring(0, 5) === '!tags') {
				return_tag(msg);
			}
			if (msg.content.substring(0, 5) === '!loli') {
				try {
					tag = "";
					page = "";
					count = 1;
					link = 'https://lolibooru.moe/';
					if (msg.content.search(" ") !== -1) {
						tag = "+" + msg.content.split(" ")[1];
						if (tag === "+-") tag = "";
						if (msg.content.split(" ").length > 2)
							page = "&page=" + msg.content.split(" ")[2];
						if (page === "-") page = "&page=1";
						if (msg.content.split(" ")[3] == "*") {
							count = 40;
						}
					}

					response = httpGetAsyncNew(link + "post?tags=-3dcg+-video+-webm+-gif" + tag + page, GetLoliN, msg, count);
				}
				catch (error) {
					msg.channel.send("Too huge for mee, try another request ");
				}
			}

			if (msg.content.substring(0, 5) === '!pony') {
				tag = "";
				page = "1";
				count = 1;
				link = 'https://derpibooru.org/';
				if (msg.content.search(" ") !== -1) {
					tag = msg.content.split(" ")[1];
					if (tag === "-") tag = "";
					if (msg.content.split(" ").length > 2)
						page = msg.content.split(" ")[2];
					if (page === "-") page = "1";
					if (msg.content.split(" ")[3] === "*") {
						count = 15;
					}
				}
				if (tag !== "") {
					response = httpGetAsyncNew(link + "search?page=" + page + "&q=" + tag, getPony, msg, count);
				}
				else {
					response = httpGetAsyncNew(link + "images?page=" + page, getPony, msg, count);
				}
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
	catch (error) {
		msg.channel.send("Something went incredibly wrong... sorry, at least I am alive and can do more requests ");
    }
}

function getRandomInt(max) {
	return Math.floor(Math.random() * Math.floor(max));
}


function httpGetAsyncNew(theUrl, callback, msg, c) {
	try {
		var xmlHttp = new XMLHttpRequest();
		xmlHttp.onreadystatechange = function () {
			if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
				callback(xmlHttp.responseText, msg, c);
		}
		xmlHttp.open("GET", theUrl, true); // true for asynchronous 
		xmlHttp.send(null);
	}
	catch (error) {
		msg.channel.send("Something wrong with GET requests");
    }
}

function GetLoliN(text, msg,count) {
	if (count === 1)
		id = 1 + getRandomInt(40);
	else
		id = 1;
	if (msg.content.search(" ") !== -1)
		if (msg.content.split(" ").length == 4)
			if (!isNaN(parseInt(msg.content.split(" ")[3])))
				id = parseInt(msg.content.split(" ")[3])

	for (i = 0; i < count; i++) {
		try {
			response = text.split('<ul id="post-list-posts">')[1].split('<div id="paginator">')[0].split('<a class="directlink')[id + i];		
			chunk = response.split('img" href="')[1].split('"')[0];

			if (response.search("largeimg") !== -1) {
				responses = chunk.replace(/ /g, '%20').replace('image', 'sample').split('%20');
				chunk = responses[0] + '%20' + responses[1] + '%20' + 'sample.jpg';
			}
			

			console.log(chunk);
			const attach = new Discord.MessageAttachment(chunk, "there_is_no_name." + chunk.substring(chunk.length - 3, chunk.length));
			msg.channel.send(attach);
		} catch (error) {
			msg.channel.send("I couldn't find it :(( maybe try again ");
			return;
		}
	}
}


function getPony(text, msg, count) {
	if (count === 1)
		id = 1 + getRandomInt(15);
	else
		id = 1;
	if (msg.content.search(" ") !== -1)
		if (msg.content.split(" ").length == 4)
			if (!isNaN(parseInt(msg.content.split(" ")[3])))
				id = parseInt(msg.content.split(" ")[3])
	for (i = 0; i < count; i++) {
		try {
			response = text.split('data-uris="{&quot;full&quot;:&quot;')[id + i];
			tags = response.split('Tagged:')[1].split('">')[0];
			response = response.split("&quot;")[0];
			const attach = new Discord.MessageAttachment(response.replace(/ /g, '%20'), "there_is_no_name." + response.substring(response.length - 3, response.length));
			msg.channel.send(attach);
			//msg.channel.send(response.replace(/ /g, '%20'));
		} catch (error) {
			msg.channel.send("I couldn't find it :(( maybe try again ");
			return;
		}
	}
}

function return_tag(msg)
{
	msg.channel.send("tags:"+tags);
}
