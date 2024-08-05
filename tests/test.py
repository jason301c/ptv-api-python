from ptv_api import PTVClient

client = PTVClient()

print("(0/) Testing .search()")
# Searching by term South Yarra, only including train routes
print(client.search("South Yarra", route_types=[0]))
input("Press enter..")

print("(1/) Testing .get_stops_by_route()")
# Getting stops of the Pakenham train route
print(client.get_stops_by_route(11, 0, include_advertised_interchange=True))
input("Press enter..")

print("(1/) Testing .get_stops_by_geolocation()")
# Latitude and longitude of Southern Cross station
print(client.get_stops_by_geolocation(-37.818, 144.952, max_results=1))
input("Press enter..")

# TODO: Filter by route

print("(1/) Testing .get_stop_details()")
# ID of Southern Cross station
print(client.get_stop_details(1181, 1))
input("Press enter..")
"""


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
