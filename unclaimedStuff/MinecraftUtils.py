import requests
import json

def getPlayerName(uuid):
    """Gets a player's username via their UUID"""
    mojangInfo = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()
    playerName = mojangInfo["name"]
    return playerName
def getPlayerUUID(playerName):
    """Gets a player's UUID via their username"""
    mojangInfo = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{playerName}").json()
    uuid = mojangInfo["id"]
    return uuid
def validPlayer(playerName):
    """Returns False if the player doesn't exist, otherwise will return a list containing their playerName and UUID [playerName, UUID]."""
    try:
        mojangInfo = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{playerName}").json()
        playerName = mojangInfo["name"]
        uuid = mojangInfo["id"]
        return [playerName, uuid]
    except:
        return False
