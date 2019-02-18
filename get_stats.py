import requests
from requests.compat import urljoin
import os
import datetime
import re
import json
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from myconfig import *

headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'From' : MY_EMAIL}

def getBoxScoresLinks(soup):
    table = soup.findChildren('table')[0]
    schedule_table = table.find('tbody')
    rows = schedule_table.find_all('tr')
    box_scores_links = []
    for row in rows:
        #print(row.prettify())
        try:
            link = row.find(class_='center ').find('a')['href']
            box_scores_links.append(link)
        except AttributeError:
            pass

    return box_scores_links

def ripStatsFromTable(table,home_bool):
    foot = table.find('tfoot')
    stat_row = foot.find_all(class_='right ')
    stats = {x['data-stat'] : x.getText() for x in stat_row}
    stats['home'] = home_bool

    return stats

def getStats(link,games):
    score_page = requests.get(BASEURL+link)
    score_soup = BeautifulSoup(score_page.text, 'html.parser')

    #Team names
    headings = score_soup.find_all(class_='section_anchor')
    away_team = headings[3]['data-label'].split('(')[0].rstrip()
    home_team = headings[5]['data-label'].split('(')[0].rstrip()

    tables = score_soup.findChildren('table')
    #Basic stats
    away_basic_table = tables[0]
    home_basic_table = tables[2]
    away_basic_stats = ripStatsFromTable(away_basic_table,False)
    home_basic_stats = ripStatsFromTable(home_basic_table,True)

    #'Advanced' stats
    away_adv_table = tables[1]
    home_adv_table = tables[3]
    away_adv_stats = ripStatsFromTable(away_adv_table,False)
    home_adv_stats = ripStatsFromTable(home_adv_table,True)

    #combine both sets of stats into one dictionary
    home_stats = {**home_adv_stats, **home_basic_stats}
    away_stats = {**away_adv_stats, **away_basic_stats}
    title = score_soup.title.getText().split('|')[0].rstrip().split(' Box Score')
    title2 = title[0] + title[1]

    game = { title2 : {home_team : home_stats, away_team : away_stats}}

    games.append(game)



CURRENTMONTH = datetime.datetime.now().strftime('%B')

BASEURL = 'https://www.basketball-reference.com'
SCHEDULEURL = 'https://www.basketball-reference.com/leagues/NBA_2019_games-october.html'

s = requests.Session()

#Collect and parse first page of schedule, should be october
page = requests.get(SCHEDULEURL)
soup = BeautifulSoup(page.text, 'html.parser')

box_scores_links = getBoxScoresLinks(soup)

list_of_games = []

def getAllGames(list_of_games,soup):
    monthList = soup.find(class_='filter')
    monthListItems = monthList.find_all('a')
    monthList = [monthListItems[i]['href'] for i in range(len(monthListItems))]
    print(monthList)

    for i in monthList:
        page = s.get(BASEURL+i)
        soup = BeautifulSoup(page.text, 'html.parser')
        current = soup.find(class_='filter').find(class_='current').getText()
        print(current)

        box_scores_links = getBoxScoresLinks(soup)
        for i in box_scores_links:
            print(i)
            getStats(i,list_of_games)
            sleep(2)

        if (current == CURRENTMONTH):
            break

        sleep(2)


#content > div.filter > div.current
#getStats(box_scores_links[0],list_of_games)
#for i,j in enumerate(list_of_games):
#    print(j)

#print(pd.DataFrame.from_dict(list_of_games).to_string())


    with open('data.json', 'w') as file:
        json.dump(list_of_games, file)

#Get games only after last one in data file
def update(soup):
    with open('data.json') as file:
        games = json.loads(file.read())
    last_game = str(games[-1].keys()).split("'")[1]
    #print("Last Game:", last_game)
    month_of_last_game = last_game.split(',')[1].split(' ')[1].lower()
    #print("Month of last game:", month_of_last_game)

    monthList = soup.find(class_='filter')
    monthListItems = monthList.find_all('a')
    monthList = [monthListItems[i]['href'] for i in range(len(monthListItems))]

    while (month_of_last_game not in monthList[0]):
        monthList.pop(0)

    print(monthList)
    new_games = []

    for i in monthList:
        page = s.get(BASEURL+i)
        soup = BeautifulSoup(page.text, 'html.parser')
        current = soup.find(class_='filter').find(class_='current').getText()
        print(current)

        box_scores_links = getBoxScoresLinks(soup)
        for i in box_scores_links:
            print(i)
            getStats(i,new_games)
            sleep(2)

        if (current == CURRENTMONTH):
            break



    unique = [x for x in new_games if x not in games]
    for item in unique:
        games.append(item)


    with open('data.json', 'w') as file:
        json.dump(games, file)







    return


if (os.stat('data.json').st_size == 0):
    getAllGames(list_of_games,soup)
else:
    update(soup)
