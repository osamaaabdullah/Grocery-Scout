#import json
import json
#import doctest
import doctest


#method to get all the urls in the current JSON data
def get_url(list_of_grocery_items: list) -> list:
    """
    >>> get_url([{"url": "fb.com", "name": "osama"}, {"url": "ab.com","name": "osama"}])
    ['fb.com', 'ab.com']
    """
    grocery_item_urls = []
    for item in list_of_grocery_items:
        grocery_item_urls.append(item['url'])
        
    return grocery_item_urls

#method to check if a current url exists in the JSON data, if it exists return the index position
def url_index(grocery_item_urls: list, url: str)->int:
    """
    >>> url_index(['fb.com', 'ab.com'], 'fb.com')
    0
    >>> url_index(['fb.com', 'ab.com'], 'osama.com')
    -1
    """
    for url_link in grocery_item_urls:
        if url_link == url:
            return grocery_item_urls.index(url_link)
    return -1

def update_grocery_item(list_of_grocery_items:list, url: str, title: str, price: int):
    """
    >>> update_grocery_item([{"url": "fb.com", "name": "item1", "price": 5}], "osama.com", 'Osama', 10)
    >>> update_grocery_item([{'url': 'fb.com', 'name': 'osama'}, {'url': 'ab.com', 'name': 'osama'}], 'fb.com', 'love', 15)
    """
    
    
    grocery_item_urls = get_url(list_of_grocery_items)
    index = url_index(grocery_item_urls, url)
    if index == -1:
        product_data = {
            "url": url,
            "product name": title,
            "price": price
            } 
        list_of_grocery_items.append(product_data)
    else:
        list_of_grocery_items[index]["product name"] = title
        list_of_grocery_items[index]["price"] = price


with open("data.json") as read_file:
    data = json.load(read_file)
    
list_of_grocery_items = data['items']
#product_path = ['items']


def write_file(list_of_grocery_items: list):
    update_file = {'items': list_of_grocery_items}
    with open("data.json", mode = "w", encoding="utf-8") as write_file:
        json.dump(update_file,write_file, indent=4)
        write_file.write("\n"+ "\n")

doctest.testmod()