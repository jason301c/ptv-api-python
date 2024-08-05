import os
import requests
from dotenv import load_dotenv
from .src.get_signature import get_url, validate_key
import json
load_dotenv()


class PTVClient:
    def __init__(self, api_key: str = None, developer_id: int = None):
        """
        Initializes a PTVClient object
        :param api_key: PTV provided API key
        :param developer_id: PTV provided Developer ID
        """
        self.__api_key = api_key or os.getenv('PTV_API_KEY')
        self.__developer_id = developer_id or os.getenv('PTV_DEVELOPER_ID')

        if not self.__api_key or not self.__developer_id:
            raise ValueError("API key / Developer ID not found")
        elif not validate_key(self.__api_key, self.__developer_id):
            raise RuntimeError("API Key / Developer ID authentication fail")

    def _make_request(self, endpoint: str, params: dict = None) -> dict or None:
        """Helper method to make API requests."""
        url = get_url(endpoint, self.__api_key, self.__developer_id, params)
        response = requests.get(url)
        print("REQUEST URL: ", url)
        return json.dumps(response.json(), indent=2)

    def get_departures_by_stop(self, route_type: int, stop_id: int, max_results: int = 10, **kwargs) -> dict or None:
        """
        View departures for all routes from a stop.

        :param route_type: Number identifying transport mode; values returned via RouteTypes API (0: Train, 1: Tram, 2: Bus, 3: V/Line, 4: Night Bus)
        :param stop_id: Identifier of stop; values returned by Stops API
        :param max_results: Maximum number of results to return
        :param kwargs: Optional keyword arguments for advanced filtering:
            - platform_numbers (list[int]): List of platform numbers to filter.
            - direction_id (int): Identifier for direction of travel.
            - gtfs (bool): Include GTFS information.
            - include_advertised_interchange (bool): Include advertised interchange.
            - date_utc (str): Filter by specific date in UTC format.
            - include_cancelled (bool): Include cancelled departures.
            - look_backwards (bool): Look for departures in the past.
            - expand (list[str]): Fields to expand in the response.
            - include_geopath (bool): Include geopath data.

        :return: Dictionary of departures data or None if request fails
        """
        endpoint = f"/v3/departures/route_type/{route_type}/stop/{stop_id}"
        params = {
            'max_results': max_results,
            **kwargs
        }
        return self._make_request(endpoint, params=params)

    def get_departures_by_stop_and_route(self, route_type: int, stop_id: int, route_id: int, max_results: int = 10,
                                         **kwargs) -> dict or None:
        """
        View departures for a specific route from a stop.

        :param route_type: Number identifying transport mode; values returned via RouteTypes API (0: Train, 1: Tram, 2: Bus, 3: V/Line, 4: Night Bus)
        :param stop_id: Identifier of stop; values returned by Stops API
        :param route_id: Identifier of route; values returned by Routes API
        :param max_results: Maximum number of results to return
        :param kwargs: Optional keyword arguments for advanced filtering:
            - direction_id (int): Identifier for direction of travel.
            - gtfs (bool): Include GTFS information.
            - include_advertised_interchange (bool): Include advertised interchange.
            - date_utc (str): Filter by specific date in UTC format.
            - include_cancelled (bool): Include cancelled departures.
            - look_backwards (bool): Look for departures in the past.
            - expand (list[str]): Fields to expand in the response.
            - include_geopath (bool): Include geopath data.

        :return: Dictionary of departures data or None if request fails
        """
        endpoint = f"/v3/departures/route_type/{route_type}/stop/{stop_id}/route/{route_id}"
        params = {
            'max_results': max_results,
            **kwargs
        }
        return self._make_request(endpoint, params=params)

    def get_directions_by_route(self, route_id: int) -> dict or None:
        """
        View directions that a route travels in.

        :param route_id: Identifier of route; values returned by Routes API
        :return: Dictionary of directions data or None if request fails
        """
        endpoint = f"/v3/directions/route/{route_id}"
        return self._make_request(endpoint)

    def get_directions_by_direction_id(self, direction_id: int) -> dict or None:
        """
        View all routes for a direction of travel.

        :param direction_id: Identifier of direction of travel; values returned by Directions API
        :return: Dictionary of routes data or None if request fails
        """
        endpoint = f"/v3/directions/{direction_id}"
        return self._make_request(endpoint)

    def get_direction_by_direction_id_and_route_type(self, direction_id: int, route_type: int) -> dict or None:
        """
        View all routes of a particular type for a direction of travel.

        :param direction_id: Identifier of direction of travel; values returned by Directions API
        :param route_type: Number identifying transport mode; values returned via RouteTypes API (0: Train, 1: Tram, 2: Bus, 3: V/Line, 4: Night Bus)
        :return: Dictionary of routes data or None if request fails
        """
        endpoint = f"/v3/directions/{direction_id}/route_type/{route_type}"
        return self._make_request(endpoint)

    def get_disruptions_all(self, **kwargs) -> dict or None:
        """
        View all disruptions for all route types.

        :param kwargs: Optional keyword arguments for filtering:
            - route_types (list[int]): Filter by route type.
            - disruption_modes (list[int]): Filter by disruption mode.
            - disruption_status (str): Filter by status of disruption ('current' or 'planned').
        :return: Dictionary of disruptions data or None if request fails
        """
        endpoint = "/v3/disruptions"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_disruptions_by_route(self, route_id: int, **kwargs) -> dict or None:
        """
        View all disruptions for a particular route.

        :param route_id: Identifier of route; values returned by Routes API
        :param kwargs: Optional keyword arguments for filtering:
            - disruption_status (str): Filter by status of disruption ('current' or 'planned').
        :return: Dictionary of disruptions data or None if request fails
        """
        endpoint = f"/v3/disruptions/route/{route_id}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_disruptions_by_route_and_stop(self, route_id: int, stop_id: int, **kwargs) -> dict or None:
        """
        View all disruptions for a particular route and stop.

        :param route_id: Identifier of route; values returned by Routes API
        :param stop_id: Identifier of stop; values returned by Stops API
        :param kwargs: Optional keyword arguments for filtering:
            - disruption_status (str): Filter by status of disruption ('current' or 'planned').
        :return: Dictionary of disruptions data or None if request fails
        """
        endpoint = f"/v3/disruptions/route/{route_id}/stop/{stop_id}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_disruptions_by_stop(self, stop_id: int, **kwargs) -> dict or None:
        """
        View all disruptions for a particular stop.

        :param stop_id: Identifier of stop; values returned by Stops API
        :param kwargs: Optional keyword arguments for filtering:
            - disruption_status (str): Filter by status of disruption ('current' or 'planned').
        :return: Dictionary of disruptions data or None if request fails
        """
        endpoint = f"/v3/disruptions/stop/{stop_id}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_disruption_by_id(self, disruption_id: int) -> dict or None:
        """
        View a specific disruption.

        :param disruption_id: Identifier of disruption; values returned by Disruptions API
        :return: Dictionary of disruption data or None if request fails
        """
        endpoint = f"/v3/disruptions/{disruption_id}"
        return self._make_request(endpoint)

    def get_disruption_modes(self) -> dict or None:
        """
        Get all disruption modes.

        :return: Dictionary of disruption modes data or None if request fails
        """
        endpoint = "/v3/disruptions/modes"
        return self._make_request(endpoint)

    def get_fare_estimate(self, min_zone: int, max_zone: int, **kwargs) -> dict or None:
        """
        Estimate a fare by zone.

        :param min_zone: Minimum Zone travelled through (e.g., 1)
        :param max_zone: Maximum Zone travelled through (e.g., 6)
        :param kwargs: Optional keyword arguments for advanced filtering:
            - journey_touch_on_utc (str): Date and time of touch on in UTC format.
            - journey_touch_off_utc (str): Date and time of touch off in UTC format.
            - is_journey_in_free_tram_zone (bool): If journey is in a free tram zone.
            - travelled_route_types (list[int]): List of route types travelled through.
        :return: Dictionary of fare estimate data or None if request fails
        """
        endpoint = f"/v3/fare_estimate/min_zone/{min_zone}/max_zone/{max_zone}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_outlets_all(self, max_results: int = 30) -> dict or None:
        """
        List all ticket outlets.

        :param max_results: Maximum number of results to return
        :return: Dictionary of ticket outlets data or None if request fails
        """
        endpoint = "/v3/outlets"
        params = {
            'max_results': max_results
        }
        return self._make_request(endpoint, params=params)

    def get_outlets_by_geolocation(self, latitude: float, longitude: float, max_distance: float = 300,
                                   max_results: int = 30) -> dict or None:
        """
        List ticket outlets near a specific location.

        :param latitude: Geographic coordinate of latitude
        :param longitude: Geographic coordinate of longitude
        :param max_distance: Maximum distance (in meters) from specified location
        :param max_results: Maximum number of results to return
        :return: Dictionary of ticket outlets data or None if request fails
        """
        endpoint = f"/v3/outlets/location/{latitude},{longitude}"
        params = {
            'max_distance': max_distance,
            'max_results': max_results
        }
        return self._make_request(endpoint, params=params)

    def get_pattern_by_run_ref(self, run_ref: str, route_type: int, **kwargs) -> dict or None:
        """
        View the stopping pattern for a specific trip/service run.

        :param run_ref: Identifier of a run as returned by the departures/* and runs/* endpoints
        :param route_type: Number identifying transport mode; values returned via RouteTypes API (0: Train, 1: Tram, 2: Bus, 3: V/Line, 4: Night Bus)
        :param kwargs: Optional keyword arguments for advanced filtering:
            - expand (list[str]): Fields to expand in the response.
            - stop_id (int): Filter by stop ID.
            - date_utc (str): Filter by specific date in UTC format.
            - include_skipped_stops (bool): Include skipped stops.
            - include_geopath (bool): Include geopath data.
            - include_advertised_interchange (bool): Include advertised interchange.
        :return: Dictionary of stopping pattern data or None if request fails
        """
        endpoint = f"/v3/pattern/run/{run_ref}/route_type/{route_type}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_route_all(self, **kwargs) -> dict or None:
        """
        View route names and numbers for all routes.

        :param kwargs: Optional keyword arguments for filtering:
            - route_types (list[int]): Filter by route type.
            - route_name (str): Filter by name of route (accepts partial route name matches).
        :return: Dictionary of route data or None if request fails
        """
        endpoint = "/v3/routes"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_route_by_id(self, route_id: int, **kwargs) -> dict or None:
        """
        View route name and number for a specific route ID.

        :param route_id: Identifier of route; values returned by Departures, Directions, and Disruptions APIs
        :param kwargs: Optional keyword arguments for filtering:
            - include_geopath (bool): Indicates if geopath data will be returned (default = false).
            - geopath_utc (str): Filter geopaths by date (ISO 8601 UTC format).
        :return: Dictionary of route data or None if request fails
        """
        endpoint = f"/v3/routes/{route_id}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_route_types(self) -> dict or None:
        """
        View all route types and their names.

        :return: Dictionary of route types data or None if request fails
        """
        endpoint = "/v3/route_types"
        return self._make_request(endpoint)

    def get_runs_by_route(self, route_id: int, **kwargs) -> dict or None:
        """
        View all trip/service runs for a specific route ID.

        :param route_id: Identifier of route; values returned by Routes API
        :param kwargs: Optional keyword arguments for filtering:
            - expand (list[str]): Fields to expand in the response.
            - date_utc (str): Filter by specific date in UTC format.
            - include_advertised_interchange (bool): Include advertised interchange.
        :return: Dictionary of run data or None if request fails
        """
        endpoint = f"/v3/runs/route/{route_id}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_runs_by_route_and_route_type(self, route_id: int, route_type: int, **kwargs) -> dict or None:
        """
        View all trip/service runs for a specific route ID and route type.

        :param route_id: Identifier of route; values returned by Routes API
        :param route_type: Number identifying transport mode; values returned via RouteTypes API (0: Train, 1: Tram, 2: Bus, 3: V/Line, 4: Night Bus)
        :param kwargs: Optional keyword arguments for filtering:
            - expand (list[str]): Fields to expand in the response.
            - date_utc (str): Filter by specific date in UTC format.
            - include_advertised_interchange (bool): Include advertised interchange.
        :return: Dictionary of run data or None if request fails
        """
        endpoint = f"/v3/runs/route/{route_id}/route_type/{route_type}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_run_by_ref(self, run_ref: str, **kwargs) -> dict or None:
        """
        View all trip/service runs for a specific run_ref.

        :param run_ref: Identifier of a run as returned by the departures/* and runs/* endpoints
        :param kwargs: Optional keyword arguments for filtering:
            - include_geopath (bool): Include geopath data.
            - expand (list[str]): Fields to expand in the response.
            - date_utc (str): Filter by specific date in UTC format.
            - include_advertised_interchange (bool): Include advertised interchange.
        :return: Dictionary of run data or None if request fails
        """
        endpoint = f"/v3/runs/{run_ref}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_run_by_ref_and_route_type(self, run_ref: str, route_type: int, **kwargs) -> dict or None:
        """
        View the trip/service run for a specific run_ref and route type.

        :param run_ref: Identifier of a run as returned by the departures/* and runs/* endpoints
        :param route_type: Number identifying transport mode; values returned via RouteTypes API (0: Train, 1: Tram, 2: Bus, 3: V/Line, 4: Night Bus)
        :param kwargs: Optional keyword arguments for filtering:
            - expand (list[str]): Fields to expand in the response.
            - date_utc (str): Filter by specific date in UTC format.
            - include_geopath (bool): Include geopath data.
        :return: Dictionary of run data or None if request fails
        """
        endpoint = f"/v3/runs/{run_ref}/route_type/{route_type}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def search(self, search_term: str, **kwargs) -> dict or None:
        """
        View stops, routes, and myki ticket outlets that match the search term.

        :param search_term: Search text (if search text is numeric and/or less than 3 characters, the API will only return routes)
        :param kwargs: Optional keyword arguments for advanced filtering:
            - route_types (list[int]): Filter by route type.
            - latitude (float): Latitude coordinate for location-based search.
            - longitude (float): Longitude coordinate for location-based search.
            - max_distance (float): Maximum distance for location-based search.
            - include_addresses (bool): Include address information.
            - include_outlets (bool): Include outlet information.
            - match_stop_by_suburb (bool): Match stop by suburb.
            - match_route_by_suburb (bool): Match route by suburb.
            - match_stop_by_gtfs_stop_id (bool): Match stop by GTFS stop ID.
        :return: Dictionary of search results data or None if request fails
        """
        endpoint = f"/v3/search/{search_term}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_stop_details(self, stop_id: int, route_type: int, **kwargs) -> dict or None:
        """
        View facilities at a specific stop (Metro and V/Line stations only).

        :param stop_id: Identifier of stop; values returned by Stops API
        :param route_type: Number identifying transport mode; values returned via RouteTypes API (0: Train, 1: Tram, 2: Bus, 3: V/Line, 4: Night Bus)
        :param kwargs: Optional keyword arguments for filtering:
            - stop_location (bool): Indicates if stop location information will be returned (default = false).
            - stop_amenities (bool): Indicates if stop amenity information will be returned (default = false).
            - stop_accessibility (bool): Indicates if stop accessibility information will be returned (default = false).
            - stop_contact (bool): Indicates if stop contact information will be returned (default = false).
            - stop_ticket (bool): Indicates if stop ticket information will be returned (default = false).
            - gtfs (bool): Indicates whether the stop_id is a GTFS ID or not.
            - stop_staffing (bool): Indicates if stop staffing information will be returned (default = false).
            - stop_disruptions (bool): Indicates if stop disruption information will be returned (default = false).
        :return: Dictionary of stop data or None if request fails
        """
        endpoint = f"/v3/stops/{stop_id}/route_type/{route_type}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_stops_by_route(self, route_id: int, route_type: int, **kwargs) -> dict or None:
        """
        View all stops on a specific route.

        :param route_id: Identifier of route; values returned by Routes API
        :param route_type: Number identifying transport mode; values returned via RouteTypes API (0: Train, 1: Tram, 2: Bus, 3: V/Line, 4: Night Bus)
        :param kwargs: Optional keyword arguments for filtering:
            - direction_id (int): Identifier for direction of travel.
            - stop_disruptions (bool): Indicates if stop disruption information will be returned (default = false).
            - include_geopath (bool): Include geopath data.
            - geopath_utc (str): Filter geopaths by date (ISO 8601 UTC format).
            - include_advertised_interchange (bool): Include advertised interchange.
        :return: Dictionary of stop data or None if request fails
        """
        endpoint = f"/v3/stops/route/{route_id}/route_type/{route_type}"
        params = {**kwargs}
        return self._make_request(endpoint, params=params)

    def get_stops_by_geolocation(self, latitude: float, longitude: float, max_results: int = 30,
                                 max_distance: float = 300, **kwargs) -> dict or None:
        """
        View all stops near a specific location.

        :param latitude: Geographic coordinate of latitude
        :param longitude: Geographic coordinate of longitude
        :param max_results: Maximum number of results returned (default = 30)
        :param max_distance: Filter by maximum distance (in meters) from location specified via latitude and longitude parameters (default = 300)
        :param kwargs: Optional keyword arguments for filtering:
            - route_types (list[int]): Filter by route type.
            - stop_disruptions (bool): Indicates if stop disruption information will be returned (default = false).
        :return: Dictionary of stop data or None if request fails
        """
        endpoint = f"/v3/stops/location/{latitude},{longitude}"
        params = {
            'max_results': max_results,
            'max_distance': max_distance,
            **kwargs
        }
        return self._make_request(endpoint, params=params)
