from bs4 import BeautifulSoup
import requests
import re
import json
from playerURLTest import playerDetails
import time
from alive_progress import alive_bar

url = "https://www.pro-football-reference.com/years/2023/passing.htm"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
tbody = doc.tbody
thead = doc.thead
header = thead.contents
tables = tbody.contents
x = 0
del tables[1::2]
heads = []

for i in range(len(tables)):
    if tables[i] == tbody.find(class_ = "thead"):
        heads.append(i)

for i in range(len(heads)):
    tables.pop(heads[i] - x)
    x = x+1
   
stats = []
detailsList = []
playerLinks = {}


with alive_bar(len(tables)) as bar:
    for table in tables:
        name = table.find(attrs={"data-stat": "player"})
        yds = table.find(attrs={"data-stat": "pass_yds"})
        tds = table.find(attrs={"data-stat": "pass_td"})
        ints = table.find(attrs={"data-stat": "pass_int"})
        ypg = table.find(attrs={"data-stat": "pass_yds_per_g"})
        comp = table.find(attrs={"data-stat": "pass_cmp_perc"})
        record = table.find(attrs={"data-stat": "qb_rec"})
        
        playerName = name.a.string
        playerYds = yds.string
        playerTDs = float(tds.string)
        playerINTs = float(ints.string)
        
        if playerINTs > 0:
            tdIntRatio = playerTDs / playerINTs
        else:
            tdIntRatio = playerTDs
        
        playerYPG = float(ypg.string)
        playerCOMP = float(comp.string)
        playerRecord = record.string

        if playerRecord == None:
            playerRecord = "0-0-0"

        playerRecord = playerRecord.split("-")
        playerWs = float(playerRecord[0])
        playerLs = float(playerRecord[1])

        if playerLs > 0:
            winPercentage = playerWs / playerLs
        else:
            winPercentage = playerWs
        
        myStat = round(tdIntRatio * playerYPG * winPercentage, 1)

        stats.append({"Name": playerName, "Ultra Stat": myStat})

        for a in name.find_all('a', href=True):
            playerLink = 'https://www.pro-football-reference.com' + a['href']
            playerLinks.update({playerName: playerLink})
            
        playerDetails(playerLink, detailsList)
        
        time.sleep(60)
        bar()

print(playerDetails)

with open("qbStats.json", "w") as l:
    json.dump(stats, l, indent=4)