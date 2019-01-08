import requests
import datetime
import re
from time import sleep
from bs4 import BeautifulSoup
from myconfig import *

headers = {
        'User-Agent' : MY_NAME,
        'From' : MY_EMAIL}

def getBoxScoresLinks(soup):
    table = soup.findChildren('table')[0]
    schedule_table = table.find('tbody')
    rows = schedule_table.find_all('tr')
    box_scores_links = []
    for row in rows:
        #print(row.prettify())
        link = row.find(class_='center ').find('a')['href']
        box_scores_links.append(link)

    return box_scores_links

def getBasicStats(link,games):
    score_page = requests.get(BASEURL+link)
    score_soup = BeautifulSoup(score_page.text, 'html.parser')

    tables = score_soup.findChildren('table')
    away_basic_table = tables[0]
    home_basic_table = tables[2]

    headings = score_soup.find_all(class_='section_anchor')
    away_team = headings[3]['data-label'].split('(')[0].rstrip()
    home_team = headings[5]['data-label'].split('(')[0].rstrip()

    foot = away_basic_table.find('tfoot')
    stat_row = foot.find_all(class_='right ')
    away_stats = {x['data-stat'] : x.getText() for x in stat_row}
    away_stats['home'] = False

    foot = home_basic_table.find('tfoot')
    stat_row = foot.find_all(class_='right ')
    home_stats = {x['data-stat'] : x.getText() for x in stat_row}
    home_stats['home'] = True

    title = score_soup.title.getText().split('|')[0].rstrip().split(' Box Score')
    title2 = title[0] + title[1]

    game = { title2 : {home_team : home_stats, away_team : away_stats}}

    games.append(game)


CURRENTMONTH = datetime.datetime.now().strftime('%B')

BASEURL = 'https://www.basketball-reference.com'
SCHEDULEURL = 'https://www.basketball-reference.com/leagues/NBA_2019_games.html'


#Collect and parse first page of schedule, should be october
page = requests.get(SCHEDULEURL)
soup = BeautifulSoup(page.text, 'html.parser')


box_scores_links = getBoxScoresLinks(soup)
#print(box_scores_links)
list_of_games = []

getBasicStats(box_scores_links[0],list_of_games)
print(list_of_games)







#Contains links to schedule of games for each month, let's pull links to each month


"""monthList = soup.find(class_='filter')
monthListItems = monthList.find_all('a')
for month in monthListItems:
    newPage = requests.get(BASEURL + month['href'])
    newSoup = BeautifulSoup(page.text, 'html.parser')
    print(soup)
    sleep(2) #just to stagger the requests"""
