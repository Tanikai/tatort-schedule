import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

# Global
cache_tatort = {}
switch_weekday_num = {
    0: "Montag",
    1: "Dienstag",
    2: "Mittwoch",
    3: "Donnerstag",
    4: "Freitag",
    5: "Samstag",
    6: "Sonntag"
}

switch_weekday_abr = {
    "So": "Sonntag",
    "Sa": "Samstag",
    "Fr": "Freitag",
    "Do": "Donnerstag",
    "Mi": "Mittwoch",
    "Di": "Dienstag",
    "Mo": "Montag"
}

def getTatort():
    global cache_tatort
    requesttime = datetime.now()
    requestdate = requesttime.date()

    # Wenn der Cache leer ist, wird die JSON-Datei geladen
    if cache_tatort == {}:
        print(">>>Cache ist leer.")
        with open("cache.json", "r") as jsoncache:
            print(">>>Cache aus JSON-Datei wird geladen.")
            cache_tatort = json.load(jsoncache)
            jsoncache.close()
            # Wenn die Informationen aus der JSON-Datei veraltet sind bzw. das Datum ungleich ist, wird die Website neu geparst
            try:
                if cache_tatort["date"] != requestdate.strftime("%Y-%m-%d"):
                    print(">>>Datum von Abfrage und Cache sind ungleich.")
                    return parseWebsite(requestdate)
                # Falls nicht, wird der Cache ausgegeben.
                else:
                    print(">>>Datum von Abfrage und Cache ist gleich. Cache wird ausgegeben.")
                    return cache_tatort["tatort"]
            
            except:
                print("Fehler beim lesen der JSON-Datei.")
                return parseWebsite(requestdate)

    # Wenn im Cache etwas drinsteht
    else:
        print(">>>Cache-Variable ist belegt.")
        # Wenn das Datum nicht gleich ist, soll die Website geparst werden
        if cache_tatort["date"] != requestdate.strftime("%Y-%m-%d"):
            print(">>>Datum von Abfrage und Cache sind ungleich.")
            return parseWebsite(requestdate)
        # Wenn das Datum gleich ist, kann der Cache zurückgegeben werden
        else:
            print(">>>Datum von Abfrage und Cache ist gleich. Cache wird ausgegeben.")
            return cache_tatort["tatort"]

def getTatortSonntag():
    tatortlist = getTatort()
    for episode in tatortlist:
        if episode["weekday"] == "Sonntag":
            return episode

def getAllTatortSonntag():
    tatortlist = getTatort()
    sonntaglist = []
    for episode in tatortlist:
        if episode["weekday"] == "Sonntag":
            sonntaglist.append(episode)
    return sonntaglist

def parseWebsite(requestdate):
    content = ""
    print("Tatort-Website wird geladen...")
    with urllib.request.urlopen("https://www.daserste.de/unterhaltung/krimi/tatort/vorschau/index.html") as response:
        content = response.read().decode("utf-8")
        #print(content)

    print("Tatort-Website wurde geladen.")
    soup = BeautifulSoup(content, "html.parser")
    tatort_htmllinklist = soup.find_all("div", class_="linklist")

    tatort_cleanhtmllinklist = tatort_htmllinklist[1]
    tatort_links = tatort_cleanhtmllinklist.find_all("a")

    tatortdict = []
    for tag in tatort_links:
        # x ist ein tatObject
        x = {}

        # Hinweis zu content:
        # In dieser Variable befinden sich der Text, der sich zwischen <a> und </a> befindet.
        content = str(tag.string)

        # Formatierung der Liste content_split:
        # [0]: Wochentag und Datum (Bsp.: "So, 21.06.") ODER "Heute" oder "Morgen"
        # [1]: Uhrzeit (Bsp.: "20:15 Uhr")
        # [2]: Titel, Kommissare und Stadt (Bsp.: "Letzte Tage (Blum und Perlmann (Konstanz))")
        content_split = content.split(" | ")

        if content_split[0] == "Heute":
            x["day"] = requestdate.day
            x["month"] = requestdate.month
            weekdaynum = requestdate.weekday()
            x["weekday"] = switch_weekday_num[weekdaynum]

        elif content_split[0] == "Morgen":
            tomorrow = requestdate + timedelta(days=1)
            x["day"] = tomorrow.day
            x["month"] = tomorrow.month
            weekdaynum = tomorrow.weekday()
            x["weekday"] = switch_weekday_num[weekdaynum]

        else:
            date = content_split[0].split(", ")
            date_split = date[1].split(".")
            x["day"] = date_split[0]
            x["month"] = date_split[1]
            x["weekday"] = switch_weekday_abr[date[0]]

        x["time"] = content_split[1]
        x["hour"] = content_split[1][0:2]
        x["minute"] = content_split[1][3:5]

        content_title = content_split[2]
        content_title = content_title[:content_title.find("(")-1]
        x["title"] = content_title

        content_bracket = content_split[2]
        content_bracket = content_bracket[content_bracket.find("(")+1:len(content_bracket)-1]

        content_city = content_bracket[content_bracket.rfind("(")+1:len(content_bracket)-1]
        x["city"] = content_city

        content_inspectors = content_bracket[:-len(content_city)-4] # Klammer*2, Leerzeichen, -1
        x["inspectors"] = content_inspectors

        x["link"] = "https://www.daserste.de" + str(tag["href"])
        tatortdict.append(x)
        print(x)

    with open("cache.json", "w") as jsoncache:
        print("Informationen werden gespeichert.")
        print(tatortdict)
        cache_tatort["date"] = requestdate.strftime("%Y-%m-%d")
        cache_tatort["tatort"] = tatortdict
        json.dump(cache_tatort, jsoncache, indent=4)
        jsoncache.close()
        print("-"*5)
        print(cache_tatort)
        
    return tatortdict

parseWebsite(datetime.now().date())