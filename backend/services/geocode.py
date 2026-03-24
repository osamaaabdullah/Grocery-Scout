import googlemaps
from backend.core.config import get_settings

settings = get_settings()

gmaps = googlemaps.Client(key=settings.geocode_api_key)

def is_valid_postal(postal_code: str) -> bool:
    return (len(postal_code) == 6 and 
            postal_code[0].isalpha() and postal_code[1].isnumeric() and 
            postal_code[2].isalpha() and postal_code[3].isnumeric() and 
            postal_code[4].isalpha() and postal_code[5].isnumeric())

def get_geocode_from_postal(postal_code:str) -> dict:
    postal_code = postal_code.strip().replace(' ', '')
    if not is_valid_postal(postal_code):
        return {"message": "Invalid postal code"} 
    try:
        geocode_result = gmaps.geocode(f'{postal_code}, CA')
        if geocode_result:
            return geocode_result[0].get("geometry", {}).get("location")
        return {"message": "No results found"}
    except Exception as e:
        return {"message": str(e)}

def postal_to_province(postal: str):
    """Helper function to convert postal code to province

    Args:
        postal (str): postal code

    Returns:
        _type_: Province Code
    """
    if not postal:
        return None
    mapping = {
        "A": "NL",
        "B": "NS",
        "C": "PE",
        "E": "NB",
        "G": "QC", "H": "QC", "J": "QC",
        "K": "ON", "L": "ON", "M": "ON", "N": "ON", "P": "ON",
        "R": "MB",
        "S": "SK",
        "T": "AB",
        "V": "BC",
        "X": "NT",
        "Y": "YT",
    }
    return mapping.get(postal[0].upper())
