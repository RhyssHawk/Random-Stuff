
import { Setting, SettingsObject } from "../SettingsManager/SettingsManager"

let chatLine = 37554
function s(message) { ChatLib.chat(message) }
function t(message) {
	if (debugMode) {
		ChatLib.chat(`&a[Debug]&r ${message}`)
	}
	else {
		ChatLib.say(message)
	}
}
function getPlayerName(uuid) { return JSON.parse(FileLib.getUrlContent(`https://sessionserver.mojang.com/session/minecraft/profile/${uuid}`)).name }

const prefix = "&7[&8UnclaimedStuff&7]"

let config
let configDir = "./config/ChatTriggers/modules/UnclaimedStuff/config.json"
let apiKey
function loadConfig() {
	let defaultConfig = {
        "apiKey":null,
        "debugMode": false,
        "guildName":"Caped"
	}
	try {
		config = JSON.parse(FileLib.read(configDir))
	}
	catch (error) {
		s("&cInvalid config file. Rewriting with default!")
		FileLib.write(configDir, JSON.stringify(defaultConfig))
		loadConfig()
	}
	if (config == null) {
		FileLib.write(configDir, JSON.stringify(defaultConfig))
		s("Created a new config file.")
		loadConfig()
	}
	else {
		//Setting variables from the config file
		apiKey = config.apiKey
		debugMode = config.debugMode
		guildName = config.guildName

	}
}
function updateConfig() {
	FileLib.write(configDir, JSON.stringify(config))
	loadConfig()
}
register("command", key => {
	new Thread(() => {
		try {
			let keyInfo = JSON.parse(FileLib.getUrlContent(`https://api.hypixel.net/key?key=${key}`))
			if (keyInfo["success"] == true) {
				s("&aSuccessfully set your API key.")
				config.apiKey = key
				updateConfig()
			}
			else {
				s(`&cError: ${keyInfo["cause"]}.`)
				return
			}
		}
		catch (error) {
			s("&cError: Invalid API key.")
		}
	}).start()
}).setName("setkeyy")

//Commands Queue
let commandsQueue = []
register("Tick", () => { step() });
let commandsQueueLastTime = new Date().getTime()
function step() {
	if (new Date().getTime() - commandsQueueLastTime > 500) {
		commandsQueueLastTime = new Date().getTime()
		if (commandsQueue.length > 0) {
			let thing = commandsQueue.shift()
			if (thing !== "") {
				t(thing)
			}
		}
	}
}
//Lobby, Skyblock, Dungeon Hub command (SoopyAddons)
register("command", (e) => {
	new Thread(() => {
		ChatLib.say("/l")
		Thread.sleep(750)
		ChatLib.say("/play skyblock")
		Thread.sleep(750)
		ChatLib.say("/warp dungeon_hub")

		return;
	}).start()
}).setName("ldung")

let debugMode
register("command", e => {
	if (debugMode == true) {
		s("&a[Debug] Debug mode &cdisabled&a.")
		config["utility"]["debugMode"] = false
	}
	else {
		s("&a[Debug] Debug mode enabled.")
		config["utility"]["debugMode"] = true
	}
	updateConfig()
}).setName("debug")
function promoteAll() {
	let currLine = chatLine
	chatLine++
	new Message(`${prefix} &aProcessing Promotions...`).setChatLineId(currLine).chat()
	if (apiKey == null || apiKey == undefined) {
		ChatLib.clearChat(currLine)
		s(`${prefix} &cError: API key not set`)
		return
	}
	else {
		new Thread(() => {
			let promotes = []
			let guildInfo = JSON.parse(FileLib.getUrlContent(`https://api.hypixel.net/guild?key=${apiKey}&name=${guildName.replace(new RegExp(" ","g"),"%20")}`))
			for (let i=0;i<guildInfo["guild"]["members"].length;i++) {
				let playerUUID = guildInfo["guild"]["members"][i]["uuid"]
				let gexpStuff = guildInfo["guild"]["members"][i]["expHistory"]
				let memberRank = guildInfo["guild"]["members"][i]["rank"]
				let joinDate = guildInfo["guild"]["members"][i]["joined"]
				let memberTime = parseInt(new Date(new Date().getTime() - joinDate) / 1000 / 60 / 60 / 24)
				let weeklyGexp = 0
				for (day in gexpStuff) {
					weeklyGexp += gexpStuff[day]
				}
				if (weeklyGexp >= 50000) {
					if (memberRank == "Member" && memberTime >= 7) {
						promotes.push(getPlayerName(playerUUID))
					}
					else if (memberRank == "Junior" && memberTime >= 30) {
						promotes.push(getPlayerName(playerUUID))
					}
				}
			}
			ChatLib.clearChat(currLine)
			if (promotes.length == 0) {
				s("&aNo players eligable for promotions! &aAll caught up!")
				return
			}
			s(`&aPromoting &6${promotes.length} &aplayers!`)
			promotes.forEach(player => {
				commandsQueue.push(`/g promote ${player}`)
			})
		}).start()
	}
}
function demoteAll() {
    let currLine = chatLine
    chatLine++
    new Message(`${prefix} &aProcessing Demotions...`).setChatLineId(currLine).chat()
}
function kickAll() {
    let currLine = chatLine
    chatLine++
    new Message(`${prefix} &aProcessing Kicks...`).setChatLineId(currLine).chat()
}

function sum(dict) {
	let total = 0
	for (x in dict) {
		total += dict[x]
	}
	return total
}
function formatNumber(num) {
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}
let colors = {
	"BLACK":"&0",
	"DARK_BLUE":"&1",
	"DARK_GREEN":"&2",
	"DARK_AQUA":"&3",
	"DARK_RED":"&4",
	"DARK_PURPLE":"&5",
	"GOLD":"&6",
	"GRAY":"&7",
	"DARK_GRAY":"&8",
	"BLUE":"&9",
	"GREEN":"&a",
	"AQUA":"&b",
	"RED":"&c",
	"LIGHT_PURPLE":"&d",
	"YELLOW":"&e",
	"WHITE":"&f"
}
function genRank(playerInfo) {
	let rankFormats = {
		"VIP":"&a[VIP]",
		"VIP_PLUS":"&a[VIP&6+&a]",
		"MVP":"&b[MVP]",
		"MVP_PLUS":"&b[MVP&c+&b]",
		"ADMIN":"&c[ADMIN]",
		"MODERATOR":"&2[MOD]",
		"HELPER":"&9[HELPER]",
		"YOUTUBER":"&c[&fYOUTUBE&c]"
	}
	let username = playerInfo["player"]["displayname"]
	let currRank
	if ("rank" in playerInfo["player"]) { currRank = rankFormats[playerInfo["player"]["rank"]] }
	else { currRank = rankFormats[playerInfo["player"]["newPackageRank"]] }
	if (currRank !== undefined) {
		if (playerInfo["player"]["monthlyPackageRank"] == "SUPERSTAR") {
			currRank = "&6[MVP&c++&6]"
			if (playerInfo["player"]["monthlyRankColor"] == "AQUA") { currRank = currRank.replace(/&6/g, "&b")}
		}
		if ("rankPlusColor" in playerInfo["player"]) { currRank = currRank.replace(/&c\+/g, colors[playerInfo["player"]["rankPlusColor"]] + "+") }
	}
	else {
		currRank = "&7"
	}
	return `${currRank} ${username}`
}

//Better /g member command
register("command", player => {
	new Thread(() => {
        if (player == undefined) {
            s("&c/mem <player> - Shows guild info about a player")
            return
        }
		let currLine = chatLine
        chatLine++
		new Message(`&0[&2GuildStuff&0] &aGetting Guild Info for &2${player}&a...`).setChatLineId(currLine).chat()
		let uuid
		try {
			let pInfo = JSON.parse(FileLib.getUrlContent(`https://api.mojang.com/users/profiles/minecraft/${player}`))
			uuid = pInfo.id
			player = pInfo.name
		}
		catch (error) {
			ChatLib.clearChat(currLine)
			s("&cThat is not a real player!")
			return
		}
		try {
			let gInfo = JSON.parse(FileLib.getUrlContent(`https://api.hypixel.net/guild?key=${apiKey}&player=${uuid}`))
			let pInfo = JSON.parse(FileLib.getUrlContent(`https://api.hypixel.net/player?key=${apiKey}&uuid=${uuid}`))
			let members = gInfo["guild"]["members"]
			for (let i=0; i<members.length; i++) {
				if (members[i]["uuid"] == uuid) {
					let expHistory = members[i]["expHistory"]
					let weeklyGexp = formatNumber(sum(expHistory))

					let expDays = "&eDaily GEXP:"
					for (x in expHistory) {
						expDays += `\n&a${x} - &2${formatNumber(expHistory[x])}`
					}
					let memTime = parseInt((new Date().getTime() - members[i]["joined"]) / 1000 / 60 / 60 / 24)
					let memRank = members[i]["rank"]

					ChatLib.clearChat(currLine)
					let nameHover = `&aGuild Name: &e${gInfo["guild"]["name"]}`
					nameHover += `\n&aGuild Tag: ${colors[gInfo["guild"]["tagColor"]] + gInfo["guild"]["tag"]}`
					nameHover += `\n&aMembers: &6${members.length}`
					nameHover += `\n&aDescription: \n&f${gInfo["guild"]["description"]}`
					
					new Message(new TextComponent(`${genRank(pInfo)}`).setHover("show_text", nameHover), ` &8| `, new TextComponent(`&a${weeklyGexp} GEXP`).setHover("show_text", expDays), ` &8| &e${memTime} days &8| &a${memRank}`).chat()
					//s(`${genRank(pInfo)} &8| &a${weeklyGexp} GEXP &8| &e${memTime} days &8| &a${memRank}`)
					return
				}
			}
		}
		catch (error) {
			ChatLib.clearChat(currLine)
			s("&cThat player is not in a guild!")
			return
		}
	}).start()
}).setName("mem")

//Private Chat
let privateChannel = false
register("command", (...message) => {
	message = message.join(" ")
	if (message == "") {
		if (privateChannel == true) {
			s("&aYou are no longer in the &6PRIVATE &achannel")
			privateChannel = false
			return
		}
		else {
			privateChannel = true
			s("&aYou are now in the &6PRIVATE &achannel")
			return
		}
	}
	ChatLib.chat(`&3Private > &6[MVP&0++&6] UnclaimedBloom6&f: ${message}`)
}).setName("pm")
register("messageSent", (message, event) => {
	var isCommand = message.startsWith("/")
	if (isCommand == false) {
		if (privateChannel == true) {
			ChatLib.chat(`&3Private > &6[MVP&0++&6] UnclaimedBloom6&f: ${message}`)
			cancel(event)
		}
	}
})

register("chat", x => {
	World.playSound("random.orb", 1, 1)
}).setChatCriteria("[SkyBlock] ${x} is visiting Your Island!")

//Dungeon Stuff
const dungeonProgression = [50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940, 12700, 17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140, 259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640, 3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640, 23159640, 30359640, 39559640, 51559640, 66559640, 85559640, 109559640, 139559640, 177559640, 225559640, 285559640, 360559640, 453559640, 569809640]
function validPlayer(player) {
	let mojangInfo
	try {
		mojangInfo = JSON.parse(FileLib.getUrlContent(`https://api.mojang.com/users/profiles/minecraft/${player}`))
	}
	catch (error) {
		//Return false
		return false
	}
	//Return as [username, uuid]
	return [mojangInfo["name"], mojangInfo["id"]]
}
function calcCataLevel(xp) {
	if (xp >= 569809640) {
		return 50
	}
	level = 0
	for (let i = 0; i < dungeonProgression.length; i++) {
		if (dungeonProgression[i] >= xp) {
			return i
		}
	}
	return 0
}
function getProfile(key, uuid) {
	let sbInfo = JSON.parse(FileLib.getUrlContent(`https://api.hypixel.net/skyblock/profiles?key=${key}&uuid=${uuid}`))
    if (sbInfo["profiles"] == null) { return null }
	// [lastSave, profileNumber]
	let lastProfile = []
	for (profile in sbInfo["profiles"]) {
		let currLastSave = sbInfo["profiles"][profile]["members"][uuid]["last_save"]
		if (currLastSave !== undefined) {
			if (lastProfile[0] == undefined) {
				lastProfile = [currLastSave, profile]
			}
			else {
				if (currLastSave > lastProfile[0]) {
					lastProfile = [currLastSave, profile]
				}
			}
		}
	}
	return sbInfo["profiles"][lastProfile[1]]
}
function getCompletions(profile, uuid) {
	let dungeonStuff = profile["members"][uuid]["dungeons"]["dungeon_types"]["catacombs"]
	let msg = "&cCompletions:"
	for (let i=1;i<8;i++) {
		try {
			if (dungeonStuff["tier_completions"][i] == undefined) {
				msg += `\n&e${i}] &a0`
			}
			else {
				msg += `\n&e${i}] &a${dungeonStuff["tier_completions"][i]}`
			}
		}
		catch(error) {
			msg += `\n&e${i}] &a0`
		}
	}
	return msg
}
function getTimes(data) {
	let msg = ""
	for (let i=1;i<8;i++) {
		try {
			let minutes = parseInt(data[i] / 1000 / 60)
			let seconds = parseInt((data[i] - (minutes * 1000 * 60)) / 1000)
			if (seconds.toString().length == 1) { seconds = "0" + seconds }
			if (isNaN(minutes) || isNaN(seconds)) {
				msg += `\n&e${i}] &a??:??`
				continue
			}
			msg += `\n&e${i}] &a${minutes}:${seconds}`
		}
		catch(error) {
			msg += `\n&e${i}] &a??:??`
		}
	}
	return msg
}
function printDungInfo(player) {
    new Thread(() => {
        let currLine = chatLine
        chatLine++
        new Message(`${prefix} &aCalculating info for ${player}...`).setChatLineId(currLine).chat()
        //Test if the player is a real player
        let mojangInfo = validPlayer(player)
        if (mojangInfo == false) {
            ChatLib.clearChat(currLine)
            s(`${prefix} &cThat is not a real player!`)
            return
        }
        //If they're real then continue
        else {
            //Set variables
            let playerName = mojangInfo[0]
            let uuid = mojangInfo[1]
            ChatLib.editChat(currLine, new Message(`${prefix} &aGenerating rank and finding secrets...`).setChatLineId(currLine))
            let pInfo = JSON.parse(FileLib.getUrlContent(`https://api.hypixel.net/player?key=${apiKey}&uuid=${uuid}`))
            let secretsFound = pInfo.player.achievements.skyblock_treasure_hunter
            if (secretsFound == undefined) { secretsFound = 0 }
            ChatLib.editChat(currLine, new Message(`${prefix} &aGetting Skyblock profile...`).setChatLineId(currLine))
            let profile = getProfile(apiKey, uuid)
            if (profile == null) {
                ChatLib.clearChat(currLine)
                s("&cError: That player doesn't have any Skyblock profiles!")
                return
            }
            let cataLevel = calcCataLevel(profile["members"][uuid]["dungeons"]["dungeon_types"]["catacombs"]["experience"])
            let sPlusTimes = profile["members"][uuid]["dungeons"]["dungeon_types"]["catacombs"]["fastest_time_s_plus"]
            //Make the final message in chat
            ChatLib.clearChat(currLine)
            s(new Message(`&6${genRank(pInfo)} &8| &c${cataLevel} &8| &e${formatNumber(secretsFound)} &8| `, new TextComponent("&7Runs").setHover("show_text",getCompletions(profile, uuid)), " &8| ", new TextComponent("&7S+ Times").setHover("show_text",`&cS+ Times: ${getTimes(sPlusTimes)}`)))
        }
    }).start()
}
register("command", player => {
    if (player !== undefined) {
        //If player hasn't set their API key
        if (apiKey == null) {
            s(`${prefix} &cError: API Key not set!`)
            return
        }
        printDungInfo(player)
    }
    //If no arguments are given
    else {
        s("&c/ds <player> - Shows dungeon info about a player.")
    }
}).setName("ds")

register("chat", player => {
    if (player !== Player.getName() && settings.getSetting("Dungeons", "Party Finder Info") == true) {
        printDungInfo(player)
    }
}).setCriteria("Dungeon Finder > ${player} joined the dungeon group! (${*} Level ${*})")

loadConfig()
if (apiKey == null) { s(`${prefix}&c API Key not set! Set it using /setkeyy <key>!`) }

const settings = new SettingsObject(
    "UnclaimedStuff", [
        {
            "name":"Info",
            "settings":[
                new Setting.Button("&cUnclaimed's dumb module", "", () => {})
            ]
        },
        {
            "name":"Dungeons",
            "settings":[
                new Setting.Toggle("Party Finder Info", true, () => {})
            ]
        },
        {
            "name":"Guild",
            "settings":[
                new Setting.Button("&aPromote &fAll Players", "&aGo", () => { promoteAll() }),
                new Setting.Button("&cDemote &fAll Players", "&cGo", () => { demoteAll() }),
                new Setting.Button("&4Kick &fAll Players", "&4Go", () => { kickAll() })
            ]
        },
        {
            "name":"Misc",
            "settings":[
                new Setting.Button("&aOther Stuff Eventually...", "", () => {})
            ]
        }
    ]
).setCommand("us")

Setting.register(settings)