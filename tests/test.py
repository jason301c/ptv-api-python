from ptv_api import PTVClient
import json
client = PTVClient()

out = client.get_stops_by_route(11, 0,include_advertised_interchange = True)
print(out)
with open('output.json', 'w') as file:
    json.dump(out, file)


# Pakenham route_id 11
# South Yarra Station stop_id 1180
# Train route_type 0
"""
client.search()

client.get_stops_by_route()
client.get_stops_by_geolocation()
client.get_stop_details()

client.get_outlets_all()
client.get_outlets_by_geolocation()

client.get_departures_by_stop()
client.get_departures_by_stop_and_route()

client.get_route_types()
client.get_route_by_id()
client.get_route_all()

client.get_disruptions_by_route()
client.get_disruptions_by_route_and_stop()
client.get_disruptions_all()
client.get_disruptions_by_stop()
client.get_disruption_modes()
client.get_disruption_by_id()

client.get_fare_estimate()

client.get_run_by_ref()
client.get_runs_by_route()
client.get_runs_by_route_and_route_type()
client.get_run_by_ref_and_route_type()

client.get_pattern_by_run_ref()
"""
