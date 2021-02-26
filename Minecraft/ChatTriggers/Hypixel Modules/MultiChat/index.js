
//Simulate: &2Guild > &6[MVP&0++&6] UnclaimedBloom6&r: NERD

var chatMessagesFile = "./config/ChatTriggers/modules/MultiChat/ChatMessages.txt"
var commandsFile = "./config/ChatTriggers/modules/MultiChat/Commands.txt"
var configFile = "./config/ChatTriggers/modules/MultiChat/settings.json"

class Settings {
    mainAccount = ""
    altAccount = ""
    multiChatMode = false
}

//Easier than doing ChatLib.chat(message). Deugging Convenience.
function s(message) {
    ChatLib.chat(message)
}

function loadConfig() {
    let configDefault = JSON.stringify({
        "mainAccount":"",
        "altAccount":"",
        "multiChatMode":false,
        "guildName":""
    })
    try {
        config = JSON.parse(FileLib.read(configFile))
        if (config == null) {
            FileLib.write(configFile, configDefault)
            config = JSON.parse(FileLib.read(configFile))
        }
        Settings.mainAccount = config.mainAccount
        Settings.altAccount = config.altAccount
        Settings.multiChatMode = config.multiChatMode
        Settings.guildName = config.guildName
    }
    catch(error) {
        s("No info in config file, exists")
        FileLib.write(configFile, configDefault)
    }
}

function updateConfig(setting, value) {
    let newConfig = JSON.parse(FileLib.read(configFile))
    newConfig[setting] = value
    newConfig = JSON.stringify(newConfig)
    FileLib.write(configFile, newConfig)
    loadConfig()
}

function clearFiles() {
    FileLib.write(chatMessagesFile, "")
    FileLib.write(commandsFile, "")
}

//STARTING THE MOD UP or /ct load

//Clear files to prevent buildup and subsequent spam upon loading
clearFiles()
//Load the config
loadConfig()

//Detect chat for a guild message
register("chat", (gchat, player, message) => {
    if (Player.getName() == Settings.altAccount) {
        if (Settings.guildName == "") {
            var chatMessage = `${gchat} > ${player}: ${message}\n`
        }
        else {
            var chatMessage = `&2${Settings.guildName} > ${player}: ${message}`
        }
        FileLib.append(chatMessagesFile, chatMessage)
    }
}).setChatCriteria("${gchat} > ${player}: ${message}")

register("tick", (e) => {
    if (Player.getName() == Settings.mainAccount) {
        text = FileLib.read(chatMessagesFile)
        if (text == "") {}
        else {
            s(text)
            FileLib.write(chatMessagesFile, "")
        }
    }
    if (Player.getName() == Settings.altAccount) {
        commands = FileLib.read(commandsFile)
        if (commands == "") {}
        else {
            ChatLib.say(commands)
            FileLib.write(commandsFile, "")
        }
    }
})

register("command", (...message) => {
    if (message == undefined) {
        if (Settings.multiChatMode == false) {
            updateConfig("multiChatMode", true)
            s("&aYou are now in the &6MULTICHAT &achannel")
            return
        }
        else {
            updateConfig("multiChatMode", false)
            s("&aYou have exited the &6MULTICHAT &achannel")
            return
        }
    }
    if (message[0] == "main") {
        Settings.mainAccount = message[1]
        s(`&0[&6MultiChat&0] &aChanged main account to &6${Settings.mainAccount}&a!`)
        s(`&0[&6MultiChat&0] &cNote: Your other account will require a &7/ct load &c for this to be taken into effect.`)
        updateConfig("mainAccount", Settings.mainAccount)
        return
    }
    else if (message[0] == "alt") {
        Settings.altAccount = message[1]
        s(`&0[&6MultiChat&0] &aChanged alt account to &6${Settings.altAccount}&a!`)
        s(`&0[&6MultiChat&0] &cNote: Your other account will require a &7/ct load &c for this to be taken into effect.`)
        updateConfig("altAccount", Settings.altAccount)
        return
    }
    else if (message[0] == "guild") {
        Settings.guildName = message[1]
        s(`&0[&6MultiChat&0] &aChanged guild name to &6${Settings.guildName}&a!`)
        updateConfig("guildName", Settings.guildName)
        return
    }
    else if (message[0] == "help") {
        helpListContents = [
            "",
            "&0----- [&6MultiChat&0] -----",
            "",
            "&8/mc &7- Toggles Multi Chat Mode",
            "&8/mc help &7- Shows this menu",
            "&8/mc main <player> &7- Sets your main accounts name",
            "&8/mc alt <player> &7- Sets your alt accounts name",
            "&8/mc <message> &7- Send a message or command",
            "&7from your main to your alt like a regular message",
            "",
            "&8/boop UnclaimedBloom6 &7- For cool people",
            ""
        ]
        helpListContents.forEach(msg => {
            s(ChatLib.getCenteredText(msg))
        })
        return
    }
    else {
        message = message.join(" ")
        s(`&aSending &6${message} &ato ${Settings.altAccount}`)
        FileLib.write(commandsFile, message)
    }
}).setName("mc")

//Send anything (Except commands) from your main account to the alt account.
register("messageSent", (message, event) => {
    //If multichat is enabled
    if (Settings.multiChatMode == true) {
        //If main types a command then don't forward that message
        var isCommand = message.startsWith("/")
        if (isCommand == true) { return }
        //Otherwise write to file
        else {
            if (Player.getName() == Settings.mainAccount) {
                FileLib.write(commandsFile, message)
                cancel(event)
            }
        }
    }
})
