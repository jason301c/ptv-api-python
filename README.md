# PTV Data API Module

This Python module is a wrapper for Public Transport Victoria (PTV) data API. It allows users to retrieve information about public transport schedules, routes, stops, and other related data made available by PTV.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Setup](#setup)
4. [Usage](#usage)
5. [Examples](#examples)
6. [Contact](#contact)
7. [To-do](#to-do)

## Features
The purpose of this module is to ease the access of PTV Data API v3 through Python. The endpoints of PTV Data API are presented as methods of PTVClient.
- PTV signature calculation
- API key authentication on initialization
- Supports all PTV API endpoints
  
## Installation
### Manually
- Clone the repository
- Install requirements.txt

## Setup
Firstly, you are going to need a pair of Developer ID and API key from Public Transport Victoria. See more at [Public Transport Victoria](https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/ptv-timetable-api/)
### Option 1: .env file
- Make a file named '.env' in the same directory where you are going to import ptv_api.
- The contents should be in the format of '.env_sample'.
### Option 2: passing while creating an instance
- When creating an instance of PTVClient, pass the Developer ID and API key

## Usage
Import PTVclient:\
from ptv_api import PTVClient'\
Instantiate a client object:\
client = PTVClient() # If you have .env file set up\
client = PTVClient("API_KEY", DEV_ID)\
Now you can access the endpoints through PTVClient's methods:\
client.search("South Yarra")\

## Examples
## Contact
## To-do
