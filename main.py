import kivy
import json
import os
import platform
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

import ChampionMasteryDTO
import LastMatch
import MatchList
import SummonerDTO


class StartWindow(Screen):
    pass

class SummonerWindow(Screen):
    pass

class MatchWindow(Screen):
    pass

class ManageWindow(ScreenManager):
    pass

class StartLayout(FloatLayout):
    def try_summoner(self, sumname, apikey):
        response = SummonerDTO.getSummonerData(sumname, apikey)
        self.is_summoner = True
        try:
            tmp = response['id']
        except KeyError:
            self.is_summoner = False
            print(response)
            self.ids.loading_label.text = ("Error: " + str(response['status']['status_code'])
                + ' ' + response['status']['message'])

class MyGridLayout(GridLayout):
    def get_summonerpage(self, sumname, apikey):
        print(platform.system())
        if platform.system() == "Linux":
            slash = '/'
        elif platform.system() == "Windows":
            slash = '\\'

        self.cwd = os.getcwd()
        
        f = open('champion.json')
        championData = json.load(f)
        f.close()
        championNames = list(championData['data'])
        self.summonerName = sumname
        self.APIKey = apikey
        response = SummonerDTO.getSummonerData(self.summonerName, self.APIKey)
        self.summonerId = response['id']
        self.profileIconId = response['profileIconId']
        self.puuid = response['puuid']
        self.level = response['summonerLevel']
        response = ChampionMasteryDTO.getChampionData(self.summonerId, self.APIKey)
        self.championId = [0, 0, 0]
        self.championPoints = [0, 0, 0]
        for i in range(3):
            self.championId[i] = response[i]['championId']
            self.championPoints[i] = response[i]['championPoints']
            for j in range(len(championNames)):
                if str(championData['data'][championNames[j]]['key']) == str(self.championId[i]):
                    self.championId[i] = championNames[j]
                    

        self.championPortrait = [0, 0, 0, 0, 0]
        self.kills = [0, 0, 0, 0, 0]
        self.assists = [0, 0, 0, 0, 0]
        self.deaths = [0, 0, 0, 0, 0]
        self.cs = [0, 0, 0, 0, 0]
        self.win = [0, 0, 0, 0, 0]
        self.matchIds = MatchList.getMatchList(self.puuid, self.APIKey)
        for i in range(5):
            response = LastMatch.getLastMatch(self.matchIds[i], self.APIKey)
            for j in range(len(response['info']['participants'])):
                if response['info']['participants'][j]['summonerName'].lower() == self.summonerName.lower():
                    if response['info']['participants'][j]['championName'] == "FiddleSticks":
                        self.championPortrait[i] = "Fiddlesticks"
                    else:
                        self.championPortrait[i] = response['info']['participants'][j]['championName']
                    self.kills[i] = response['info']['participants'][j]['kills']
                    self.assists[i] = response['info']['participants'][j]['assists']
                    self.deaths[i] = response['info']['participants'][j]['deaths']
                    self.cs[i] = response['info']['participants'][j]['totalMinionsKilled']
                    self.win[i] = response['info']['participants'][j]['win']
                    if self.win[i] == True:
                        self.win[i] = '           Win'
                    else:
                        self.win[i] = '           Lose'

        self.ids.summ_icon.source = source = str(self.cwd) + slash + 'profileicon' + slash +str(self.profileIconId) + '.png'
        self.ids.summ_name.text = str(self.summonerName)
        self.ids.summ_level.text = 'Level ' + str(self.level)
        self.ids.champ_mastery1P.source = str(self.cwd) + slash + 'champion' + slash +str(self.championId[0]) + '.png'
        self.ids.champ_mastery1.text = str(self.championPoints[0])
        self.ids.champ_mastery2P.source = str(self.cwd) + slash + 'champion' + slash +str(self.championId[1]) + '.png'
        self.ids.champ_mastery2.text = str(self.championPoints[1])
        self.ids.champ_mastery3P.source = str(self.cwd) + slash + 'champion' + slash +str(self.championId[2]) + '.png'
        self.ids.champ_mastery3.text = str(self.championPoints[2])
        self.ids.match0p.source = str(self.cwd) + slash + 'champion' + slash  + str(self.championPortrait[0]) + '.png'
        self.ids.match0kda.text = str(self.kills[0]) +"/"+ str(self.deaths[0])+"/"+str(self.assists[0]) + " - "+str(self.cs[0]) + " cs " + str(self.win[0])
        self.ids.match1p.source = str(self.cwd) + slash + 'champion' + slash  + str(self.championPortrait[1]) + '.png'
        self.ids.match1kda.text = str(self.kills[1])+"/"+str(self.deaths[1])+"/"+str(self.assists[1]) + " - "+str(self.cs[1]) + " cs " + str(self.win[1])
        self.ids.match2p.source = str(self.cwd) + slash + 'champion' + slash  + str(self.championPortrait[2]) + '.png'
        self.ids.match2kda.text = str(self.kills[2])+"/"+str(self.deaths[2])+"/"+str(self.assists[2]) + " - "+str(self.cs[2]) + " cs " + str(self.win[2])
        self.ids.match3p.source = str(self.cwd) + slash + 'champion' + slash  + str(self.championPortrait[3]) + '.png'
        self.ids.match3kda.text = str(self.kills[3])+"/"+str(self.deaths[3])+"/"+str(self.assists[3]) + " - "+str(self.cs[3]) + " cs " + str(self.win[3])
        self.ids.match4p.source = str(self.cwd) + slash + 'champion' + slash  + str(self.championPortrait[4]) + '.png'
        self.ids.match4kda.text = str(self.kills[4])+"/"+str(self.deaths[4])+"/"+str(self.assists[4]) + " - "+str(self.cs[4]) + " cs " + str(self.win[4])


class LoLScoreboardApp(App):
    pass



if __name__ == "__main__":
    LoLScoreboardApp().run()
