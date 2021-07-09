# Tatort Schedule

## About The Project

This project contains a Python 3 module that parses the schedule of the [*Tatort* website](https://www.daserste.de/unterhaltung/krimi/tatort/vorschau/index.html). After parsing, it returns a list containing the next broadcasts on the channel *Das Erste*.

### Built With

* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

You will need a working installation of Python 3.

### Installation

1. Install via pip:

   ```sh
   pip install tatort_schedule
   ```

## Usage

Import tatort_schedule and call the get_tatort function:

```python
from tatort_schedule import schedule

schedule = schedule.get_tatort()
```

For each schedule element, a dictionary with the following keys is returned:

| Key | Example Value |
| --- | --------------|
| day | 9 |
| month | 7 |
| weekday | Freitag |
| time | 22:15 Uhr |
| hour | 22 |
| minute | 15 |
| title | Mord Ex Machina |
| city | Saarbrücken |
| inspectors | Stellbrink und Marx |
| link | [https://www.daserste.de/unterhaltung/krimi/tatort/sendung/mord-ex-machina-104.html](https://www.daserste.de/unterhaltung/krimi/tatort/sendung/mord-ex-machina-104.html) |

## License

Distributed under the GPLv3 License. See `LICENSE` for more information.

## Contact

Kai Anter - [@tanikai29](https://twitter.com/tanikai29) - kai.anter@web.de

Project Link: [https://github.com/Tanikai/tatort-schedule](https://github.com/Tanikai/tatort-schedule)
