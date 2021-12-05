#!/usr/bin/env python3
import requests

def getChampionData(summonerId, APIKey):
    region = "eun1"
    URL = "https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + summonerId + "?api_key=" + APIKey
    response = requests.get(URL)

    return response.json()