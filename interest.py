import json
from math import floor

import requests

from consts import INTEREST_MULTIPLIER
from util import get_interest_param_box


def get_historical_rates(pool, address):
    # API endpoint
    api_url = f"https://api.ergoplatform.com/api/v1/boxes/unspent/byAddress/{address}"

    # Make the HTTP GET request
    response = requests.get(api_url)
    if response.status_code != 200:
        return f"Failed to fetch data: {response.status_code}"

    # Filter boxes with the specified token ID
    boxes = response.json()["items"]
    filtered_boxes = [
        box for box in boxes
        if box['assets'] and box['assets'][0]['tokenId'] == pool["CHILD_NFT"]
    ]

    # Order boxes by their R6 value
    ordered_boxes = sorted(
        filtered_boxes,
        key=lambda box: int(box['additionalRegisters']['R6']['renderedValue'])
    )

    # Concatenate rates from R4
    rates = []
    for box in ordered_boxes:
        rates.extend(json.loads(box['additionalRegisters']['R4']['renderedValue']))

    projected_borrow_rates = []
    for rate in rates:
        projected_borrow_rates.append((rate / INTEREST_MULTIPLIER) ** 2190)

    interest_param_box = get_interest_param_box(pool["interest_parameter"], pool["INTEREST_PARAMETER_NFT"])
    coefficients = json.loads(interest_param_box["additionalRegisters"]["R4"]["renderedValue"])

    projected_lender_apy = []
    for rate in rates:
        util = estimate_rate(pool, rate, coefficients)
        est = calculate_rate(coefficients, util)
        projected_lender_apy.append(1 + util * ((rate / INTEREST_MULTIPLIER) ** 2190 - 1))


    return {
        "raw_rates": rates,
        "projected_borrow_rates": projected_borrow_rates,
        "projected_lender_apy": projected_lender_apy
    }

def calculate_rate(coefficients, util):
    a = coefficients[0]
    b = coefficients[1]
    c = coefficients[2]
    d = coefficients[3]
    e = coefficients[4]
    f = coefficients[5]

    x = util * INTEREST_MULTIPLIER
    M = INTEREST_MULTIPLIER
    D = 100000000
    current_rate = floor(
        M + (
                a +
                floor(floor(b * x) / D) +
                floor(floor(floor(floor(c * x) / D) * x) / M) +
                floor(floor(floor(floor(floor(floor(d * x) / D) * x) / M) * x) / M) +
                floor(floor(floor(floor(floor(floor(floor(floor(e * x) / D) * x) / M) * x) / M) * x) / M) +
                floor(floor(
                    floor(floor(floor(floor(floor(floor(floor(floor(f * x) / D) * x) / M) * x) / M) * x) / M) * x) / M)
        )
    )
    return current_rate


def estimate_rate(pool, current_rate, coefficients):
    util = 0

    output_rate = calculate_rate(coefficients, util)
    while output_rate < current_rate:
        util += 0.005
        output_rate = calculate_rate(coefficients, util)

    return util
