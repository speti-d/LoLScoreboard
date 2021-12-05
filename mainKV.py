#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
import LastMatch
import MatchList
import SummonerDTO
import json
import requests


class MainApplication(Frame):

    def __init__(self, master):
        self.master = master
        ttk.Frame.__init__(self, self.master)
        self.api_var = StringVar()  # Sztringváltozó az apikulcs bekérésére
        self.id_var = StringVar()  # Sztringváltozó amiben a lekérendő felhasználó azonosítóját tartjuk
        self.id_label = ttk.Label(self)  # A címke amin a bemeneti doboz felett jelenítünk meg szöveget
        self.api_label = ttk.Label(self)  #
        self.id_entry = ttk.Entry(self)  # A bemeneti doboz amiben a felhasználó az azonosítóját adhatja meg
        self.api_entry = ttk.Entry(self)
        self.search_button = ttk.Button(self)  # A gomb aminek a megnyomásával lefut a keresés
        self.result_box = Text(self)  # Textbox amibe majd megy a megformázott meccsadat
        self.configure_gui()
        self.create_widgets()

    def get_matchdata(self, *args):
        summonerName = self.id_entry.get()
        APIKey = self.api_entry.get()
        responseJSON = SummonerDTO.getSummonerData(summonerName, APIKey)
        try:
            puuid = responseJSON['puuid']

            responseJSON2 = MatchList.getMatchList(puuid, APIKey)
            # ha a puuid egyezik a LastMatch.getLastMatch(lastid, APIKey)-ban találtal, highlight

            lastid = responseJSON2[0]

            responseJSON3 = LastMatch.getLastMatch(lastid, APIKey)

    championName = []
    kills = []
    assists = []
    deaths = []
    visionScore = []
    champID = []
    summonerSpell1ID = []
    summonerSpell2ID = []
    item0ID = []
    item1ID = []
    item2ID = []
    item3ID = []
    item4ID = []
    item5ID = []
    item6ID = []

    for i in range(0, len(responseJSON3['info']['participants'])):
        championName.append(responseJSON3['info']['participants'][i]['championName'])
        kills.append(responseJSON3['info']['participants'][i]['kills'])
        assists.append(responseJSON3['info']['participants'][i]['assists'])
        deaths.append(responseJSON3['info']['participants'][i]['deaths'])
        visionScore.append(responseJSON3['info']['participants'][i]['visionScore'])
        champID.append(responseJSON3['info']['participants'][i]['championId'])
        summonerSpell1ID.append(responseJSON3['info']['participants'][i]["summoner1Id"])
        summonerSpell2ID.append(responseJSON3['info']['participants'][i]["summoner2Id"])
        item0ID.append(responseJSON3['info']['participants'][i]["item0"])
        item1ID.append(responseJSON3['info']['participants'][i]["item1"])
        item2ID.append(responseJSON3['info']['participants'][i]["item2"])
        item3ID.append(responseJSON3['info']['participants'][i]["item3"])
        item4ID.append(responseJSON3['info']['participants'][i]["item4"])
        item5ID.append(responseJSON3['info']['participants'][i]["item5"])
        item6ID.append(responseJSON3['info']['participants'][i]["item6"])


            output = "{0:13} {1:^8} {2:>17}".format("Name", "K |D |A ", "Vision") + "\n"
            for i in range(0, 10):
                kda = "{0:>2}|{1:>2}|{2:>2}".format(str(kills[i]), str(deaths[i]), str(assists[i]))
                output = output + "{0:13} {1:^8} {2:>17}".format(championName[i], kda, visionScore[i]) + "\n"
            self.result_box.configure(state='normal')
            self.result_box.delete('1.0', END)  # Kitörlöm a doboz korábbi tartalmát
            self.result_box.insert('1.0', output)  # Beszúrom az új tartalmat
            self.result_box.configure(state='disable')
        except:
            pass

    def configure_gui(self):  # Ebben a metódusban adjuk meg, hogyan nézzenek ki a widgeteink
        # Ablakon beluli widgetek:
        self.master.title('JGtimer')
        self.id_label.configure(text='Username:')
        self.api_label.configure(text='Api key:')
        self.id_entry.configure(textvariable=self.id_var)
        self.api_entry.configure(textvariable=self.api_var, show='*')
        self.search_button.configure(text='Search...', command=self.get_matchdata)
        self.result_box.configure(height=11, width=40, state='disable')
        #
        self.id_entry.bind("<Return>", self.get_matchdata)
        self.api_entry.bind("<Return>", self.get_matchdata)
        #
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.resizable(0, 0)
        # Ez a két sor kell ahhoz, hogy az ablak méretét lehessen dinamikusan változtatni
        # Ha azt végül nem akarjuk akkor nem kell
        for col in range(0, 4):
            self.columnconfigure(col, weight=1)
        for row in range(0, 4):
            self.rowconfigure(row, weight=1)
        self.rowconfigure(4, weight=2)
        # Súlyokat oszt a soroknak és oszlopoknak, még nem jó majd játsz vele nyugodtan
        # -Peti

    def create_widgets(self):  # Ez a metódus tölti be őket a megfelelő helyre a gridben
        self.grid(padx=5, pady=5, sticky=(N, W, E, S))
        # USERNAME:
        self.id_label.grid(row=2, column=0, sticky=W)  # A "Username:" labelt balra igazitja, a 0/0-as cellaban
        self.id_entry.grid(row=3, column=0, sticky=(W, E))  # A bemeneti box-ot átméretezi hogy a 1/0-as cellát kitöltse
        # API KEY
        self.api_entry.grid(row=1, column=0, sticky=(W, E))
        self.api_label.grid(row=0, column=0, sticky=W)
        # SEARCH BUTTON
        self.search_button.grid(row=3, column=1)  # A Kereső gombot odaragasztja az 1/1-es cella bal oldalára
        # RESULT BOX
        self.result_box.grid(row=4, column=0, columnspan=2, sticky=(N, W, E, S), pady=(5, 0))
        # TODO:
        # - A result boxnak kéne kitalálni valami fix méretet, hogy köré igazítsam a dolgokat


if __name__ == '__main__':
    root = Tk()
    main_app = MainApplication(root)
    root.mainloop()
