//Get current time as 01:02:03
function get24hTime() {
    let dateNow = new Date()
    let x = [dateNow.getHours(), dateNow.getMinutes(), dateNow.getSeconds()]
    //Turn 4:38:3 into 04:38:30
    for (i=0;i<x.length;i++) {
        if (x[i].toString().length == 1) { x[i] = "0" + x[i]}
    }
    return x[0] + ":" + x[1] + ":" + x[2]
}

//Save the ChatLog to a text file in the format "PlayerName-ServerIP-YY/MM/DD.txt" in the file ".minecraft/ChatLogs"
register("chat", message => {
	let x = new Date()
    let fileName = `${Player.getName()}-${Server.getIP()}-${x.getFullYear()}-${(x.getMonth()+1)}-${x.getDate()}.txt`
    let timeStamp = `[${get24hTime()}]`
    try {
        FileLib.append(`./ChatLogs/${fileName}`, `${timeStamp} ${ChatLib.removeFormatting(message)}\n`)
    }
    catch(error) {
        const File = Java.type("java.io.File")
        let f = new File("ChatLogs","./")
        f.mkdirs()
        FileLib.append(`./ChatLogs/${fileName}`, `${timeStamp} ${ChatLib.removeFormatting(message)}\n`)
    }
}).setCriteria("${message}")