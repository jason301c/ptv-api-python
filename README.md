# PTV Data API Module

This Python module is a wrapper for Public Transport Victoria (PTV) data API. It allows users to retrieve information about public transport schedules, routes, stops, and other related data made available by PTV.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Setup](#setup)
4. [Usage](#usage)
5. [Examples](#examples)
6. [Endpoints](#methods-and-endpoints)
6. [Contact](#contact)
7. [To-do](#to-do)

## Features
The purpose of this module is to ease the access of [PTV Data API](https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/ptv-timetable-api/) v3 through Python. The endpoints of PTV Data API are presented as methods of PTVClient.
- PTV signature calculation
- API key authentication on initialization
- Supports all PTV API endpoints
  
## Installation
### Manually
1. Download the folder `ptv_api`.
2. Install the required packages using `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

## Setup
You are going to need a pair of Developer ID and API key from [Public Transport Victoria](https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/ptv-timetable-api/)
### Option 1: .env file
- Create a file named __'.env'__ in the same directory where you import __'ptv_api'__.
- The contents should follow the format of __'.env_sample'__.
### Option 2: Passing credentials during instantiation
- When creating an instance of __'PTVClient'__, pass the Developer ID and API key as arguments

## Usage
Import __'PTVClient'__:
   ```bash
   pip install -r requirements.txt
   ```
Instantiate a client object:
   ```bash
   client = PTVClient()  # If you have the .env file set up
   # OR
   client = PTVClient("API_KEY", DEV_ID)
   ```
Access the endpoints through __'PTVClient'__'s methods:
   ```
   client.search("South Yarra")
   ```

## Examples
To view departures for the Pakenham line in Southern Cross
   ```bash
   departures = client.get_departures_by_stop_and_route(route_type=0, stop_id=1181, route_id=11)
   print(departures)
   ```
To estimate a fare by zone:
   ```bash
   fare_estimate = client.get_fare_estimate(min_zone=1, max_zone=2)
   print(fare_estimate)
   ```
And so many more...

## Methods and Endpoints
You can access the list of PTV Endpoints [here](https://timetableapi.ptv.vic.gov.au/swagger/ui/index).
<details>
<summary>All endpoints have a corresponding method. (Click to expand)</summary>

- `get_departures_by_stop`
  - Endpoint: `/v3/departures/route_type/{route_type}/stop/{stop_id}`

- `get_departures_by_stop_and_route`
  - Endpoint: `/v3/departures/route_type/{route_type}/stop/{stop_id}/route/{route_id}`

- `get_directions_by_route`
  - Endpoint: `/v3/directions/route/{route_id}`

- `get_directions_by_direction_id`
  - Endpoint: `/v3/directions/{direction_id}`

- `get_direction_by_direction_id_and_route_type`
  - Endpoint: `/v3/directions/{direction_id}/route_type/{route_type}`

- `get_disruptions_all`
  - Endpoint: `/v3/disruptions`

- `get_disruptions_by_route`
  - Endpoint: `/v3/disruptions/route/{route_id}`

- `get_disruptions_by_route_and_stop`
  - Endpoint: `/v3/disruptions/route/{route_id}/stop/{stop_id}`

- `get_disruptions_by_stop`
  - Endpoint: `/v3/disruptions/stop/{stop_id}`

- `get_disruption_by_id`
  - Endpoint: `/v3/disruptions/{disruption_id}`

- `get_disruption_modes`
  - Endpoint: `/v3/disruptions/modes`

- `get_fare_estimate`
  - Endpoint: `/v3/fare_estimate/min_zone/{min_zone}/max_zone/{max_zone}`

- `get_outlets_all`
  - Endpoint: `/v3/outlets`

- `get_outlets_by_geolocation`
  - Endpoint: `/v3/outlets/location/{latitude},{longitude}`

- `get_pattern_by_run_ref`
  - Endpoint: `/v3/pattern/run/{run_ref}/route_type/{route_type}`

- `get_route_all`
  - Endpoint: `/v3/routes`

- `get_route_by_id`
  - Endpoint: `/v3/routes/{route_id}`

- `get_route_types`
  - Endpoint: `/v3/route_types`

- `get_runs_by_route`
  - Endpoint: `/v3/runs/route/{route_id}`

- `get_runs_by_route_and_route_type`
  - Endpoint: `/v3/runs/route/{route_id}/route_type/{route_type}`

- `get_run_by_ref`
  - Endpoint: `/v3/runs/{run_ref}`

- `get_run_by_ref_and_route_type`
  - Endpoint: `/v3/runs/{run_ref}/route_type/{route_type}`

- `search`
  - Endpoint: `/v3/search/{search_term}`

- `get_stop_details`
  - Endpoint: `/v3/stops/{stop_id}/route_type/{route_type}`

- `get_stops_by_route`
  - Endpoint: `/v3/stops/route/{route_id}/route_type/{route_type}`

- `get_stops_by_geolocation`
  - Endpoint: `/v3/stops/location/{latitude},{longitude}`
</details>


## Contact
For questions or support, feel free to message me on GitHub.

## To-do
- Perhaps uploading to PyPi for easier access
