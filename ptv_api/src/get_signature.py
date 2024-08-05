from hashlib import sha1
import hmac
import requests
from urllib.parse import urlencode

def url_encode_params(params: dict) -> str:
    """
    Encoding the parameters into URL by using urllib.
    :param params: Parameters stored in a key value pair
    :return: Encoded string containing those parameters
    """
    params_list = []
    # Converts dict into list of tuples
    for k, v in params.items():
        if isinstance(v, list):
            params_list.extend([(k, x) for x in v])
        else:
            params_list.append((k, v))
    return urlencode(params_list)

def get_url(request: str, api_key: str, developer_id: int, params: dict = None, base_url: str = 'https://timetableapi.ptv.vic.gov.au') -> str:
    """
    Code partially taken from Public Transport Victoria's API documentation
    :param request: The original request URL
    :param developer_id: PTV Developer ID
    :param api_key: PTV API Key
    :param params: Additional query parameters
    :param base_url: PTV API Base URL, defaults to 'https://timetableapi.ptv.vic.gov.au'
    :return: Request URL with signature
    """
    # Replacing all spaces in request
    request = request.replace(" ", "%20")

    # Set default params argument to an empty dict
    if not params:
        params = {}

    # Forming request URL
    query_string = url_encode_params(params)
    request = request + ('&' if ('?' in request) else '?') + (f"{query_string}&" if len(query_string) > 0 else query_string)

    # Calculating signature
    raw = bytes(request + f'devid={developer_id}', 'UTF-8')
    hashed = hmac.new(bytes(api_key, 'UTF-8'), raw, sha1)
    signature = hashed.hexdigest()

    return base_url + str(raw, 'UTF-8') + f'&signature={signature}'


def validate_key(api_key: str, developer_id: int) -> bool:
    """
    Validates the auth details by using /v3/route_types endpoint.
    :param developer_id: PTV Developer ID
    :param api_key: PTV API Key
    :return: True if the API key and Developer ID authenticates successfully, otherwise False
    """
    request = requests.get(get_url('/v3/route_types', api_key, developer_id))
    if request.status_code == 200:
        return True
    else:
        return False



if __name__ == '__main__':
    """
    Signature generation test
    """
    from dotenv import load_dotenv
    import os

    print("Testing signature generation, ensure you have the API key and Developer ID inside ptv_api/.env\n")
    load_dotenv('../.env')
    ptv_api_key = os.getenv('PTV_API_KEY')
    ptv_developer_id = os.getenv('PTV_DEVELOPER_ID')

    if not (ptv_api_key or ptv_developer_id):
        raise ValueError("API Key / Developer ID not found! Provide .env file inside ptv_api/.env.")

    print("PTV API Key:", ptv_api_key)
    print("PTV Developer ID:", ptv_developer_id, "\n")

    print("Sending request for route types...")
    assert validate_key(ptv_api_key, int(ptv_developer_id)), f"Unsuccessful request"
    print("Successful request")
