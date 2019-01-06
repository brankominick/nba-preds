import requests
import datetime
import re
from time import sleep
from bs4 import BeautifulSoup
from myconfig import *

headers = {
        'User-Agent' : MY_NAME,
        'From' : MY_EMAIL}

curMonth = datetime.datetime.now().strftime('%B')

baseURL = 'https://www.basketball-reference.com'
scheduleURL = 'https://www.basketball-reference.com/leagues/NBA_2019_games.html'


#Collect and parse first page of schedule, should be october
page = requests.get(scheduleURL)
soup = BeautifulSoup(page.text, 'html.parser')


table = soup.findChildren('table')[0]
scheduleTable = table.find('tbody')
rows = scheduleTable.find_all('tr')
boxScoresLinks = []
for row in rows:
    #print(row.prettify())
    link = row.find(class_='center ').find('a')['href']
    boxScoresLinks.append(link)

print(boxScoresLinks)
page = requests.get(baseURL+boxScoresLinks[0])
soup = BeautifulSoup(page.text, 'html.parser')
print(soup.title)
#print(scheduleTable)
#boxScores = scheduleTable.find_all()
#boxScores = scheduleTable.find_all(href=re.compile('boxscores'))
#print(boxScores)
#for link in boxScores:
#    print(link['href'])




#Contains links to schedule of games for each month, let's pull links to each month


"""monthList = soup.find(class_='filter')
monthListItems = monthList.find_all('a')
for month in monthListItems:
    newPage = requests.get(baseURL + month['href'])
    newSoup = BeautifulSoup(page.text, 'html.parser')
    print(soup)
    sleep(2) #just to stagger the requests"""
