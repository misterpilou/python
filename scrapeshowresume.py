from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
from db import conshowtime
import re
from datetime import datetime
conn = conshowtime()
cur=conn.cursor()
cur.execute("USE ShowTime")

def scraperesume(url, shownum) :
    html = urlopen("http://en.wikipedia.org" + "/wiki/" + url)
    bsObj = BeautifulSoup(html, "html.parser")
    listep = bsObj.find("table", {"class": "wikitable plainrowheaders wikiepisodetable"}).findAll("tr", {"class": "vevent"})
    listres = bsObj.find("table", {"class": "wikitable plainrowheaders wikiepisodetable"}).findAll("td", {"class": "description"})
    listeep = listep[shownum-1]
    print (listeep)
    liste = listeep.findAll("td")
    ez = str(liste[0]).strip("<td></td>")
    if(int(ez)==shownum) :
        numoverall=listeep.find("th").get_text()
        numoverall = int(numoverall)
        numinseason=int(ez)
        titleep=liste[1].get_text().strip("\"")
        directedby=liste[2].get_text().strip("\"")
        writtenby=liste[3].get_text().strip("\"")
        reldate = liste[4].find("span", {"class": "bday dtstart published updated"})
        reldate = reldate.get_text()
        resume = listres[shownum-1].get_text().strip("\"")
        print(resume)
        cur.execute("INSERT INTO resume(num_overall, num_in_season, title, directed_by, written_by, release_date, resume) VALUES (%s, %s, %s, %s, %s, %s, %s)", (int(numoverall), int(numinseason), titleep, directedby, writtenby, reldate, resume))
        conn.commit()

#<td>3</td>


showname = input("Selectionnez le nom de la série : ")
showseason = input("Entrez quelle saison ? : ")
shownumber = input("Selectionnez le numero de l'episode : ")
show1 = showname.title()
show2 = show1.replace(" ", "_")
show3 = showseason.replace(showseason, "_(season_"+ showseason +")")
urlshow = show2+show3
show4 = int(shownumber)
scraperesume(urlshow, show4)
print(show2+show3)
cur.close()
conn.close()