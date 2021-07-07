import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Global
TATORT_URL = "https://www.daserste.de/unterhaltung/krimi/tatort/vorschau/index.html"

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


def get_tatort():
    website = get_tatort_html()
    return parse_tatort_website(website)


def get_tatort_html() -> str:
    html_file = ""
    with urllib.request.urlopen(TATORT_URL) as response:
        html_file = response.read().decode("utf-8")
    return html_file


def parse_tatort_website(html: str):
    soup = BeautifulSoup(html, "html.parser")  # BSoup-Object for site parsing
    # 0:"nächste Erstausstrahlung" 1:"im Ersten" 2:"in den Dritten" 3:"auf ONE" 4:"Tatort in Ihrem dritten Programm"
    tatort_linklists = soup.find_all("div", class_="linklist")

    # Timestamp of website request is between </body> and </html> tag
    # </body><!-- stage-4.deo @ Sun Feb 07 09:16:08 CET 2021 --></html>
    comment = soup.html.contents[len(soup.html.contents)-2]
    at_index = comment.find("@")
    timestamp_text = comment[at_index+2:-1]
    # FIXME: Proper handling of Timezone
    request_timestamp = datetime.strptime( timestamp_text, "%a %b %d %H:%M:%S CEST %Y")

    tatort_im_ersten_list = tatort_linklists[1].find_all("a")
    return parse_schedule(tatort_im_ersten_list, request_timestamp)


def parse_schedule(schedule_list, request_timestamp):
    schedule = []
    for entry in schedule_list:
        schedule.append(parse_entry(entry, request_timestamp))
    return schedule


def parse_entry(schedule_entry, request_timestamp):
    entry = {}
    # Example for a link text:
    # So., 14.02. | 20:15 Uhr | Hetzjagd (Odenthal und Stern  (Ludwigshafen))

    # Formatierung der Liste content_split:
    # [0]: Wochentag und Datum (Bsp.: "So, 21.06.") ODER "Heute" oder "Morgen"
    # [1]: Uhrzeit (Bsp.: "20:15 Uhr")
    # [2]: Titel, Kommissare und Stadt (Bsp.: "Letzte Tage (Blum und Perlmann (Konstanz))")
    date_text = time_text = title = ""
    split_link = str(schedule_entry.string).split(" | ")
    date_text = split_link[0]
    time_text = split_link[1]
    title = split_link[2]

    append_date(date_text, entry, request_timestamp)
    append_time(time_text, entry)
    append_title_info(title, entry)
    entry["link"] = "https://www.daserste.de" + str(schedule_entry["href"])
    return entry


def append_date(date_text: str, entry, request_date):
    if "Heute" in date_text:
        entry["day"] = request_date.day
        entry["month"] = request_date.month
        weekdaynum = request_date.weekday()
        entry["weekday"] = switch_weekday_num[weekdaynum]

    elif "Morgen" in date_text:
        with request_date + timedelta(days=1) as date:
            entry["day"] = date.day
            entry["month"] = date.month
            weekdaynum = date.weekday()
            entry["weekday"] = switch_weekday_num[weekdaynum]

    else:
        date = date_text.split(", ")
        date_split = date[1].split(".")
        entry["day"] = date_split[0]
        entry["month"] = date_split[1]
        entry["weekday"] = switch_weekday_abr[date[0][:-1]]


def append_time(time_text: str, entry):
    entry["time"] = time_text
    entry["hour"] = time_text[0:2]
    entry["minute"] = time_text[3:5]


def append_title_info(title_text: str, entry):
    entry["title"] = title_text[:title_text.find("(")-1]

    bracket_text = title_text[title_text.find("(")+1:len(title_text)-1]

    city_text = bracket_text[bracket_text.rfind("(")+1:len(bracket_text)-1]
    entry["city"] = city_text

    entry["inspectors"] = bracket_text[:-len(city_text)-4]


if __name__ == "__main__":
    print(get_tatort())
