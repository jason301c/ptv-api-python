import os
import requests
from dotenv import load_dotenv
from .src.get_signature import get_url, validate_key
from .enum.RouteType import RouteType

load_dotenv()


class PTVClient:
    def __init__(self, api_key: str = None, developer_id: int = None):
        """
        Initializes a PTVClient object
        :param api_key: PTV provided API key
        :param developer_id: PTV provided Developer ID
        """
        self.api_key = api_key or os.getenv('PTV_API_KEY')
        self.developer_id = developer_id or os.getenv('PTV_DEVELOPER_ID')
        self.base_url = 'https://timetableapi.ptv.vic.gov.au'

        if not self.api_key or not self.developer_id:
            raise ValueError("API key / Developer ID not found")
        elif not validate_key(api_key, developer_id):
            raise RuntimeError("API Key / Developer ID authentication fail")

    def _make_request(self, endpoint: str, params: dict = None) -> dict or None:
        """Helper method to make API requests."""
        url = get_url(endpoint, self.api_key, self.developer_id, self.base_url)
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None
        return response.json()

    def get_departures_for_stop(self, route_type: int, stop_id: int, max_results: int = 10, **kwargs):
        """
        View departures for all routes from a stop.

        :param route_type: Number identifying transport mode; values returned via RouteTypes API
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
        endpoint = f'/v3/departures/route_type/{route_type}/stop/{stop_id}'
        params = {
            'max_results': max_results,
            **kwargs  # Merge the kwargs dictionary with the explicit params
        }
        return self._make_request(endpoint, params=params)

    def get_departures_for_stop_and_route(self, route_type: int, stop_id: int, route_id: str, max_results: int = 10, **kwargs):
        """
        View departures for a specific route from a stop.

        :param route_type: Number identifying transport mode; values returned via RouteTypes API
        :param stop_id: Identifier of stop; values returned by Stops API
        :param route_id: Identifier of route; values returned by Routes API - v3/routes
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
        endpoint = f'/v3/departures/route_type/{route_type}/stop/{stop_id}/route/{route_id}'
        params = {
            'max_results': max_results,
            **kwargs
        }
        return self._make_request(endpoint, params=params)

    def get_directions_for_route(self, route_id: int):
        """
        View directions that a route travels in.

        :param route_id: Identifier of route; values returned by Routes API
        :return: Dictionary of directions data or None if request fails
        """
        endpoint = f'/v3/directions/route/{route_id}'
        return self._make_request(endpoint)

    def get_routes_for_direction(self, direction_id: int):
        """
        View all routes for a direction of travel.

        :param direction_id: Identifier of direction of travel; values returned by Directions API
        :return: Dictionary of routes data or None if request fails
        """
        endpoint = f'/v3/directions/{direction_id}'
        return self._make_request(endpoint)

    def get_routes_for_direction_and_type(self, direction_id: int, route_type: int):
        """
        View all routes of a particular type for a direction of travel.

        :param direction_id: Identifier of direction of travel; values returned by Directions API
        :param route_type: Number identifying transport mode; values returned via RouteTypes API
        :return: Dictionary of routes data or None if request fails
        """
        endpoint = f'/v3/directions/{direction_id}/route_type/{route_type}'
        return self._make_request(endpoint)

    def get_all_disruptions(self, **kwargs):
        """
        View all disruptions for all route types.

        :param kwargs: Optional keyword arguments for filtering:
            - route_types (list[int]): Filter by route_type; values returned via RouteTypes API.
            - disruption_modes (list[int]): Filter by disruption_mode; values returned via v3/disruptions/modes API.
            - disruption_status (str): Filter by status of disruption, e.g., 'current', 'planned'.

        :return: Dictionary of disruptions data or None if request fails
        """
        endpoint = '/v3/disruptions'
        params = kwargs
        return self._make_request(endpoint, params=params)

    def get_disruptions_by_route(self, route_id: int, **kwargs):
        """
        View all disruptions for a particular route.

        :param route_id: Identifier of route; values returned by Routes API
        :param kwargs: Optional keyword arguments for filtering:
            - disruption_status (str): Filter by status of disruption, e.g., 'current', 'planned'.

        :return: Dictionary of disruptions data or None if request fails
        """
        endpoint = f'/v3/disruptions/route/{route_id}'
        params = kwargs
        return self._make_request(endpoint, params=params)

    def get_disruptions_by_route_and_stop(self, route_id: int, stop_id: int, **kwargs):
        """
        View all disruptions for a particular route and stop.

        :param route_id: Identifier of route; values returned by Routes API
        :param stop_id: Identifier of stop; values returned by Stops API
        :param kwargs: Optional keyword arguments for filtering:
            - disruption_status (str): Filter by status of disruption, e.g., 'current', 'planned'.

        :return: Dictionary of disruptions data or None if request fails
        """
        endpoint = f'/v3/disruptions/route/{route_id}/stop/{stop_id}'
        params = kwargs
        return self._make_request(endpoint, params=params)

    def get_disruptions_by_stop(self, stop_id: int, **kwargs):
        """
        View all disruptions for a particular stop.

        :param stop_id: Identifier of stop; values returned by Stops API
        :param kwargs: Optional keyword arguments for filtering:
            - disruption_status (str): Filter by status of disruption, e.g., 'current', 'planned'.

        :return: Dictionary of disruptions data or None if request fails
        """
        endpoint = f'/v3/disruptions/stop/{stop_id}'
        params = kwargs
        return self._make_request(endpoint, params=params)

    def get_disruption_by_id(self, disruption_id: int):
        """
        View a specific disruption.

        :param disruption_id: Identifier of disruption; values returned by Disruptions API
        :return: Dictionary of disruption data or None if request fails
        """
        endpoint = f'/v3/disruptions/{disruption_id}'
        return self._make_request(endpoint)

    def get_disruption_modes(self):
        """
        Get all disruption modes.

        :return: Dictionary of disruption modes data or None if request fails
        """
        endpoint = '/v3/disruptions/modes'
        return self._make_request(endpoint)

    def estimate_fare_by_zone(self, min_zone: int, max_zone: int, **kwargs):
        """
        Estimate a fare by zone.

        :param min_zone: Minimum zone traveled through, e.g., 1
        :param max_zone: Maximum zone traveled through, e.g., 6
        :param kwargs: Optional keyword arguments for additional details:
            - journey_touch_on_utc (str): Journey touch-on time in UTC format.
            - journey_touch_off_utc (str): Journey touch-off time in UTC format.
            - is_journey_in_free_tram_zone (bool): Indicates if the journey is within the free tram zone.
            - travelled_route_types (list[int]): List of route types traveled.

        :return: Dictionary of fare estimate data or None if request fails
        """
        endpoint = f'/v3/fare_estimate/min_zone/{min_zone}/max_zone/{max_zone}'
        params = kwargs
        return self._make_request(endpoint, params=params)

    def get_all_ticket_outlets(self, max_results: int = 100):
        """
        List all ticket outlets.

        :param max_results: Maximum number of results to return
        :return: Dictionary of ticket outlets data or None if request fails
        """
        endpoint = '/v3/outlets'
        params = {'max_results': max_results}
        return self._make_request(endpoint, params=params)

    def get_outlets_by_geolocation(self, latitude: float, longitude: float, max_results: int = 30, **kwargs):
        """
        List ticket outlets near a specific location.

        :param latitude: Geographic coordinate of latitude
        :param longitude: Geographic coordinate of longitude
        :param max_results: Maximum number of results to return
        :param kwargs: Optional keyword arguments for additional filtering:
            - max_distance (float): Maximum distance from the location in meters.

        :return: Dictionary of ticket outlets near location data or None if request fails
        """
        endpoint = f'/v3/outlets/location/{latitude},{longitude}'
        params = {'max_results': max_results, **kwargs}
        return self._make_request(endpoint, params=params)

    def get_stopping_pattern(self, run_ref: str, route_type: int, **kwargs):
        """
        View the stopping pattern for a specific trip/service run.

        :param run_ref: The run_ref is the identifier of a run as returned by the departures/* and runs/* endpoints
        :param route_type: Number identifying transport mode; values returned via RouteTypes API
        :param kwargs: Optional keyword arguments for additional details:
            - expand (list[str]): Fields to expand in the response.
            - stop_id (int): Specific stop ID to include.
            - date_utc (str): Filter by specific date in UTC format.
            - include_skipped_stops (bool): Include skipped stops in the response.
            - include_geopath (bool): Include geopath data.
            - include_advertised_interchange (bool): Include advertised interchange.

        :return: Dictionary of stopping pattern data or None if request fails
        """
        endpoint = f'/v3/pattern/run/{run_ref}/route_type/{route_type}'
        params = kwargs
        return self._make_request(endpoint, params=params)

    def get_routes(self, **kwargs):
        """
        View route names and numbers for all routes.

        :param kwargs: Optional keyword arguments for filtering:
            - route_types (list[int]): Filter by route_type; values returned via RouteTypes API.
            - route_name (str): Filter by name of route (accepts partial route name matches).

        :return: Dictionary of routes data or None if request fails
        """
        endpoint = '/v3/routes'
        params = kwargs
        return self._make_request(endpoint, params=params)

    def get_route_by_id(self, route_id: int, **kwargs):
        """
        View route name and number for a specific route ID.

        :param route_id: Identifier of route; values returned by Departures, Directions, and Disruptions APIs
        :param kwargs: Optional keyword arguments for additional details:
            - include_geopath (bool): Indicates if geopath data will be returned.
            - geopath_utc (str): Filter geopaths by date in UTC format.

        :return: Dictionary of route data or None if request fails
        """
        endpoint = f'/v3/routes/{route_id}'
        params = kwargs
        return self._make_request(endpoint, params=params)

    def get_route_types(self):
        """
        View all route types and their names.

        :return: Dictionary of route types data or None if request fails
        """
        endpoint = '/v3/route_types'
        return self._make_request(endpoint)

    def get_runs_for_route(self, route_id: int, **kwargs):
        """
        View all trip/service runs for a specific route ID.

        :param route_id: Identifier of route; values returned by Routes API
        :param kwargs: Optional keyword arguments for additional details:
            - expand (list[str]): Fields to expand in the response.
            - date_utc (str): Filter by specific date in UTC format.
            - include_advertised_interchange (bool): Include advertised interchange.

        :return: Dictionary of runs data or None if request fails
        """
        endpoint = f'/v3/runs/route/{route_id}'
        params = kwargs
        return self._make_request(endpoint, params=params)

    def get_stops_near_location(self, latitude: float, longitude: float, max_results: int = 30, **kwargs):
        """
        View all stops near a specific location.

        :param latitude: Geographic coordinate of latitude
        :param longitude: Geographic coordinate of longitude
        :param max_results: Maximum number of results to return
        :param kwargs: Optional keyword arguments for additional filtering:
            - route_types (list[int]): Filter by route_type; values returned via RouteTypes API.
            - max_distance (float): Maximum distance from the location in meters.
            - stop_disruptions (bool): Indicates if stop disruption information will be returned.

        :return: Dictionary of stops near location data or None if request fails
        """
        endpoint = f'/v3/stops/location/{latitude},{longitude}'
        params = {'max_results': max_results, **kwargs}
        return self._make_request(endpoint, params=params)