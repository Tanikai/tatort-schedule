# tatort.py

<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

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
   git clone https://github.com/Tanikai/Tatort.py.git
   ```
2. Install Python requirements
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Import the tatort.py package and call the get_tatort function:

```python
import tatort

schedule = tatort.get_tatort()
```

## License

Distributed under the GPLv3 License. See `LICENSE` for more information.

## Contact

Kai Anter - [@tanikai29](https://twitter.com/tanikai29) - kai.anter@web.de

Project Link: [https://github.com/Tanikai/Tatort.py](https://github.com/Tanikai/Tatort.py)
