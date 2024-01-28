import json

import requests

explorer_url = "https://api.ergoplatform.com/api/v1"

def get_interest_param_box(address, nft):
    potential_boxes = get_unspent_boxes_by_address(address)
    for box in potential_boxes:
        if len(box["assets"]) > 0 and box["assets"][0]["tokenId"] == nft:
            return box
    return None

def get_request(url, max_retries=5):
    """
    Perform an HTTP GET request with retries upon receiving a non-200 status code.

    :param url: The URL to send the GET request to.
    :param headers: The headers to include in the GET request.
    :param max_retries: The maximum number of retries before giving up.
    :return: The response object, or 404 if the final status code is 404.
    """
    for attempt in range(max_retries):
        response = requests.get(url)
        if response.status_code == 200:
            return response
        if response.status_code == 404:
            return 404
    return None


def get_unspent_boxes_by_address(addr, limit=50, offset=0):
    return json.loads(get_request(f"{explorer_url}/boxes/unspent/byAddress/{addr}?limit={limit}&offset={offset}").text)['items']
