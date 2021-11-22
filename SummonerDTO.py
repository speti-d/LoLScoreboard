#!/usr/bin/env python3
import requests

def getSummonerData(summonerName, APIKey):
    region = "eun1"
    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)

    return response.json()