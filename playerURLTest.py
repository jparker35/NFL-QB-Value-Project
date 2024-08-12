from bs4 import BeautifulSoup
import requests
import json
from alive_progress import alive_bar

testList = []

def playerDetails(url, userList):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    details = {}

    name = doc.find('h1')
    playerName = name.span.text
    details.update({'Name': playerName})

    for a in doc.find_all(itemscope = 'image', src=True):
        picture = a['src']
        details.update({'Picture': picture})

    position = doc.find("strong", string = "Position").next_sibling
    position = position.replace(':', '')
    position = position.replace(' ', '')
    position = position.replace('\n', ' ').replace('\r', '').strip()
    details.update({"Position": position})

    throws = doc.find("strong", string = "Throws:").next_sibling
    throws = throws.strip()
    details.update({"Throws": throws})

    htwt = str(doc.find_all('p')[2].text).split('\xa0')
    details.update({"Height and Weight": htwt[0] + " " + htwt[1]})

    if doc.find("strong", string = "Team") != None:
        team = doc.find("strong", string = "Team").next_sibling.next_sibling
        team = team.text
    else:
        team = "Free Agent"
    details.update({"Current Team": team})

    college = doc.find("strong", string = "College").next_sibling.next_sibling
    college = college.text 
    details.update({"College": college})

    highSchoolName = doc.find("strong", string = "High School").next_sibling.next_sibling
    highSchoolName = highSchoolName.text 
    highSchoolState = doc.find("strong", string = "High School").next_sibling.next_sibling.next_sibling.next_sibling
    highSchoolState = highSchoolState.text
    highSchool = highSchoolName + ", " + highSchoolState
    details.update({"High School": highSchool})

    if doc.find("strong", string = "Draft") != None:
        draftTeam = doc.find("strong", string = "Draft").next_sibling.next_sibling
        draftPosition = draftTeam.next_sibling
        draftYear = draftPosition.next_sibling.text.split()[0]
        draftPosition = draftPosition.text.strip().split()
        draftRound = draftPosition[2].replace('st', '').replace('rd', '').replace('th', '').replace('nd', '')
        draftPick = int(draftPosition[4].replace('(', '').replace('st', '').replace('th', '').replace('rd', '').replace('nd',''))
        details.update({"Drafted": draftYear + (': ') +  "Round " + draftRound})
        details.update({"Pick Number": draftPick})
    else:
        draftPosition = "Undrafted"
        details.update({"Drafted": draftPosition})
        details.update({"Pick Number": 258})

    if position == "QB" and playerName != "Taysom Hill" and playerName != "Logan Woodside" and playerName != "Sean Clifford":
        qbRecord = doc.find(attrs= {"data-tip": "Team record in games started by this QB (regular season)"}).next_sibling.nextSibling.nextSibling.text
        if qbRecord != '':
            carrerW = float(qbRecord.split('-')[0])
            carrerL = float(qbRecord.split('-')[1])
            if carrerL != 0:
                carrerWinPercent = carrerW / carrerL
            else:
                carrerWinPercent = carrerW
        else:
            carrerWinPercent = 0

        gamesPlayed = float(doc.find(attrs= {"data-tip": "Games played"}).next_sibling.nextSibling.nextSibling.text)
        totalYards = float(doc.find(attrs= {"data-tip": "Yards Gained by Passing<br>For teams, sack yardage is deducted from this total"}).next_sibling.nextSibling.nextSibling.text)
        carrerYPG = round(totalYards / gamesPlayed, 1)

        carrerTds = float(doc.find(attrs= {"data-tip": "Passing Touchdowns"}).next_sibling.nextSibling.nextSibling.text)
        carrerInts = float(doc.find(attrs= {"data-tip": "Interceptions thrown"}).next_sibling.nextSibling.nextSibling.text)
        if carrerInts != 0:
            tdIntRatio = round(carrerTds / carrerInts, 1)
        else:
            tdIntRatio = 0

        carrerUltra = round(tdIntRatio * carrerYPG * carrerWinPercent, 1)

        details.update({'Carrer Ultra Stat': carrerUltra})
    else:
        details.update({'Carrer Ultra Stat': "Not a QB"})

    userList.append(details)

    with open("qbDetails.json", "w") as l:
        json.dump(userList, l, indent=4)
    