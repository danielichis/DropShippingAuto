import requests
from selectolax.parser import HTMLParser
import requests
import re
cookies = {
    'session-id': '138-3363892-2334805',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'sp-cdn': '"L5Z9:PE"',
    'ubid-main': '135-7500017-8187530',
    'lc-main': 'es_US',
    'csm-hit': 'tb:42029YQ73ZR4Z693WDX2+s-1K8W6D050VS3RN9YGNDS|1726945361664&t:1726945361664&adb:adblk_yes',
    'session-token': 'BCeB0cRWvX5aauM9Jjl7P80R/4cQw/ADCCGTPXq9VhQwpusheeH94NgYUJXID51fiCamFYVSJdfz2n2ovb51gBbCsWJ3ZG8kW/C5QhvmkWCVHJ1EEqjYMyGfZGw33Wf0Md5vbMH3v+X48laymcN6X9AHA8hT3zePSSCE+Vq7Od7lmBF8yEOw7e5Hf9TtrsmuOQsWmr6gBqtTp3qNCFmt7t6y8lyIXvL5CHpSpIoPwimEdvo7sRgHK5jiWpZLXxv/GLKwQaoTpie6ggQU3jR35azljWZ0mJgkwr7hSa/flyS5Dkaa6vVONezZ2yU4o0KBVE4Ffn96hYNtOFaD6fkrIxg6HSNxgMDd',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'es-419,es;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'session-id=138-3363892-2334805; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:PE"; ubid-main=135-7500017-8187530; lc-main=es_US; csm-hit=tb:42029YQ73ZR4Z693WDX2+s-1K8W6D050VS3RN9YGNDS|1726945361664&t:1726945361664&adb:adblk_yes; session-token=BCeB0cRWvX5aauM9Jjl7P80R/4cQw/ADCCGTPXq9VhQwpusheeH94NgYUJXID51fiCamFYVSJdfz2n2ovb51gBbCsWJ3ZG8kW/C5QhvmkWCVHJ1EEqjYMyGfZGw33Wf0Md5vbMH3v+X48laymcN6X9AHA8hT3zePSSCE+Vq7Od7lmBF8yEOw7e5Hf9TtrsmuOQsWmr6gBqtTp3qNCFmt7t6y8lyIXvL5CHpSpIoPwimEdvo7sRgHK5jiWpZLXxv/GLKwQaoTpie6ggQU3jR35azljWZ0mJgkwr7hSa/flyS5Dkaa6vVONezZ2yU4o0KBVE4Ffn96hYNtOFaD6fkrIxg6HSNxgMDd',
    'device-memory': '8',
    'downlink': '10',
    'dpr': '1',
    'ect': '4g',
    'priority': 'u=0, i',
    'rtt': '100',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '1297',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'viewport-width': '1297',
}

response = requests.get('https://www.amazon.com/dp/B0D7TQD8BF', cookies=cookies, headers=headers)
#print(response.text,"\n\n")
html=HTMLParser(response.text)
#save to html file

titulo=html.css_first("span[id='productTitle']").text()
try:
    precio=html.css_first("div[id='corePrice_feature_div'] span[class='a-offscreen']").text()
except:
    precio="No disponible"


#scripts=html.css("script")
print("titulo",titulo)
print("precio",precio)
for script in html.css("script"):
    if "ImageBlockATF" in script.text():
        print(script.text())