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
print(client.get_stops_by_geolocation(-37.818, 144.952, max_results=1, route_types=[0, 3]))
input("Press enter..")

print("(1/) Testing .get_stop_details()")
# ID of Southern Cross tram station
print(client.get_stop_details(2091, 1))
input("Press enter..")

print("(1/) Testing .get_outlets_all()")
# Gets 30 ticket outlets
print(client.get_outlets_all(30))
input("Press enter..")

print("(1/) Testing .get_outlets_by_geolocation()")
# Gets ticket outlets within 300m of Southern Cross station
print(client.get_outlets_by_geolocation(-37.818, 144.952, 300))
input("Press enter..")

print("(1/) Testing .get_departures_by_stop")
# Gets departures of Southern Cross tram station
print(client.get_departures_by_stop(1, 2091, 10))
input("Press enter..")

print("(1/) Testing .get_departures_by_stop_and_route")
# Gets departures of Pakenham trains in Southern Cross station with direction to Pakenham
print(client.get_departures_by_stop_and_route(0, 1181, 11, 10, direction_id=10))
input("Press enter..")

print("(1/) Testing .get_route_types")
# Gets all the possible route types
print(client.get_route_types())
input("Press enter..")

print("(1/) Testing get_route_by_id")
# Gets Pakenham train route
print(client.get_route_by_id(11))
input("Press enter...")

print("(1/) Testing get_route_all")
# Gets all train routes
print(client.get_route_all(route_types=[0]))
input("Press enter...")

print("(1/) Testing get_disruptions_by_route")
# Gets Pakenham route disruptions
print(client.get_disruptions_by_route(11))
input("Press enter...")

print("(1/) Testing get_disruptions_by_route_and_stop")
# Gets Pakenham disruptions at Pakenham station
print(client.get_disruptions_by_route_and_stop(11, 1153))
input("Press enter...")

print("(1/) Testing get_disruptions_all")
# Gets all disruptions
print(client.get_disruptions_all())
input("Press enter...")

print("(1/) Testing get_disruptions_by_stop")
# Gets all disruptions in Southern Cross station
print(client.get_disruptions_by_stop(1181))
input("Press enter...")

print("(1/) Testing get_disruption_modes")
# Gets all disruption modes
print(client.get_disruption_modes())
input("Press enter...")

print("(1/) Testing get_fare_estimate")
# Gets fare for zone 1 to zone 2
print(client.get_fare_estimate(1, 2))
input("Press enter...")

print("(1/) Testing get_runs_by_route")
# Gets Pakenham runs
print(client.get_runs_by_route(11))
print(client.get_runs_by_route_and_route_type(11, 0))
input("Press enter...")


input("Tests done! Press any key to end.")

