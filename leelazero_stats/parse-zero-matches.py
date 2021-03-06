#!/usr/bin/python

import datetime
import os
import sys
import time
import glob
import re
import urllib
from bs4 import BeautifulSoup

best_networks = {}

fh = urllib.urlopen("http://zero.sjeng.org")
#fh = open("index.html")
soup = BeautifulSoup(fh.read(), "html.parser")
for table in soup.find_all(lambda tag: tag.name == "table" and "networks-table" in tag["class"]):
    for row in table.find_all("tr"):
        data = row.find_all("td")
        if not data: continue
        num, date, network, games, prior_games = data
        games = int(games.string)
        prior_games = int(prior_games.string)
        best_networks[network.string] = {}
        best_networks[network.string]["prior_games"] = prior_games
        best_networks[network.string]["date"] = date.string

for table in soup.find_all(lambda tag: tag.name == "table" and "matches-table" in tag["class"]):
    for row in table.find_all("tr"):
        data = row.find_all("td")
        if not data: continue
        date, networks, record, games, sprt = data
        net_elements = networks.find_all()
        next_net = net_elements[1]
        prev_net = net_elements[5]
        wins, losses = re.search("(\d+) : (\d+)", record.contents[0]).groups()
        wins = int(wins)
        losses = int(losses)
        if next_net.string in best_networks:
            best_networks[next_net.string]["prev_net"] = prev_net.string
            best_networks[next_net.string]["wins"] = wins
            best_networks[next_net.string]["losses"] = losses

for k in sorted(best_networks.keys(), key=lambda x: (best_networks[x]["prior_games"], best_networks[x]["date"])):
    v = best_networks[k]
    if "wins" in v:
        items = [k, "6", "128", "", v["prior_games"], v["wins"], v["losses"]] + [""]*7 + [v["date"]]
        print ", ".join(map(str, items))
            


