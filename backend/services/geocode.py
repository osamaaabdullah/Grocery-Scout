import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GEOCODE_API_KEY"))


def get_geocode_from_postal(postal_code:str) -> dict:
    postal_code = postal_code.strip().replace(' ', '')
    if (len(postal_code) == 6 and 
        postal_code[0].isalpha() and postal_code[1].isnumeric() and 
        postal_code[2].isalpha() and postal_code[3].isnumeric() and 
        postal_code[4].isalpha() and postal_code[5].isnumeric()):
        try:
            geocode_result = gmaps.geocode(f'{postal_code}, CA')
            if geocode_result:
                return geocode_result[0].get("geometry", {}).get("location")
            return {"message": "No results found"}
        except Exception as e:
            return {"message": e}
    
    return {"message": "Invalid postal code"}        
