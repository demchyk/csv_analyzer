# CSV Analyzer


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger) [![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

Service for processing and analysing big data provided in csv format. As input we 


## Installation and running

Clone repository 

```sh
git clone https://github.com/demchyk/csv_analyzer
```
Install the dependencies

```sh
cd csv_analyzer
pip install -r requirements.txt
```

And start the server

```sh
python wsgi.py
```

## Usage

For using this application you must have a specific file structure in your main profect folder
```text
|---ZTE
|    |GSMV3
|       |--- input_data
|           |--- fils.scv
|       |--- requirements
|           |--- datapath.txt
|           |--- formula.txt
|           |--- cluster.txt
|           |--- keys.txt
|    |LTE
|       |--- input_data
|           |--- fils.scv
|       |--- requirements
|           |--- datapath.txt
|           |--- formula.txt
|           |--- cluster.txt
|           |--- keys.txt
|    |WCDMA
|       |--- input_data
|           |--- fils.scv
|       |--- requirements
|           |--- datapath.txt
|           |--- formula.txt
|           |--- cluster.txt
|           |--- keys.txt
```

Run the server and open the server home page
For processing input data open the "Load new data" tab and follow the instruction
![load_new_data](/img/load_new_data.png)

For export processed data open the "Export to csv" tab and follow the instruction
![export_to_scv](/img/export_to_scv.png)

For visualization data open the "Dashboard" tab
![dashapp](/img/dashapp.gif)
