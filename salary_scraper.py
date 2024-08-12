from bs4 import BeautifulSoup
import requests
import json

url = "https://overthecap.com/position/quarterback/2023"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
tbody = doc.tbody
tables = tbody.contents
capHits = []


for table in tables:
    name = table.contents[0]
    capHit = table.contents[2]
    playerName = name.a.string
    playerCapHit = capHit.string
    playerCapHit = playerCapHit.replace("$", "")
    playerCapHit = playerCapHit.replace(",", "")
    if playerName == "Matt Stafford":
        playerName = "Matthew Stafford"
    capHits.append({"Name": playerName, "Cap Hit": float(playerCapHit)})
    print(playerName)

print(capHits)
with open("qbCapHit.json", "w") as l:
    json.dump(capHits, l, indent=4)