from hashlib import sha1
import hmac
import requests


def get_url(request: str, api_key: str, developer_id: int, base_url: str = 'https://timetableapi.ptv.vic.gov.au') -> str:
    """
    Code taken from Public Transport Victoria's API documentation
    :param request: The original request URL
    :param developer_id: PTV Developer ID
    :param api_key: PTV API Key
    :param base_url: PTV API Base URL, defaults to 'https://timetableapi.ptv.vic.gov.au'
    :return: Request URL with signature
    """
    request = request + ('&' if ('?' in request) else '?')
    raw = bytes(request + f'devid={developer_id}', 'UTF-8')

    hashed = hmac.new(bytes(api_key, 'UTF-8'), raw, sha1)
    signature = hashed.hexdigest()
    return base_url + str(raw, 'UTF-8') + f'&signature={signature}'


def validate_key(api_key: str, developer_id: int) -> bool:
    """
    Validates the auth details by using /v3/route_types endpoint.
    :param developer_id: PTV Developer ID
    :param api_key: PTV API Key
    :return: True if the API key and Developer ID validates, otherwise False
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
    ptv_developer_id = int(os.getenv('PTV_DEVELOPER_ID'))
    print("PTV API Key:", ptv_api_key)
    print("PTV Developer ID:", ptv_developer_id, "\n")

    print("Sending request for route types...")
    assert validate_key(ptv_api_key, ptv_developer_id), f"Unsuccessful request"
    print("Successful request")
