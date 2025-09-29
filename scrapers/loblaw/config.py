STORE_CONFIG = {
        "Loblaws": {
            'cartId': 'c3a2b386-14c9-45f1-9e98-fa5a6f96001f',
            'domainUserId': 'e11bad8f-e8e3-497f-b2b0-8e550e69af8b',
            'sessionId': 'af7ee6d4-fd91-4341-8eb6-99648d589b3f',
            'banner': 'loblaw'
        },

        "Zehrs": {
            'cartId': '345ea88e-2a1a-43b7-a8ea-12ff49587122',
            'domainUserId': '5c1613b1-35e5-44eb-8571-dba6df654906',
            'sessionId': '6fe7854a-69ab-401d-99be-492a270b7b8a',
            'banner': 'zehrs'
        },
        
        "Independent": {
            'cartId': 'b82bbb3f-956a-4a9f-9f9a-e521fbe826e6',
            'domainUserId': '52507a42-36c4-424c-84ca-2591d96bc65e',
            'sessionId': '82140c40-61f9-4544-9ec3-57bb446b2bab',
            'banner': 'independent'
        },

        "Valu-Mart": {
            'cartId': 'db6814a3-a702-4fd0-894c-ad745a22573d',
            'domainUserId': '82289e20-2bb3-462b-bf08-d3dd594942f1',
            'sessionId': 'b55cbf9f-0af3-4413-8ca8-ca0ea6c08c79',
            'banner': 'valumart'
        },
        
        "Real Atlantic Superstore": {
            'cartId': '4060196b-bca7-4a7c-a605-ebcb6b828322',
            'domainUserId': '000366bd-fa19-4d58-9c71-882f4524f09f',
            'sessionId': 'a3cd3dd7-55df-4c01-897b-515e2229db37',
            'banner': 'rass'
        },
        
        "Real Canadian Superstore": {
            'cartId': '17edfc36-ef48-4414-9abf-15a9add443cd',
            'domainUserId': '65b41b41-866e-486a-a6b6-d0396ddc41c6',
            'sessionId': '76b98e93-4ac6-4e44-bfb9-0e8637ac3c18',
            'banner': 'superstore'
        },
        "No Frills": {
            'cartId': '0c85a4d3-fc9c-47b7-afee-5b65d964d06e',
            'domainUserId': 'a4a4c09c-0a83-4f26-a19f-b783f8da95aa',
            'sessionId': '83b5d0ac-7c34-466c-8906-7bfff5a61389',
            'banner': 'nofrills'
        }
    }

API_ENDPOINTS = {
    "product_url": "http://127.0.0.1:8000/products",
    "price_url": "http://127.0.0.1:8000/prices",
    "province_price_url": "http://127.0.0.1:8000/province/prices",
    "price_history_url": "http://127.0.0.1:8000/price/history/",
}

TEST_CATEGORY_LIST = ["28195", "28194"]
TEST_STORE_LIST = [
    {
        "retailer": "Loblaws",
        "province_stores": [
            {
                "store_id": 1011,
                "province": "ON",
            }
        ],
    },
    
    {
        "retailer": "Zehrs",
        "province_stores": [
            {
                "store_id": 505,
                "province": "ON",
            }
        ],
    },
    
    {
        "retailer": "Independent",
        "province_stores": [
            {
                "store_id": 1892,
                "province": "AB",
            },
            {
                "store_id": 7533,
                "province": "ON",
            },
        ],
    },
    
    {
        "retailer": "Valu-Mart",
        "province_stores": [
            {
                "store_id": 9487,
                "province": "ON",
            },
            {
                "store_id": 7890,
                "province": "QC",
            }
        ],
    },
    
    {
        "retailer": "Real Canadian Superstore",
        "province_stores": [
            {
                "store_id": 1567,
                "province": "AB",
            },
            {
                "store_id": 2841,
                "province": "ON",
            },
            
        ],
    },
    
    {
        "retailer": "No Frills",
        "province_stores": [
            {
                "store_id": 3448,
                "province": "AB",
            },
            {
                "store_id": 4012,
                "province": "ON",
            },
            
        ],
    }
]

CATEGORY_LIST = ["28195", "28194", "28196", "28197", "28198", "28199", "28200", 
                "28224", "28222", "28220", "28225", "28227", "28221", "28226", "28223", "58904",
                "28214", "28174", "28170", "59252", "59253", "28215", "28171", "28173", "28216", "59318", "59319",
                "28187", "28186", "28247", "28246", "28183", "28184", "28248", "28244", "28243", "28188", "28185", "57088", "28245",
                "58466", "58467", "58468", "58469", "58466", "58046", "58309", "58311", "58045", "58498", "58499", "58500", "58501", "58502", "58498", "58557", "58559", "58560", "58558", "58561", "58568", "58563", "58570", "58561", "58812", "58813", "58814", "58816", "58812", "58680", "58687",
                "58685", "58690", "58680", "58801", "58802", "58809", "58804", "58801",
                "28250", "28249", "28242", "59210", "28162", "28163", "28165", "28238", "28164", "28239", "28241",
                "59260", "59271", "29713", "29714", "59391", "29717", "59302", "29924", "29925", "29927", "59320", "59339", "59374", "28251", "28147", "28148", "28149", "28150", "59494"]

STORE_LIST = [
    {
        "retailer": "Loblaws",
        "province_stores": [
            {
                "store_id": 4429,
                "province": "AB",
            },
            {
                "store_id": 7494,
                "province": "BC",
            },
            {
                "store_id": 1011,
                "province": "ON",
            }
        ],
    },
    
    {
        "retailer": "Zehrs",
        "province_stores": [
            {
                "store_id": 505,
                "province": "ON",
            }
        ],
    },
    
    {
        "retailer": "Independent",
        "province_stores": [
            {
                "store_id": 1892,
                "province": "AB",
            },
            {
                "store_id": 1789,
                "province": "BC",
            },
            {
                "store_id": 7470,
                "province": "NB",
            },
            {
                "store_id": 1417,
                "province": "NL",
            },
            {
                "store_id": 1414,
                "province": "NS",
            },
            {
                "store_id": 9798,
                "province": "NT",
            },
            {
                "store_id": 7533,
                "province": "ON",
            },
            {
                "store_id": 7170,
                "province": "PE",
            },
            {
                "store_id": 7152,
                "province": "SK",
            },
            {
                "store_id": 1806,
                "province": "YT",
            },
            
        ],
    },
    
    {
        "retailer": "Valu-Mart",
        "province_stores": [
            {
                "store_id": 9487,
                "province": "ON",
            },
            {
                "store_id": 7890,
                "province": "QC",
            }
        ],
    },
    
    {
        "retailer": "Real Atlantic Superstore",
        "province_stores": [
            {
                "store_id": 361,
                "province": "NB",
            },
            {
                "store_id": 373,
                "province": "NS",
            },
            {
                "store_id": 388,
                "province": "PE",
            },
            
        ],
    },
    
    {
        "retailer": "Real Canadian Superstore",
        "province_stores": [
            {
                "store_id": 1567,
                "province": "AB",
            },
            {
                "store_id": 1560,
                "province": "BC",
            },
            {
                "store_id": 1508,
                "province": "MB",
            },
            {
                "store_id": 2841,
                "province": "ON",
            },
            {
                "store_id": 1536,
                "province": "SK",
            },
            {
                "store_id": 1530,
                "province": "YT",
            },
            
        ],
    },
    
    {
        "retailer": "No Frills",
        "province_stores": [
            {
                "store_id": 3448,
                "province": "AB",
            },
            {
                "store_id": 3985,
                "province": "BC",
            },
            {
                "store_id": 3442,
                "province": "MB",
            },
            {
                "store_id": 9536,
                "province": "NB",
            },
            {
                "store_id": 2707,
                "province": "NL",
            },
            {
                "store_id": 2706,
                "province": "NS",
            },
            {
                "store_id": 4012,
                "province": "ON",
            },
            {
                "store_id": 9537,
                "province": "PE",
            },
            {
                "store_id": 7579,
                "province": "SK",
            },
            
        ],
    }
]

             
            
             
            
             