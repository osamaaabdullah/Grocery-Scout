#import json
import json
#import doctest
import doctest


def get_store_items(store_name: str) -> dict:
    """
    Get the dictionary of items given store name
    
    >>> get_store_items('No Frills')
    {'https://www.nofrills.ca/large-grade-a-eggs/p/20812144001_EA\\n': {'product name': 'Large Grade A Eggs', 'price': 3.93, 'stock': 'available'}, 'https://www.nofrills.ca/boneless-skinless-chicken-breast/p/21430671_EA\\n': {'product name': 'Boneless Skinless Chicken Breast', 'price': 26.0, 'stock': 'available'}, 'https://www.nofrills.ca/100-coconut-water/p/20570506_EA\\n': {'product name': '100% Coconut Water', 'price': 2.99, 'stock': 'available'}}
    """
    
    with open("data.json") as read_file:
        data = json.load(read_file)
        
    dict_of_items = data[store_name]
    return dict_of_items


def item_exists(store_name: str, url: str) -> bool:
    """
    Retrieve the dictionary of items for a store and check if an item exists in the dictionary
    >>> item_exists('No Frills', 'https://www.nofrills.ca/boneless-skinless-chicken-breast/p/21430671_EA\\n')
    True
    
    >>> item_exists('No Frills', 'https://www.nofrills.ca/blueberries-1-2-pint/p/20152465001_EA\\n')
    False
    """
    
    store_items = get_store_items(store_name)
    store_items_url = store_items.keys()
    return url in store_items_url

def add_item(store_name: str, url: str, product_name: str, price: float, stock: str) ->dict:
    """Given that an item for a given url does not exist, add that item into the dictionary, else update the item"""
    
    current_items = get_store_items(store_name)
    current_items[url] = {
        'product_name': product_name,
        'price': price,
        'stock': stock
    }
    return current_items

def write_file(store_name: str, current_items: dict):
    with open("data.json") as read_file:
        data = json.load(read_file)        
    
    data[store_name] = current_items
    with open("data.json", mode = "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4)
        write_file.write("\n"+ "\n")

"""
problems so far
- url that is incorrect
- url but with out of stock



way later
- location problem
"""



if __name__ == '__main__':
    #add_item('No Frills', 'https://www.nofrills.ca/breakfast-sausage/p/21399630_EA', 'Breakfast Sausage', 9.99, 'available')
    doctest.testmod()