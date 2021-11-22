#!/usr/bin/env python3
import requests

def getLastMatch(matchid, APIKey):
    URL = "https://europe.api.riotgames.com/lol/match/v5/matches/" + matchid + "?api_key=" + APIKey

    response = requests.get(URL)

    return response.json()