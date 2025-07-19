import requests
from urban_fare_db_writer import save_scraped_data

def get_response(url, page, skip):
    
    cookies = {
        '_gcl_au': '1.1.905722945.1747460953',
        '_ga': 'GA1.1.1870849172.1747460954',
        '_fbp': 'fb.1.1747460953656.80605672842488338',
        '__exponea_etc__': '55873bc3-f2e4-4619-ae82-c6cf87d954fa',
        '_pin_unauth': 'dWlkPVpHRTVNek13TlRRdFlXTmxNUzAwWWpKaExXRTRZalV0TlRObE5HSXpabVZoWWpnNQ',
        '__cf_bm': '4BJc9G05CCIEiXNyCndSWvBgirK0RPcJ.3g5I_QRRNM-1750636311-1.0.1.1-n6qLRmKvA40immahjh.vtB3tSmH1MIEJGEc2RRoyIbEXGOrFiB4u4xLnEbC6jPQnEDbIF6hN_QnuYFPLQPJbRvGxkyKcoxk2PGcxFDW0xMU',
        'cf_clearance': 'kW6NbmCvBUrMhPYJd5aQO.Veg1yIUH1.tQH5chmCF20-1750636311-1.2.1.1-ITIpNOgev8wa64ftiYYCzD2vTaBPpYLnnfWF4as.Yt.VMNRZ55hG_zKd_Bxl39ZrnroiGvmaLz95ozjE39lIks0OhzDlp8gOOk3Zlovr_KIOobReNLw6PvVLKUWg1RGDbGnQ.yhsaGopTrHuxEJpADpjeVVAd.BDQkI7iKzF28QEIuMq_2flBviT3sh_FWh3RS2DmMnP5YV.X6enEsjeo3HILrmjBhgcM2EeUrf9HAjQHkbszvxib8Rihzvh3i9iaZe1TMpuaofxcABO1l.aGUkbneS_I54uW0fvaJ.67VHuzMUPFiELyy7F5_2E7CgELNtmWQkmqY2iQ96Sq8_SlhdHwulww2jqeRSzxCDIl8E',
        '_clck': '1qgz2w1%7C2%7Cfwz%7C0%7C1963',
        '__exponea_time2__': '0.22213959693908691',
        '_clsk': '54rsuh%7C1750636346547%7C5%7C1%7Ci.clarity.ms%2Fcollect',
        '_ga_ZM4WBLPQ9B': 'GS2.1.s1750636312$o4$g1$t1750636354$j18$l0$h0',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.urbanfare.com',
        'priority': 'u=1, i',
        'referer': 'https://www.urbanfare.com/',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'x-correlation-id': '091a7147-dd38-4a20-959e-53e615a95715',
        'x-customer-session-id': 'https://www.urbanfare.com|78100a22-0b1a-4d13-ad57-53254cc4fcae',
        'x-shopping-mode': '11111111-1111-1111-1111-111111111111',
        'x-site-host': 'https://www.urbanfare.com',
        'x-site-location': 'HeadersBuilderInterceptor',
        # 'cookie': '_gcl_au=1.1.905722945.1747460953; _ga=GA1.1.1870849172.1747460954; _fbp=fb.1.1747460953656.80605672842488338; __exponea_etc__=55873bc3-f2e4-4619-ae82-c6cf87d954fa; _pin_unauth=dWlkPVpHRTVNek13TlRRdFlXTmxNUzAwWWpKaExXRTRZalV0TlRObE5HSXpabVZoWWpnNQ; __cf_bm=4BJc9G05CCIEiXNyCndSWvBgirK0RPcJ.3g5I_QRRNM-1750636311-1.0.1.1-n6qLRmKvA40immahjh.vtB3tSmH1MIEJGEc2RRoyIbEXGOrFiB4u4xLnEbC6jPQnEDbIF6hN_QnuYFPLQPJbRvGxkyKcoxk2PGcxFDW0xMU; cf_clearance=kW6NbmCvBUrMhPYJd5aQO.Veg1yIUH1.tQH5chmCF20-1750636311-1.2.1.1-ITIpNOgev8wa64ftiYYCzD2vTaBPpYLnnfWF4as.Yt.VMNRZ55hG_zKd_Bxl39ZrnroiGvmaLz95ozjE39lIks0OhzDlp8gOOk3Zlovr_KIOobReNLw6PvVLKUWg1RGDbGnQ.yhsaGopTrHuxEJpADpjeVVAd.BDQkI7iKzF28QEIuMq_2flBviT3sh_FWh3RS2DmMnP5YV.X6enEsjeo3HILrmjBhgcM2EeUrf9HAjQHkbszvxib8Rihzvh3i9iaZe1TMpuaofxcABO1l.aGUkbneS_I54uW0fvaJ.67VHuzMUPFiELyy7F5_2E7CgELNtmWQkmqY2iQ96Sq8_SlhdHwulww2jqeRSzxCDIl8E; _clck=1qgz2w1%7C2%7Cfwz%7C0%7C1963; __exponea_time2__=0.22213959693908691; _clsk=54rsuh%7C1750636346547%7C5%7C1%7Ci.clarity.ms%2Fcollect; _ga_ZM4WBLPQ9B=GS2.1.s1750636312$o4$g1$t1750636354$j18$l0$h0',
    }

    params = {
        'take': '30',
        'skip': skip,
        'page': page,
        'f': 'Breadcrumb:grocery/fruits & vegetables/fresh vegetables',
    }

    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    
    return response

def scrape(url):
    page = 1
    skip = 0
    product_list = []
    
    while True:
        response = get_response(url,page,skip)
        data = response.json()
        item_list = data["items"]
        if not item_list:
            break
        product_list.extend([(item.get("productId"), item.get("name"), item.get("pricePerUnit"), item.get("price"), item.get("wasPrice")) for item in item_list])
        page +=1
        skip +=30 
    
    return product_list

if __name__ == "__main__":
    url = 'https://storefrontgateway.urbanfare.com/api/stores/7615/categories/30694/search'
    data = scrape(url)
    save_scraped_data(data)