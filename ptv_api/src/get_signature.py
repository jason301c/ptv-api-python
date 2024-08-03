from hashlib import sha1
import hmac


def get_url(request: str, developer_id: int, api_key: str,
            base_url: str = 'https://timetableapi.ptv.vic.gov.au') -> str:
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


if __name__ == '__main__':
    """
    Signature generation test
    """
    from dotenv import load_dotenv
    import os
    import requests
    print("Testing signature generation, ensure you have the API key and Developer ID inside ptv_api/.env\n")

    load_dotenv('../.env')
    ptv_api_key = os.getenv('PTV_API_KEY')
    ptv_developer_id = int(os.getenv('PTV_DEVELOPER_ID'))
    print("PTV API Key:", ptv_api_key)
    print("PTV Developer ID:", ptv_developer_id, "\n")
    print("Sending request for route types...")

    req = requests.get(get_url('/v3/route_types', ptv_developer_id, ptv_api_key))

    assert req.status_code == 200, f"Unsuccessful request code {req.status_code}, check your API key and Developer ID"
    print("Successful request:", req.json(), "\n")