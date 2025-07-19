import requests
import os
from dotenv import load_dotenv


def get_response():
    load_dotenv()
    headers = {
        'x-apikey': os.getenv("NO_FRILLS_X_API_KEY"),
    }

    params = {
        'bannerIds': 'nofrills',
    }

    response = requests.get('https://api.pcexpress.ca/pcx-bff/api/v1/pickup-locations', params=params, headers=headers)
    return response
