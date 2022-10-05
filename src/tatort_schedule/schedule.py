import urllib.request
import dateutil.parser
import dateutil.tz
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from enum import IntEnum

# Global
TATORT_URL = "https://www.daserste.de/unterhaltung/krimi/tatort/vorschau/index.html"


class Scheduletype(IntEnum):
    Erste = 1
    Dritte = 2


def get_tatort_erste() -> [dict]:
    """
    Returns the current schedule for Tatort on the channel "Das Erste".
    """
    return parse_tatort_website(load_tatort_website(), Scheduletype.Erste)


def get_tatort_dritte() -> [dict]:
    """
    Returns the current schedule for Tatort on other channels.
    """
    return parse_tatort_website(load_tatort_website(), Scheduletype.Dritte)


def load_tatort_website() -> str:
    """
    Loads the Tatort schedule webiste defined in TATORT_URL.
    """
    html_file = ""
    with urllib.request.urlopen(TATORT_URL) as response:
        html_file = response.read().decode("utf-8")
    return html_file


def parse_tatort_website(html: str, schedule=Scheduletype.Erste) -> [dict]:
    """
    Parses the given Tatort website and returns an array of dicts, each
    containing a schedule entry for the upcoming Tatort episodes.

    >>> site = open("../../tests/testdata/20210209.html", "r").read()
    >>> schedule = parse_tatort_website(site)
    >>> schedule[0]
    {'city': 'Dresden', 'inspectors': 'Gorniak, Winkler und Schnabel', 'title': 'Rettung so nah', 'time': '2021-02-07T20:15:00+01:00', 'link': 'https://www.daserste.de/unterhaltung/krimi/tatort/sendung/rettung-so-nah-100.html'}
    >>> schedule = parse_tatort_website(site, Scheduletype.Dritte)
    >>> schedule[0]
    {'city': 'MÃ¼nster', 'inspectors': 'Thiel und Boerne', 'title': 'Ein FuÃŸ kommt selten allein', 'channel': 'BR', 'time': '2021-02-09T20:15:00+01:00', 'link': 'https://www.daserste.de/unterhaltung/krimi/tatort/sendung/ein-fuss-kommt-selten-allein-104.html'}
    """
    soup = BeautifulSoup(html, "html.parser")

    # Timestamp of website request is between </body> and </html> tag, e.g.
    # </body><!-- stage-4.deo @ Sun Feb 07 09:16:08 CET 2021 --></html>
    for line in reversed(soup.html.contents):
        at_index = line.find("@")  # look for comment
        if at_index == -1:
            continue
        else:  # valid line: ' stage-3.deo @ Sun Aug 29 17:40:15 CEST 2021 '
            timestamp_text = line[at_index+2:-1]
            break

    tzmapping = {'CET': dateutil.tz.gettz('Europe/Berlin'),
                 'CEST': dateutil.tz.gettz('Europe/Berlin')}
    try:
        request_timestamp = dateutil.parser.parse(
            timestamp_text, tzinfos=tzmapping)
    except Exception:
        request_timestamp = datetime.now()

    # Found linklists:
    # 0:"nächste Erstausstrahlung"
    # 1:"im Ersten"
    # 2:"in den Dritten"
    # 3:"auf ONE"
    # 4:"Tatort in Ihrem dritten Programm"
    tatort_linklists = soup.find_all("div", class_="linklist")
    # sometimes there are more than 5 entries
    index_offset = len(tatort_linklists) - 5
    tatort_list = tatort_linklists[int(schedule) + index_offset].find_all("a")
    schedule_list = []
    for link in tatort_list:
        entry = _parse_row(link.string, request_timestamp, schedule)
        entry["link"] = link["href"]
        if not "https://www.daserste.de" in entry["link"]:
            entry["link"] = "https://www.daserste.de" + entry["link"]
        schedule_list.append(entry)
    return schedule_list


def _parse_row(schedule_text: str, request_timestamp: datetime, schedule: Scheduletype) -> dict:
    """
    Parses a row in the Tatort schedule, for example:
    >>> entry_string = "So., 14.02. | 20:15 Uhr | Hetzjagd (Odenthal und Stern  (Ludwigshafen))"

    A request timestamp has to be passed into the function, because the first column can contain 'Heute' or 'Morgen' (today and tomorrow respectively)
    >>> request_ts = datetime(2021, 2, 7, 9, 16, 8, 0, dateutil.tz.gettz('Europe/Berlin'))
    >>> entry = _parse_row(entry_string, request_ts, Scheduletype.Erste)

    The results are returned in a dictionary:
    >>> entry["time"]
    '2021-02-14T20:15:00+01:00'
    >>> entry["title"]
    'Hetzjagd'
    >>> entry["city"]
    'Ludwigshafen'
    >>> entry["inspectors"]
    'Odenthal und Stern'

    >>> entry_string = "Di., 09.02. | 20:15 Uhr | BR | Ein Fuß kommt selten allein (Thiel und Boerne  (Münster))"
    >>> entry = _parse_row(entry_string, request_ts, Scheduletype.Dritte)
    >>> entry["time"]
    '2021-02-09T20:15:00+01:00'
    >>> entry["title"]
    'Ein Fuß kommt selten allein'
    >>> entry["city"]
    'Münster'
    >>> entry["inspectors"]
    'Thiel und Boerne'
    >>> entry["channel"]
    'BR'
    """
    columns = schedule_text.split(" | ")

    if schedule == Scheduletype.Erste:
        entry = _parse_title(columns[2])
    elif schedule == Scheduletype.Dritte:
        entry = _parse_title(columns[3])
        entry["channel"] = columns[2]
    entry["time"] = _parse_datetime(columns[0], columns[1], request_timestamp)
    return entry


def _parse_datetime(date_text: str, time_text: str, request_ts: datetime) -> datetime:
    """
    Returns a datetime object containing info from date_text and time_text:

    >>> request_ts = datetime(2020, 2, 7, 9, 16, 8, 0, dateutil.tz.gettz('Europe/Berlin'))
    >>> _parse_datetime("So., 14.02.", "20:15 Uhr", request_ts)
    '2020-02-14T20:15:00+01:00'

    When the new Tatort episode is coming today, the date of the request
    timestamp is used:
    >>> _parse_datetime("Heute", "20:15 Uhr", request_ts)
    '2020-02-07T20:15:00+01:00'

    Same thing with tomorrow:
    >>> _parse_datetime("Morgen", "20:15 Uhr", request_ts)
    '2020-02-08T20:15:00+01:00'

    During summertime / CEST, the timezone in the timestamp is UTC+2:
    >>> _parse_datetime("So., 11.07.", "20:15 Uhr", request_ts)
    '2020-07-11T20:15:00+02:00'
    """

    if "Heute" in date_text:
        day = int(request_ts.day)
        month = int(request_ts.month)
        year = int(request_ts.year)
    elif "Morgen" in date_text:
        tomorrow = request_ts + timedelta(days=1)
        day = int(tomorrow.day)
        month = int(tomorrow.month)
        year = int(tomorrow.year)
    else:
        date = date_text.split(", ")
        date_split = date[1].split(".")
        day = int(date_split[0])
        month = int(date_split[1])
        year = int(request_ts.year)

    hour = int(time_text[0:2])
    minute = int(time_text[3:5])

    return datetime(year, month, day, hour, minute, 0, 0, request_ts.tzinfo).isoformat()


def _parse_title(title_text: str) -> dict:
    """
    Parses the title, city and inspector names from the given string:

    >>> title = "  Damian  (    Tobler und Weber   (   Schwarzwald   )  )  "
    >>> title_infos = _parse_title(title)
    >>> title_infos["title"]
    'Damian'
    >>> title_infos["city"]
    'Schwarzwald'
    >>> title_infos["inspectors"]
    'Tobler und Weber'

    >>> title = "In der Familie (1) (Batic, Leitmayr und Kalli mit Faber, Bönisch, Dalay, Pawlak (München, Dortmund))"
    >>> title_infos = _parse_title(title)
    >>> title_infos["title"]
    'In der Familie (1)'
    >>> title_infos["city"]
    'München, Dortmund'
    >>> title_infos["inspectors"]
    'Batic, Leitmayr und Kalli mit Faber, Bönisch, Dalay, Pawlak'
    """

    title_info = {}
    # parse backwards
    city_begin = title_text.rfind("(")+1
    city_end = title_text.find(")", city_begin)
    title_info["city"] = title_text[city_begin:city_end].strip()

    inspector_begin = title_text.rfind("(", 0, city_begin-1) + 1
    title_info["inspectors"] = title_text[inspector_begin:city_begin-2].strip()

    title_info["title"] = title_text[:inspector_begin-2].strip()

    return title_info


if __name__ == "__main__":
    import doctest
    doctest.testmod()
