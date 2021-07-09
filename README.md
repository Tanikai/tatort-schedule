# Tatort Schedule

## About The Project

This project contains a Python 3 module that parses the ["Tatort" schedule website](https://www.daserste.de/unterhaltung/krimi/tatort/vorschau/index.html) and returns a list with the next Tatort broadcasts on the channel "Das Erste".

### Built With

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Working installation of Python 3.

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/Tanikai/tatort-schedule.git
   ```

2. Install Python requirements

   ```sh
   pip install -r requirements.txt
   ```

## Usage

Import the tatort.py package and call the get_tatort function:

```python
from tatortschedule import schedule

schedule = schedule.get_tatort()
```

## License

Distributed under the GPLv3 License. See `LICENSE` for more information.

## Contact

Kai Anter - [@tanikai29](https://twitter.com/tanikai29) - kai.anter@web.de

Project Link: [https://github.com/Tanikai/tatort-schedule](https://github.com/Tanikai/Tatort.py)
