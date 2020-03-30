# Zeus

**ZEUS** is a Python library that serves the weather reporting needs of the Cristina Torres Memorial Observatory. The library consists of several scripts that are run independently in the terminal and use the API of the [National Weather Service](https://www.weather.gov/) (DWML) and [Sunrise-Sunset](https://sunrise-sunset.org/) (JSON). The scripts currently available in the Zeus library are:

- `status.py` : Report current weather status
- `forecast.py` : Report seven-day weather forecast
- `bot.py` : Send status messages to CTMO Twitter page

---

## Installation

Installation simply involves downloading the library and making sure all Python dependencies are met on the local system. The Zeus library was developed on Ubuntu 18.04.4 LTS and has not (yet) been tested on other platforms.

---

## Usage

From the terminal, run one of the scripts as shown in the following example command:

`$ python3 status.py`

---

29 Mar 2020

Richard Camuccio  
rcamuccio@gmail.com