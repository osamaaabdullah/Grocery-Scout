import json
import base64
import uuid
import time

def generate_cookie(store_id, postal_code, city, state):
    if not store_id or not postal_code:
        return None

    now_ms = int(time.time() * 1000)
    future_ms = now_ms + 5000

    acid = str(uuid.uuid4())

    location_data = {
        "intent": "PICKUP",
        "isExplicit": False,
        "storeIntent": "PICKUP",
        "mergeFlag": True,
        "isDefaulted": False,
        "pickup": {
            "nodeId": store_id,
            "timestamp": now_ms,
            "selectionType": "CUSTOMER_SELECTED",
            "selectionSource": "Pickup Store Selector"
        },
        "shippingAddress": {
            "timestamp": now_ms,
            "type": "partial-location",
            "giftAddress": False,
            "postalCode": postal_code,
            "deliveryStoreList": [
                {
                    "nodeId": store_id,
                    "type": "DELIVERY",
                    "timestamp": future_ms,
                    "deliveryTier": None,
                    "selectionType": "LS_SELECTED",
                    "selectionSource": "ZIP_CODE_BY_USER"
                }
            ],
            "city": city,
            "state": state
        },
        "postalCode": {
            "timestamp": now_ms,
            "base": postal_code
        },
        "mp": [],
        "mpDelStoreCount": 0,
        "showLocalExperience": False,
        "showLMPEntryPoint": False,
        "mpUniqueSellerCount": 0,
        "validateKey": f"prod:v3:{acid}"
    }

    encoded_loc_data = base64.urlsafe_b64encode(
        json.dumps(location_data, separators=(',', ':')).encode()
    ).decode()

    cookie = {'ACID': acid, 'hasACID': 'true', 'locDataV3': encoded_loc_data, 'locGuestData': encoded_loc_data}
    
    return cookie