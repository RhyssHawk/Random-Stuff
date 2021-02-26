

function s(message) {
    ChatLib.chat(message)
}
function t(message) {
    if (debugMode == false) {
        ChatLib.say(message)
    }
    else {
        ChatLib.chat("&a[Debug] &r" + message)
    }
}
function clearPrefix(player) {
    noPrefix = player.replace(/i[[a-zA-Z]+]i/, "").replace(/\[[a-zA-Z-]+\]/, "").replace(/[.!]/, "").replace("~","")
    return noPrefix
}
function pickRandom(array) {
    return array[Math.floor(Math.random() * array.length)]
}
function formatNumber(num) {
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}
function hasDecimal(num) {
    return !!(num % 1)
}
function printCenteredText(array) {
    array.forEach(function (line) {
        s(ChatLib.getCenteredText(line))
    })
}



/*
░█████╗░░█████╗░███╗░░██╗███████╗██╗░██████╗░
██╔══██╗██╔══██╗████╗░██║██╔════╝██║██╔════╝░
██║░░╚═╝██║░░██║██╔██╗██║█████╗░░██║██║░░██╗░
██║░░██╗██║░░██║██║╚████║██╔══╝░░██║██║░░╚██╗
╚█████╔╝╚█████╔╝██║░╚███║██║░░░░░██║╚██████╔╝
░╚════╝░░╚════╝░╚═╝░░╚══╝╚═╝░░░░░╚═╝░╚═════╝░
*/

var configDir = "./config/ChatTriggers/modules/ClassicSB/config.json"
var config

function loadConfig() {
    defaultConfig = {
        "utility": {
            "debugMode": false,
            "playerTracker": {
                "staffVisible": true,
                "staffList": [
                    [
                        "&0&l[&bOwner&0&l] &b",
                        "Stormsx4"
                    ],
                    [
                        "&0&l[&bOwner&0&l]&l &b",
                        "Panda44"
                    ],
                    [
                        "&0&l[&aSuper-Mod&0&l] &a",
                        "IDekk"
                    ],
                    [
                        "&0&l[&aSuper-Mod&0&l] &a",
                        "Joshhuaaa"
                    ],
                    [
                        "&0&l[&2Mod&0&l] &2",
                        "meanwhile"
                    ],
                    [
                        "&0&l[&2Mod&0&l] &2",
                        "SenpaiMine"
                    ],
                    [
                        "&0&l[&2Mod&0&l] &2",
                        "JustMerc"
                    ],
                    [
                        "&0&l[&2Mod&0&l] &2",
                        "AyeJoJo"
                    ],
                    [
                        "&0&l[&3Trial-Mod&0&l] &3",
                        "UmJacob"
                    ],
                    [
                        "&0&l[&3Trial-Mod&0&l] &3",
                        "PlaceBuilder01"
                    ],
                    [
                        "&0&l[&3Trial-Mod&0&l] &3",
                        "xKylex"
                    ],
                    [
                        "&0&l[&eHelper&0&l] &e",
                        "MeatCity"
                    ],
                    [
                        "&0&l[&eHelper&0&l] &e",
                        "JamieMathematics"
                    ]
                ],
                "nearbyVisible": true,
                "excludeNearby": [
                    "UnclaimedBloom6",
                    "Unclaimedd",
                    "Unclaimeddd",
                    "Unclaimedddd",
                    "oiSam",
                    "Joshhuaaa"
                ]
            },
            "autoCongratz": {
                "enabled": true
            },
            "prefixReplacer": {},
            "advert": {
                "active":false,
                "lastAdvert":null,
                "msgs":[]
            }
        },
        "games": {
            "blacklist": [],
            "lottery": {
                "active": false,
                "startedAt": null,
                "lotteryPrice": 1000,
                "length": 60,
                "lotteryEntered": {}
            },
            "guesser": {
                "active": false,
                "startedAt": null,
                "prize": null,
                "defaultPrize": 25000,
                "length": 30,
                "attemptedPlayers": [],
                "correctNumber": null
            },
            "scramble": {
                "active": false,
                "defaultPrize": 100000,
                "length": 30,
                "answer": null,
                "prize": null,
                "startedAt": null
            }
        }
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
        
        //Debug Mode
        debugMode = config["utility"]["debugMode"]

        //Player Tracker
        trackerStaffVisible = config["utility"]["playerTracker"]["staffVisible"]
        trackerStaffList = config["utility"]["playerTracker"]["staffList"]
        trackerNearbyVisible = config["utility"]["playerTracker"]["nearbyVisible"]
        trackerNearbyExclude = config["utility"]["playerTracker"]["excludeNearby"]

        //Prefix Replacer
        prefixPlayers = config["utility"]["prefixReplacer"]

        //Blacklisted Players
        blacklistedPlayers = config["games"]["blacklist"]

        //Chat Advertiser
        lastChatAdvert = config["utility"]["advert"]["lastAdvert"]
        advertActive = config["utility"]["advert"]["adtive"]
        advertMsgs = config["utility"]["advert"]["msgs"]

        //Lottery
        lotteryActive = config["games"]["lottery"]["active"]
        lotteryStarted = config["games"]["lottery"]["startedAt"]
        lotteryPrice = config["games"]["lottery"]["lotteryPrice"]
        lotteryDuration = config["games"]["lottery"]["length"]
        lotteryEntered = config["games"]["lottery"]["lotteryEntered"]

        //Guesser
        guesserActive = config["games"]["guesser"]["active"]
        guesserStarted = config["games"]["guesser"]["startedAt"]
        guesserPrize = config["games"]["guesser"]["prize"]
        guesserDefaultPrize = config["games"]["guesser"]["defaultPrize"]
        guesserDuration = config["games"]["guesser"]["length"]
        guesserAttempted = config["games"]["guesser"]["attemptedPlayers"]
        guesserNumber = config["games"]["guesser"]["correctNumber"]

        //Scramble
        scrambleActive = config["games"]["scramble"]["active"]
        scrambleStarted = config["games"]["scramble"]["startedAt"]
        scramblePrize = config["games"]["scramble"]["prize"]
        scrambleDefaultPrize = config["games"]["scramble"]["defaultPrize"]
        scrambleDuration = config["games"]["scramble"]["length"]
        scrambleAnswer = config["games"]["scramble"]["answer"]

    }
}
function updateConfig() {
    s(JSON.stringify(config))
    FileLib.write(configDir, JSON.stringify(config))
    loadConfig()
    s(JSON.stringify(config))
}
function showHelp(page) {
    helpCommands = [
        "/tracker <staff|near|toggle>",
        "/lottery <start|set|info>",
        "/guesser <min> <max> [prize]",
        "/scramble <word|random> [prize]",
        "/paybal <player>",
        "/prefix <set|remove|list>",
        "/gt ",
        "/blacklist <add|remove|list> <player>"
        
    ]
    if (page == undefined) { page = 1 }
    dpage = page -= 1
    s(ChatLib.getCenteredText("&6--------------------- &eHelp Page &6----------------------&r"))
    for (i=dpage*10;i<dpage*10+10;i++) {
        if (helpCommands[i] == undefined) { }
        else {
            s("&6 - &e" + helpCommands[i])
        }
    }
    s(ChatLib.getCenteredText("&6" + (page*10+1) + " &e- &6" + (page*10+10)))
    s("&6" + ChatLib.getChatBreak())
}

register("command", function(page) {
    showHelp(page)
}).setName("chelp")

//Debug mode. No more changing t's into s()'s!
var debugMode
register("command", function() {
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

/*
██╗░░░██╗████████╗██╗██╗░░░░░██╗████████╗██╗░░░██╗
██║░░░██║╚══██╔══╝██║██║░░░░░██║╚══██╔══╝╚██╗░██╔╝
██║░░░██║░░░██║░░░██║██║░░░░░██║░░░██║░░░░╚████╔╝░
██║░░░██║░░░██║░░░██║██║░░░░░██║░░░██║░░░░░╚██╔╝░░
╚██████╔╝░░░██║░░░██║███████╗██║░░░██║░░░░░░██║░░░
░╚═════╝░░░░╚═╝░░░╚═╝╚══════╝╚═╝░░░╚═╝░░░░░░╚═╝░░░
*/

//-------------------------------------------------------------------------------------------------
/*
█▀█ █░░ ▄▀█ █▄█ █▀▀ █▀█   ▀█▀ █▀█ ▄▀█ █▀▀ █▄▀ █▀▀ █▀█
█▀▀ █▄▄ █▀█ ░█░ ██▄ █▀▄   ░█░ █▀▄ █▀█ █▄▄ █░█ ██▄ █▀▄
*/
var trackerStaffVisible
var trackerStaffList
var trackerNearbyVisible
var trackerNearbyExclude

var lastTabList = TabList.getNames()
var lastStaffUpdate = new Date().getTime()
var pmsg = "&b&lLoading..."
var onlineStaff = []

function updateStaffList() {
    new Thread(function (x) {

        var serverInfo = JSON.parse(FileLib.getUrlContent("https://api.minetools.eu/query/" + Server.getIP()))
        playerList = serverInfo.Playerlist

        while (serverInfo == undefined) { }
        tabList = TabList.getNames()
        onlineStaff = []

        for (i = 0; i < trackerStaffList.length; i++) {
            if (playerList.indexOf(trackerStaffList[i][1]) > -1) {
                if (tabList.indexOf(trackerStaffList[i][1]) == -1) {
                    onlineStaff.push([trackerStaffList[i][0], trackerStaffList[i][1], " ⚫"])
                }
                else {
                    onlineStaff.push([trackerStaffList[i][0], trackerStaffList[i][1], ""])
                }
            }
        }

        //Make String
        pmsg = "&b&l&nOnline Staff&r\n\n"
        if (onlineStaff.length > 0) {
            onlineStaff.forEach(function (player) {
                pmsg += player[0] + player[1] + player[2] + "&r\n"
            })
        }

    }).start()
}
register("tick", function (x) {

    tabList = TabList.getNames()

    if (new Date().getTime() - lastStaffUpdate > 21000) {
        lastStaffUpdate = new Date().getTime()
        updateStaffList()
    }

    //Player Joined
    tabList.forEach(function (playerName) {
        if (lastTabList.indexOf(playerName) == -1) {
            for (i = 0; i < trackerStaffList.length; i++) {
                if (playerName == trackerStaffList[i][1]) {
                    s(trackerStaffList[i][0] + trackerStaffList[i][1] + " &ehas joined")
                    if (trackerStaffVisible) {
                        for (i = 0; i < 2; i++) {
                            World.playSound("entity.llama.spit", 2, 1)
                        }
                    }
                    updateStaffList()
                    return
                }
            }
            s("&e" + playerName + " has joined!")
        }
    })

    //Player Left
    lastTabList.forEach(function (playerName) {
        if (tabList.indexOf(playerName) == -1) {
            for (i = 0; i < trackerStaffList.length; i++) {
                if (playerName == trackerStaffList[i][1]) {
                    s(trackerStaffList[i][0] + trackerStaffList[i][1] + " &ehas left")
                    updateStaffList()
                    return
                }
            }
            s("&e" + playerName + " has left")
        }
    })

    lastTabList = tabList
})
register("renderOverlay", function (x) {
    if (trackerStaffVisible == true) {
        height = 30
        onlineStaff.forEach(function (p) {
            height += 9
        })
        Renderer.drawRect(Renderer.color(0, 0, 0, 90), 2, 2, 175, height)
        Renderer.drawString(pmsg, 10, 10)
    }
})
//Nearby Players
var nearbyPlayers = []
var oldNearbyPlayers = []
var trackerNearbyExclude
var nearbyMsg

register("tick", function (x) {
    oldNearbyPlayers = nearbyPlayers
    nearbyPlayers = []
    World.getAllPlayers().forEach(function (player) {
        if (trackerNearbyExclude.indexOf(player.name) == -1) {
            nearbyPlayers.push(player.name)
            if (oldNearbyPlayers.indexOf(player.name) == -1) {
                if (trackerNearbyVisible) {
                    for (i = 0; i < 5; i++) {
                        World.playSound("block.wood_button.click_on", 2, 1)
                    }
                }
            }
        }
    })
})
register("renderOverlay", function (a) {
    if (trackerNearbyVisible == true) {
        nearbyMsg = "&b&l&nNearby Players\n\n"
        nearbyPlayers.forEach(function (player) {
            nearbyMsg += "&a" + player + "&r\n"
        })
        height = 30
        nearbyPlayers.forEach(function (p) {
            height += 9
        })
        Renderer.drawRect(Renderer.color(0, 0, 0, 90), 190, 2, 175, height)
        Renderer.drawString(nearbyMsg, 200, 10)
    }
})

register("command", function (a, b, c) {
    if (a == undefined) {
        s("&cCorrect Syntax: /tracker <staff, near, toggle>")
        return
    }
    if (a == "staff") {
        if (b == "list") {
            msg = [
                "&b&l&nStaff List&r",
                ""
            ]
            trackerStaffList.forEach(function (staffMember) {
                msg.push(staffMember[0] + staffMember[1])
            })
            printCenteredText(msg)
        }
        else if (b == "t" || b == "toggle") {
            if (trackerStaffVisible == true) {
                config["utility"]["playerTracker"]["staffVisible"] = false
            }
            else {
                config["utility"]["playerTracker"]["staffVisible"] = true
            }
            updateConfig()
        }
    }
    else if (a == "nearby" || a == "near") {
        if (b == "t" || b == "toggle") {
            if (trackerNearbyVisible == true) {
                config["utility"]["playerTracker"]["nearbyVisible"] = false
            }
            else {
                config["utility"]["playerTracker"]["nearbyVisible"] = true
            }
            updateConfig()
        }
    }
    else if (a == "t" || a == "toggle") {
        if (trackerStaffVisible == true || trackerNearbyVisible == true) {
            config["utility"]["playerTracker"]["staffVisible"] = false
            config["utility"]["playerTracker"]["nearbyVisible"] = false
        }
        else {
            config["utility"]["playerTracker"]["staffVisible"] = true
            config["utility"]["playerTracker"]["nearbyVisible"] = true
        }
        updateConfig()
    }
}).setName("tracker")

updateStaffList()

/*
█▄▄ ▄▀█ █░░ ▄▀█ █▄░█ █▀▀ █▀▀   ▀█▀ █▀█ ▄▀█ █▀▀ █▄▀ █▀▀ █▀█
█▄█ █▀█ █▄▄ █▀█ █░▀█ █▄▄ ██▄   ░█░ █▀▄ █▀█ █▄▄ █░█ ██▄ █▀▄
*/
//Show the balance and online players on screen

var balance = 0

ChatLib.command("bal")

//Update balance and online players every tick
register("tick", function(x) {
    ChatLib.actionBar("&aBalance: &7$" + formatNumber(balance) + "       &aOnline: &7" + TabList.getNames().length)
})

var moneyOut = [
    /&aShop > &r&fYou bought .+ for &r&c\$([0-9,.]+)&r&f\.&r/,
    /&a\$([0-9,.]+) has been sent to .+/,
    /&fYou purchased .+ &ffor &c\$([0-9,.]+)&r&f!&r/,
    /&a\[Shop] &rYou bought .+ from .+ for \$([0-9,.]+)\.&r/
]
var moneyIn = [
    /&aShop > &r&fYou sold .+ for a total of &r&a\$([0-9,.]+)&r&f\.&r/,
    /&a\$([0-9,.]+)&r&6 has been received from.+/,
    /&fYou earned &b\$([0-9,.]+)&r&r&f!&r/,
    /&a\[Shop] &rYou sold .+ to .+ for \$([0-9,.]+)\.&r/,
    /&aShop > &r&fYou sold .+ for &r&a\$([0-9,.]+)&r&f\.&r/,
    /&a\[Shop] &r.+ bought .+ for \$([0-9,.]+).&r/
]

moneyOut.forEach(function(msg) {
    register("chat", function(msg) {
        match = msg.match(msg)
        amount = parseInt(match[0].replaceAll(",",""))
        s("&cBalance - $" + amount)
        balance -= amount
    }).setCriteria(msg)
})

moneyIn.forEach(function(msg) {
    register("chat", function(msg) {
        match = msg.match(msg)
        amount = parseInt(match[0].replaceAll(",",""))
        //s("&aBalance + $" + amount)
        balance += amount
    }).setCriteria(msg)
})

//Set balance via /bal
register("chat", function(x) {
    balance = parseInt(x.replaceAll(",",""))
}).setChatCriteria("Balance: $${x}")

//Pay someone your whole balance
register("command", function(player) {
    t("/pay " + player + " " + balance)
}).setName("paybal")

/*
█▀▄▀█ █▀▀ █▀ █▀ ▄▀█ █▀▀ █▀▀   █▀▀ █ █░░ ▀█▀ █▀▀ █▀█
█░▀░█ ██▄ ▄█ ▄█ █▀█ █▄█ ██▄   █▀░ █ █▄▄ ░█░ ██▄ █▀▄
*/

var filterMessages = [
    "&aNow ${*} your island.&r",
    "Shift + Left Click to break crop&r",
    /&a\[Shop] &r.+ bought .+ for \$[\d,.]+.&r/,
    /&a\[Shop] &r&r\$[\d,.]+ \d+ \w+&r&7 shop is out of stock!&r/
]
filterMessages.forEach(function(filterMsg) {
    register("chat", function(event) {
        cancel(event)
    }).setChatCriteria(filterMsg)
})

/*
█▀█ █▀█ █ █░█ ▄▀█ ▀█▀ █▀▀   █▀▀ █░█ ▄▀█ █▄░█ █▄░█ █▀▀ █░░
█▀▀ █▀▄ █ ▀▄▀ █▀█ ░█░ ██▄   █▄▄ █▀█ █▀█ █░▀█ █░▀█ ██▄ █▄▄
*/
function sayPrivateChat(message) {
    ChatLib.chat("&3Private > &6[MVP&0++&6] UnclaimedBloom6&f: " + message)
}
var privateChannel = false
register("command", function() {
    message = ""
    if (arguments.length > 0) {
        for (i=0;i <arguments.length;i++) {
            message += arguments[i] + " "
        }
    }

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
	sayPrivateChat(message)
}).setName("pm")

register("messageSent", function(message, event) {
	var isCommand = message.startsWith("/")
	if (isCommand == false) {
		if (privateChannel == true) {
            sayPrivateChat(message)
            cancel(event)
		}
	}
})

/*
▄▀█ █░█ ▀█▀ █▀█ ▄▄ █▀ █▀▀ █░░ █░░
█▀█ █▄█ ░█░ █▄█ ░░ ▄█ ██▄ █▄▄ █▄▄
*/

//TO BE ADDED (maybe)

/*
█▀▀ █░█ ▄▀█ ▀█▀   █░░ █▀█ █▀▀ █▀
█▄▄ █▀█ █▀█ ░█░   █▄▄ █▄█ █▄█ ▄█
*/

//Save the ChatLog to a text file in the format "PlayerName-ServerIP-YY/MM/DD.txt" in the file ".minecraft/ChatLogs"
register("chat", function(message) {
	x = new Date()
    fileName = Player.getName() + "-" + Server.getIP() + "-" + x.getFullYear() + "-" + (x.getMonth()+1) + "-" + x.getDate() + ".txt"
    timeStamp = "[" + x.getHours() + ":" + x.getMinutes() + ":" + x.getSeconds() + "]"
    try {
        oldStuff = FileLib.read("./ChatLogs/" + fileName)
        oldStuff += timeStamp + ChatLib.removeFormatting(message) + "\n"
        FileLib.write("./ChatLogs/" + fileName, oldStuff)
    }
    catch(error) {
        var File = Java.type("java.io.File")
        f = new File("ChatLogs","./")
        f.mkdirs()
        oldStuff = FileLib.read("./ChatLogs/" + fileName)
        oldStuff += timeStamp + ChatLib.removeFormatting(message) + "\n"
        FileLib.write("./ChatLogs/" + fileName, oldStuff)
    }
}).setCriteria("${message}")

/*
█▀▀ █▄░█ █▀▀ █░█ ▄▀█ █▄░█ ▀█▀ █▀▀ █▀█
██▄ █░▀█ █▄▄ █▀█ █▀█ █░▀█ ░█░ ██▄ █▀▄
*/

//Enchants, [enchant-id, in-game, CT-name, max-level]
var enchantsList = [
    [0,"protection","protect.all",4],
    [1,"fireprot","protect.fire",4],
    [2,"featherfall","protect.fall",4],
    [3,"blastprotect","protect.explosion",4],
    [4,"projprot","protect.projectile",4],
    [5,"respiration","oxygen",3],
    [6,"aquaaffinity","waterWorker",1],
    [7,"thorns","thorns",3],
    [8,"depthstrider","waterWalker",3],
    [9,"frostwalker","frostWalker",2],
    [10,"binding","binding_curse",1],
    [16,"sharpness","damage.all",5],
    [17,"smite","damage.undead",5],
    [18,"baneofarthropods","damage.arthropods",5],
    [19,"knockback","knockback",2],
    [20,"fireaspect","fire",2],
    [21,"looting","lootBonus",3],
    [22,"sweepingedge","sweeping",3],
    [32,"efficiency","digging",5],
    [33,"silktouch","untouching",1],
    [34,"unbreaking","durability",3],
    [35,"fortune","lootBonusDigger",3],
    [48,"power","arrowDamage",5],
    [49,"punch","arrowKnockback",2],
    [50,"flame","arrowFire",1],
    [51,"infinity","arrowInfinite",1],
    [61,"luck","lootBonusFishing",3],
    [62,"lure","fishingSpeed",3],
    [70,"mending","mending",1],
    [71,"vanishingcurse","vanishing_curse",1],
    
]
var itemEnchants = [
    [["Pickaxe"],[32, 33, 34, 70]],
    [["Axe"],[16, 17, 18, 32, 34, 35, 70]],
    [["Sword"],[16, 17, 18, 20, 21, 22, 34, 70]],
    [["Shovel"],[32, 33, 34, 70]],
    [["Hoe"],[32, 34, 35, 70]],
    [["Helmet"],[0, 1, 3, 4, 5, 6, 34, 70]],
    [["Chestplate","Leggings","Tunic","Pants"],[0, 1, 3, 4, 34, 70]],
    [["Boots"],[0, 1, 2, 3, 4, 8, 34, 70]],
    [["Bow"],[48, 49, 50, 51, 34, 70]],
    [["Rod"],[61, 62, 34, 70]],
    [["Shears"],[32, 34, 70]],
]

register("command", function(e) {
    var itemName = Player.getHeldItem().getName().replace(/[0-9.]+ /, "")
    s(itemName)
    var itemType = itemName.split(" ")
    for (i=0; i < itemEnchants.length; i++) {
        itemEnchants[i][0].forEach(function(a) {
            if (itemType[1] == a || itemName == a) {
                s("&aEnchanting The Item!")
                enchants = itemEnchants[i][1]
                currentEnchants = Player.getHeldItem().getEnchantments()
                finalEnchants = []
                dupes = []
                //For every enchant on the current tool
                currentEnchants.forEach(function(name) {
                    enchantsList.forEach(function(enchantInfo) {
                        //If the enchant name and level matches (max level enchant already applied) then add it as a duplicate
                        if (name == enchantInfo[2] && currentEnchants[name] == enchantInfo[3]) {
                            dupes.push(enchantInfo[0])
                        }
                    })
                })
                //Filter duplicate enchants and add the rest to an array
                enchants.forEach(function(id) {
                    if (dupes.indexOf(id) == -1) {
                        finalEnchants.push(id)
                    }
                })
                //If the tool is already maxed then stop
                if (finalEnchants.length == 0) {
                    s("&cThis item is already fully enchanted!")
                }
                else {
                    //Convert the enchant ID to the /enchant name and enchant the tool
                    finalEnchants.forEach(function(enchantID) {
                        enchantsList.forEach(function(enchantInfo) {
                            //If the enchant ID matches in the long list then get the second item (/enchant id) and /enchant it
                            if (enchantID == enchantInfo[0]) {
                                t("/enchant " + enchantInfo[1] + " " + enchantInfo[3])
                            }
                        })
                    })
                }
            }
        })
    }
    if (Player.getHeldItem().getDamage() != 0) {
        t("/fix")
    }
}).setName("gt")

/*
▄▀█ █░█ ▀█▀ █▀█   █▀▀ █▀█ █▄░█ █▀▀ █▀█ ▄▀█ ▀█▀ ▀█
█▀█ █▄█ ░█░ █▄█   █▄▄ █▄█ █░▀█ █▄█ █▀▄ █▀█ ░█░ █▄
*/

register("chat", function(player, purchase) {
    if (Player.getName() == "Unclaimedd") {
        var purchaseArray = purchase.split(" ")
        purchaseArray.forEach(function(x) {
        })
        if (purchaseArray[1] == "command") {
            ChatLib.say("Congratz on the " + purchase + ", " + player + "!")
        }
        else if (purchaseArray[0] == "Upgrade") {
            ChatLib.say("Congratz on the " + purchaseArray[4] + " rank, " + player + "!")
        }
        else {
            ChatLib.say("Congratz on the " + purchase + ", " + player + "!")
        }
    }
}).setChatCriteria("[Broadcast] Thank you ${player} for purchasing ${purchase}")

/*
█░█░█ █▀▀ █░░ █▀▀ █▀█ █▀▄▀█ █▀▀   █▀▀ █▀█ █▀▄▀█ █▀▄▀█ ▄▀█ █▄░█ █▀▄
▀▄▀▄▀ ██▄ █▄▄ █▄▄ █▄█ █░▀░█ ██▄   █▄▄ █▄█ █░▀░█ █░▀░█ █▀█ █░▀█ █▄▀
*/

// the /welcome command thing
var lastPlayerJoined = ""
register("chat", function(player) {
    lastPlayerJoined = player
}).setChatCriteria("Welcome ${player}!")

register("command", function(player) {
    if (player == undefined) { }
    else { lastPlayerJoined = player }
    msgArr = [
        "Welcome, " + lastPlayerJoined + "!",
        "Welcome to ClassicSB, " + lastPlayerJoined + "!",
        "Welcome, " + lastPlayerJoined + "! Do /is to get started."
    ]
    a = pickRandom(msgArr)
    ChatLib.say(a)
}).setName("wlc")

/*
█▀█ █▀█ █▀▀ █▀▀ █ ▀▄▀   █▀█ █▀▀ █▀█ █░░ ▄▀█ █▀▀ █▀▀ █▀█
█▀▀ █▀▄ ██▄ █▀░ █ █░█   █▀▄ ██▄ █▀▀ █▄▄ █▀█ █▄▄ ██▄ █▀▄
*/

var prefixPlayers

var nameFormats = [
    /&0\[&r&(.)lvl\. \d+&r&0\]&r&.&ki&r&0\[&r&.([\w-]+)&r&0\]&r&.&ki&r([\w&~]+) &r&f» .+/, //Ranked player talking
    /&0\[&r&(.)lvl\. \d+()&r&0\]&r&7(\w+) &r&f» .+/, //Default talking
    /&6\[&r&(.)&ki&r&0\[&r&.([\w-]+)&r&0]&r&.&ki&r&.([\w&~]+)&r&6 -> &r&cme&r&6] &r.+/, //Ranked player private message received
    /&6\[&r&cme&r&6 -> &r&(.)&ki&r&0\[&r&.([\w-]+)&r&0]&r&.&ki&r([\w&~]+)&r&6] &r.+/, //Ranked player message sent
    /&a\$\d.+ has been sent to &r&(.)&ki&r&0\[&r&.([\w-]+)&r&0]&r&.&ki&r([\w&~]+)&r\.&r/, //Money received
    /&a\$\d.+&r&6 has been received from&r&a &r&(.)&ki&r&0\[&r&.([\w-]+)&r&0]&r&.&ki&r([\w&~]+)&r&6\.&r/, //Money sent
    /&6\[&r&cme&r&6 -> &r&0\[&r&(.)([\w-]+)&r&0]&r([\w&~]+)&r&6] &r.+/, //Sent message to staff
    /&6\[&r&0\[&r&(.)([\w-]+)&r&0]&r([\w&~]+)&r&6 -> &r&cme&r&6] &r.+/, //Staff private message received
    /&0\[&r&(.)lvl\. \d+&r&0]&r&0\[&r&.([\w-]+)&r&0]&r([\w&~]+) &r&f» .+/ //Staff talking in main chat
]
nameFormats.forEach(function(re) {
    register("chat", function(e) {
        msg = ChatLib.getChatMessage(e, true).replace(/§/g, "&")
        if (re.exec(msg) !== null) {
            matches = msg.match(re)
            //Set variables to make it easier
            rankColor = "&" + matches[1]
            prefix = matches[2]
            playerFormatted = matches[3]
            playerUnformatted = ChatLib.removeFormatting(playerFormatted).replace("~","").toLowerCase()
            //If the player has a custom prefix then continue
            if (playerUnformatted.toLowerCase() in prefixPlayers) {
                //If color isn't defined then set it as the player's normal default color eg &4 for immortal default
                if (prefixPlayers[playerUnformatted]["color"] !== "") {
                    newColor = prefixPlayers[playerUnformatted]["color"]
                }
                else {
                    newColor = rankColor
                }
                //New variables
                newPrefix = prefixPlayers[playerUnformatted]["prefix"]
                newName = prefixPlayers[playerUnformatted]["name"]
                //Build the new message
                //If the player is a default then add a prefix
                if (prefix == "") {
                    newMsg = msg.replace(playerFormatted, newColor + "&ki&0[" + newColor + newPrefix + "&0]" + newColor + "&ki&r" + newName).replace(new RegExp(rankColor,"g"),newColor)
                }
                else {
                    newMsg = msg.replace(playerFormatted, newName).replace(new RegExp(rankColor,"g"),newColor).replace(prefix, newPrefix).replace("»","&r&f»")
                }
                s(newMsg)
                cancel(e)
            }
        }
    }).setCriteria("${*}")
})

register("command", function(a, b, c, d, e) {
    //Set command
    if (a == "set") {
        //If there is an important value missing then error message and return
        if (b == undefined || c == undefined || d == undefined) {
            s("&cError: /prefix set <player> <color> <prefix> [newName]")
            return
        }
        else {
            b = b.toLowerCase()
            //Check if the name is whitespace only with & for colors
            if (/^[\w&]+$/.test(b) == false) {
                s("&cError: Illegal characters.")
                return
            }
            //Check if the color is a valid color code
            else if (/^&[a-f0-9]$/.test(c) == false) {
                s("&cError: Colors must be &👻a-&👻f, &👻0-&👻9.")
                return
            }
            //If the new name is undefined, set it as their old one with the set color
            if (e == undefined) {
                e = c + b
            }
            //Add the new entry to the config
            config["utility"]["prefixReplacer"][b] = {
                "color":c,
                "prefix":d,
                "name":e
            }
            //Say that it worked and update the config
            s("&aSuccessfully updated &6" + b + " &ato show as " + c + "&ki&0[" + c + d + "&0]" + c + "&ki&r" + e)
            updateConfig()
        }
    }
    //Remove someone's prefix
    else if (a == "remove") {
        b = b.toLowerCase()
        delete config["utility"]["prefixReplacer"][b]
        s("&aSuccessfully removed &6" + b + " &afrom the prefix list.")
        updateConfig()
    }
    else if (a == "list") {
        msg = [
            "",
            "&0----- &aPrefix Players &0-----",
            ""
        ]
        for (x in prefixPlayers) {
            color = prefixPlayers[x]["color"]
            prefix = prefixPlayers[x]["prefix"]
            player = prefixPlayers[x]["name"]
            msg.push(x + " - " + color + "&ki&0[" + color + prefix + "&0]" + color + "&ki" + player)
        }
        msg.push("")
        printCenteredText(msg)
    }
    else {
        s("&cError: /prefix <set|remove|list>")
    }
}).setName("prefix")

/*
█▀█ █░█░█ █▀█   █▀▄▀█ █▀█ █▀▄ █▀▀
█▄█ ▀▄▀▄▀ █▄█   █░▀░█ █▄█ █▄▀ ██▄
*/
//OwO
var replacements = {
    'r': 'w',
    'l': 'w',
    'R': 'W',
    'L': 'W',
  //  'ow': 'OwO',
    'no': 'nu',
    'has': 'haz',
    'have': 'haz',
    'says': 'sez',
    'this':'dis',
    'you': 'uu',
    'the': 'da',
    'The': 'Da',
    'THE': 'THE',
  }
function replaceOwo(message) {
    for (thing in replacements) {
        //s(thing + " " + replacements[thing])
        message = message.replaceAll(thing, replacements[thing])
    }
    return message
}
var owo = false
register("messageSent",function(message, event) {
    if (owo == true && message.startsWith("/") == false) {
        if (privateChannel) {
            sayPrivateChat(replaceOwo(message))
        }
        else {
            ChatLib.say(replaceOwo(message))
        }
        cancel(event)
    }
})
register("command", function() {
    message = ""
    if (arguments.length > 0) {
        for (i=0;i <arguments.length;i++) {
            message += arguments[i] + " "
        }
    }
    if (message != "") {
        ChatLib.say(replaceOwo(message))
    }
    else {
        if (owo) {
            owo = false
            s("&cOwO mode disabled!")
        }
        else {
            owo = true
            s("&aOwO mode enabled!")
        }
    }
}).setName("owo")

/*
█▀▀ █░█ ▄▀█ ▀█▀   ▄▀█ █▀▄ █░█ █▀▀ █▀█ ▀█▀ █ █▀ █▀▀ █▀█
█▄▄ █▀█ █▀█ ░█░   █▀█ █▄▀ ▀▄▀ ██▄ █▀▄ ░█░ █ ▄█ ██▄ █▀▄
*/

var lastChatAdvert
var advertActive
var advertMsgs

register("command", function(a, b, c) {
    if (a == "help") {
        s("&a/advert toggle")
        s("&a/advert list")
        s("&a/advert set <number> <message>")
        s("&a/advert delay <minutes>")
        return
    }
    else if (a == "toggle") {
        if (advertActive == false) {
            config["utility"]["advert"]["active"] = true
            s("&aChat Advert beginning!")
        }
        else {
            config["utility"]["advert"]["active"] = true
            s("&cChat Advert stopped!")
        }
        updateConfig()
    }
    else if (a == "list") {
        if (advertMsgs.length == 0) {
            s("&cError: No messages set!")
            return
        }
        s("&cChat Advert Messages:")
        advertMsgs.forEach(function(x) {
            s("&f\"" + x + "\"")
        })
        s("")
        return
    }
    else if (a == "set") {
        s("Setting Value")
    }
}).setName("advert")

register("tick", function(x) {
    /*if (new Date().getTime() - lastChatAdvert > 2000 || lastChatAdvert == null) {
        updateConfig()
    }*/
})

/*
░██████╗░░█████╗░███╗░░░███╗███████╗░██████╗
██╔════╝░██╔══██╗████╗░████║██╔════╝██╔════╝
██║░░██╗░███████║██╔████╔██║█████╗░░╚█████╗░
██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░░╚═══██╗
╚██████╔╝██║░░██║██║░╚═╝░██║███████╗██████╔╝
░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚═════╝░
*/

var blacklistedPlayers

register("command", function(a, b) {
    if (a == "list") {
        msg = [
            "",
            "&8----- &7Blacklisted Players &8-----",
            ""
        ]
        blacklistedPlayers.forEach(function(player) {
            msg.push("&7" + player)
        })
        msg.push("")
        printCenteredText(msg)
    }
    else if (a == undefined || b == undefined) {
        s("&cError: /blacklist <add|remove|list> [player]")
        return
    }
    else {
        if (a == "add" && b !== undefined) {
            config["games"]["blacklist"].push(b)
            s("&aSuccessfully added &c" + b + " &ato the game blacklist!")
            updateConfig()
        }
        else if (a == "remove" && b !== undefined) {
            newList = []
            if (isBlacklisted(b)) {
                blacklistedPlayers.forEach(function(player) {
                    if (player.toLowerCase() !== b.toLowerCase()) {
                        newList.push(player)
                    }
                })
                config["games"]["blacklist"] = newList
                s("&aSuccessfully removed &c" + b + " &afrom the game blacklist!")
                updateConfig()
            }
            else {
                s("&cError: That player is not currently blacklisted!")
            }
        }
    }
}).setName("blacklist")

function isBlacklisted(player) {
    blacklisted = false
    player = player.toLowerCase()
    blacklistedPlayers.forEach(function(x) {
        if (player == x.toLowerCase()) {
            blacklisted = true
        }
    })
    if (blacklisted == true) {
        return true
    }
    else {
        return false
    }
}

/*
█░░ █▀█ ▀█▀ ▀█▀ █▀▀ █▀█ █▄█
█▄▄ █▄█ ░█░ ░█░ ██▄ █▀▄ ░█░
*/
var lotteryStarted
var lotteryPrice
var lotteryActive
var lotteryDuration
var lotteryEntered

function resetLottery() {
    config["games"]["lottery"]["lotteryEntered"] = {}
    config["games"]["lottery"]["startedAt"] = null
    config["games"]["lottery"]["active"] = false
    updateConfig()
}
//Lottery commands
register("command", function (a, b, c) {
    //Start the Lottery
    if (a == "start") {
        if (lotteryActive == false) {
            t("A lottery is starting! Pay me $" + formatNumber(lotteryPrice) + " per ticket. The lottery will automatically end after " + lotteryDuration + " seconds. You can buy multiple tickets at a time!")
            config["games"]["lottery"]["active"] = true
            config["games"]["lottery"]["startedAt"] = new Date().getTime()
            config["games"]["lottery"]["lotteryEntered"] = {}
            updateConfig()
        }
        else {
            s("&cError: A lottery is already active!")
        }
    }
    else if (a == "cancel") {
        if (lotteryActive == true) {
            t("The lottery has been cancelled! Players have been refunded.")
            for (player in lotteryEntered) {
                t("/pay " + player + " " + lotteryPrice * lotteryEntered[player])
            }
            resetLottery()
        }
        else {
            s("&cError: The lottery is not active currently!")
        }
    }
    //Set values
    else if (a == "set" && b != undefined && c != undefined) {
        if (b == "lotteryPrice" || b == "price") {
            config["games"]["lottery"]["lotteryPrice"] = parseInt(c)
            updateConfig()
            s("&aSuccessfully updated lotteryPrice to " + parseInt(c))
        }
        else if (b == "time" || b == "duration") {
            config["games"]["lottery"]["length"] = parseInt(c)
            updateConfig()
            s("&aSuccessfully updated lotteryDuration to " + parseInt(c))
        }
        else {
            return
        }
    }
    //Info about lottery (config settings)
    else if (a == "info") {
        lotteryInfoMsgs = [
            "",
            "&0 -- &6Lottery Stuff &0 -- ",
            "",
            "&7Active: &e" + lotteryActive,
            "&7Ticket Price: &e$" + formatNumber(lotteryPrice),
            "&7Duration: &e" + lotteryDuration + " &7seconds",
            ""
        ]
        printCenteredText(lotteryInfoMsgs)
    }
    else {
        s("&cSyntax: /lottery <start, set, info>")
    }
}).setName("lottery")
//Money Received
register("chat", function (amount, player) {
    //Setup variables for player's raw name and amount they paid
    var realAmount = parseInt(amount.replaceAll(",", ""))
    realName = clearPrefix(player)

    //If paid amount is higher than cost of ticket
    if (realAmount >= lotteryPrice && lotteryActive == true) {
        if (isBlacklisted(realName)) {
            t("/pay " + realName + " " + realAmount)
            return
        }
        excessMoney = realAmount
        ticketsBought = 1
        //Remove excess amount of money if ticket price isn't exactly divisible
        for (i = 0; i < (realAmount / lotteryPrice) - 1; i++) {
            excessMoney -= lotteryPrice
            ticketsBought++
        }
        //If there's excess money pay the player back
        if (excessMoney != 0 && hasDecimal(realAmount / ticketsBought) == true) {
            t("/pay " + realName + " " + excessMoney)
        }

        realAmount = realAmount - excessMoney

        //If the player isn't in the list yet then add them
        if (lotteryEntered[realName] == undefined) {
            lotteryEntered[realName] = ticketsBought
        }

        //If player's in the list then add to their ticket count
        else {
            lotteryEntered[realName] += ticketsBought
        }
        //Let the player know how many tickets/total tickets they purchased
        t("/w " + realName + " You just bought " + ticketsBought + " tickets! (" + lotteryEntered[realName] + " total)")
        config["games"]["lottery"]["lotteryEntered"] = lotteryEntered
        updateConfig()
    }
    //If player pays less than ticket price pay them back full amount
    else if (realName < lotteryPrice && lotteryActive == true) {
        t("/pay " + realName + " " + realAmount)
    }
}).setChatCriteria("$${amount} has been received from ${player}")
//Auto end lottery
register("tick", function (x) {
    //If it's been at least x seconds since the lottery started
    if (lotteryStarted != null && new Date().getTime() - lotteryStarted > (lotteryDuration * 1000)) {
        //Add people to big array to choose random 
        playerHat = []
        for (person in lotteryEntered) {
            for (i = 0; i < lotteryEntered[person]; i++) {
                playerHat.push(person)
            }
        }
        //Pick random winner
        winner = pickRandom(playerHat)
        t("Lottery Over! The winner was " + winner.replace("~", "") + ". They have just won $" + formatNumber(playerHat.length * lotteryPrice) + " with " + lotteryEntered[winner] + " tickets!")
        t("/pay " + winner + " " + playerHat.length * lotteryPrice)

        //Summary of tickets bought in the lottery
        lotteryEndMsg = [
            "&6Lottery Ticket Buyers",
            ""
        ]
        for (player in lotteryEntered) {
            lotteryEndMsg.push("&7" + player + "&8: " + lotteryEntered[player] + " tickets")
        }
        printCenteredText(lotteryEndMsg)
        resetLottery()
    }
})

/*
█▀▀ █░█ █▀▀ █▀ █▀ █▀▀ █▀█
█▄█ █▄█ ██▄ ▄█ ▄█ ██▄ █▀▄
*/
//Guessing Game Stuff
var guesserActive
var guesserStarted
var guesserPrize
var guesserDefaultPrize
var guesserDuration
var guesserAttempted
var guesserNumber

function resetGuesser() {
    config["games"]["guesser"]["active"] = false
    config["games"]["guesser"]["startedAt"] = null
    config["games"]["guesser"]["prize"] = null
    config["games"]["guesser"]["attemptedPlayers"] = []
    config["games"]["guesser"]["correctNumber"] = null
    updateConfig()
}

register("command", function (min, max, prize) {
    if (min == undefined || max == undefined) {
        s("&cCorrect Syntax: /guesser <minimum> <maximum> <prize>")
        return
    }
    if (prize == undefined) {
        prize = guesserDefaultPrize
    }
    config["games"]["guesser"]["active"] = true
    ans = Math.floor(Math.random() * max + 1)
    config["games"]["guesser"]["correctNumber"] = ans
    config["games"]["guesser"]["prize"] = parseInt(prize)
    s("&aAnswer: &6" + ans)
    t("I am thinking of a number between " + min + " and " + max + ". Whoever guesses it wins $" + formatNumber(prize) + ". /msg me your answers!")
    config["games"]["guesser"]["startedAt"] = new Date().getTime()
    updateConfig()
}).setName("guesser")

register("chat", function (player, number) {
    var exit = false
    var pName = clearPrefix(player).replace("[", "")
    var playerAns = parseInt(number)
    if (isNaN(playerAns) == true) {
        return
    }
    if (guesserActive == true && isBlacklisted(pName) == false) {
        guesserAttempted.forEach(function (x) {
            if (pName == x) {
                t("/w " + pName + " You have already had ur guess xd")
                exit = true
            }
        })
        if (exit == true) {
            return
        }
        else {
            if (playerAns == ans) {
                t(pName + " Guessed the right answer! (" + ans + ")")
                t("/pay " + pName + " " + guesserPrize)
                resetGuesser()
            }
            else {
                msgs = [
                    "lol nope!",
                    "wrong!",
                    "Better luck next time!",
                    "xd nerd wrong!",
                    "incorrect! xd",
                    "guess better loser",
                    "no"
                ]
                t("/w " + pName + " " + pickRandom(msgs))
                config["games"]["guesser"]["attemptedPlayers"].push(pName)
                updateConfig()
            }
        }
    }
}).setChatCriteria("${player} -> me] ${message}")

register("tick", function (e) {
    if (guesserStarted != null && new Date().getTime() - guesserStarted > 30000) {
        t("Game Over! Nobody guessed the number in time. The correct answer was " + guesserNumber + "!")
        resetGuesser()
    }
})

/*
█▀ █▀▀ █▀█ ▄▀█ █▀▄▀█ █▄▄ █░░ █▀▀
▄█ █▄▄ █▀▄ █▀█ █░▀░█ █▄█ █▄▄ ██▄
*/



function shuffle(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1))
        var temp = array[i]
        array[i] = array[j]
        array[j] = temp
    }
    return array
}
function resetScramble() {
    config["games"]["scramble"]["active"] = false
    config["games"]["scramble"]["startedAt"] = null
    config["games"]["scramble"]["prize"] = null
    config["games"]["scramble"]["answer"] = null
    updateConfig()
}

var wordsList = "./config/ChatTriggers/modules/ClassicSB/scrambleWordList.json"

var scrambleActive
var scrambleStarted
var scramblePrize
var scrambleDefaultPrize
var scrambleDuration
var scrambleAnswer

register("command", function(word, prize) {
    if (word == undefined) {
        s("&cCorrect Syntax: /scramble <word> [prize]")
        return
    }
    else if (word == "random") {
        wordFile = JSON.parse(FileLib.read(wordsList))
        config["games"]["scramble"]["answer"] = pickRandom(wordFile)
    }
    else if (word == "cancel" && scrambleActive == true) {
        t("This round of unscramble has been cancelled! the word was \"" + scrambleAnswer + "\"!")
        resetScramble()
        return
    }
    else {
        config["games"]["scramble"]["answer"] = word
    }
    if (prize == undefined) {
        prize = scrambleDefaultPrize
    }
    config["games"]["scramble"]["prize"] = prize
    wordArray = config["games"]["scramble"]["answer"].split("")
    scrambledWord = shuffle(wordArray).join("")
    s("Answer: " + config["games"]["scramble"]["answer"])
    t("The first person to unscramble \"" + scrambledWord + "\" gets $" + formatNumber(prize) + "! /msg me your answer!")
    config["games"]["scramble"]["startedAt"] = new Date().getTime()
    config["games"]["scramble"]["active"] = true
    updateConfig()
}).setName("scramble")

register("chat", function(player, message) {
    realName = clearPrefix(player)
    if (message == scrambleAnswer && scrambleActive == true && isBlacklisted(realName) == false) {
        t(realName + " guessed the answer right! The word was \"" + scrambleAnswer + "\"! ")
        t("/pay " + realName + " " + scramblePrize)
        resetScramble()
    }
}).setChatCriteria("[${player} -> me] ${message}")

register("tick", function(x) {
    if (scrambleStarted != null && new Date().getTime() - scrambleStarted > (scrambleDuration * 1000)) {
        t("Nobody guessed the word in time! The answer was " + scrambleAnswer + "!")
        resetScramble()
    }
})

loadConfig()
