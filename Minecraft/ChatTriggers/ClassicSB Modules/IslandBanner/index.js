
var logDir = "./config/ChatTriggers/modules/IslandBanner/banLogs.json"
var configDir = "./config/ChatTriggers/modules/IslandBanner/config.json"
var config
function loadConfig() {
    defaultConfig = {
        "corner1":null,
        "corner2":null,
        "banList":[],
        "safeList":[]
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
        corner1 = config["corner1"]
        corner2 = config["corner2"]
        banList = config["banList"]
        safeList = config["safeList"]
    }
}
function updateConfig() {
    FileLib.write(configDir, JSON.stringify(config))
    loadConfig()
}
function getCoords() {
    return [parseInt(Player.getX()), parseInt(Player.getY()), parseInt(Player.getZ())]
}
function isBetween(n, a, b) {
    return (n - a) * (n - b) <= 0
}
function isInList(object, array) {
    if (array == undefined || array.length == 0) { return false}
    for (i=0;i<array.length;i++) {
        if (array[i] == object) { return true }
    }
    return false
}
function removeObject(object, array) {
    if (array == undefined || array.length == 0) { return []}
    newList = []
    for (i=0;i<array.length;i++) {
        if (array[i] !== object) { newList.push(array[i]) }
    }
    return newList
}
function newLogEntry(player) {
    msg = getMonthDay() + " [" + get24hTime() + "] " + player + " was banned!\n"
    s(msg)
    oldLogs = FileLib.read(logDir)
    if (oldLogs == null) { oldLogs = "" }
    FileLib.write(logDir, oldLogs + msg)
}
function get24hTime() {
    dateNow = new Date()
    x = [dateNow.getHours(), dateNow.getMinutes(), dateNow.getSeconds()]
    //Turn 4:38:3 into 04:38:30
    for (i=0;i<x.length;i++) {
        if (x[i].toString().length == 1) { x[i] = "0" + x[i]}
    }
    return x[0] + ":" + x[1] + ":" + x[2]
}
function getMonthDay() {
    dateNow = new Date()
    months = ["January","Febuary","March","April","May","June","July","August","September","October","November","December"]
    return dateNow.getDate() + " " + months[dateNow.getMonth()]

}
function scanPlayers() {
    players = World.getAllPlayers()
    players.forEach(function(info) {
        playerCoords = [parseInt(info.x), parseInt(info.y), parseInt(info.z)]
        score = 0
        for (i=0;i<playerCoords.length;i++) {
            if (isBetween(playerCoords[i], corner1[i], corner2[i])) {
                score++
            }
        }
        if (score == 3) {
            if (isInList(info.name, config["safeList"]) == false && isInList(info.name, config["banList"]) == false) {
                ChatLib.say("/is ban " + info.name)
                World.playSound("entity.ender_dragon.growl",1,1)
                ChatLib.say("/w " + info.name + " Stay away from the minecarts!")
                config["banList"].push(info.name)
                newLogEntry(info.name)
                updateConfig()
            }
        }
    })
}
function s(message) {
    ChatLib.chat(message)
}

var corner1
var corner2
var banList
var safeList

register("command", function(arg, arg2) {
    //Set the first corner
    if (arg == "1") {
        config["corner1"] = getCoords()
        s("&aSuccessfully set corner 1 to " + config["corner1"].toString())
        updateConfig()
    }
    //Set the second corner
    else if (arg == "2") {
        config["corner2"] = getCoords()
        s("&aSuccessfully set corner 2 to " + config["corner2"].toString())
        updateConfig()
    }
    //Make players safe from being banned
    else if (arg == "safe") {
        config["safeList"].push(arg2)
        s("&aAdded &c" + arg2 + "&a to the safe list!")
        updateConfig()
    }
    //Unban people
    else if (arg == "unban") {
        if (isInList(arg2, config["banList"])) {
            config["banList"] = removeObject(arg2, config["banList"])
            ChatLib.say("/is unban " + arg2)
            s("&aSuccessfully pardoned &c" + arg2 + "&a!")
            updateConfig()
        }
        else {
            s("&cError: That player is not banned!")
        }
    }
    else if (arg == "help") {
        s("&7/isban 1 &8- Set first corner")
        s("&7/isban 2 &8- Set second corner")
        s("&7/isban safe <player> &8- Make someone immune to getting banned")
        s("&7/isban unban <player> &8- Unban someone")
    }
}).setName("isban")

register("tick", function(x) {
    scanPlayers()
})

loadConfig()