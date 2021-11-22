#!/usr/bin/env python3
import requests

def getMatchList(puuid, APIKey):

    URL = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=1&api_key=" + APIKey
    # A count-nál az érték a kidobott matchID-k számát befolyásolja (start 0-ról)

    response = requests.get(URL)

    return response.json()