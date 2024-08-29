import requests

cookies = {
    'session-id': '131-8285060-6782665',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'sp-cdn': '"L5Z9:PE"',
    'ubid-main': '132-8907738-0217012',
    'lc-main': 'en_US',
    'csm-hit': 'tb:T1N5CQ8YPXPFJRJ8Z3DA+s-BR4Q9SYBMKMW0YM53281|1724434070370&t:1724434070370&adb:adblk_yes',
    'session-token': 'ZMwJX3oZmmrPMRC13eMI9y/XcizDsi42EHZETIfCxGhmL5GHMZg8p0+6JvVZGjfW7EZe5rlX4Gu983E/I3jJLXP2DuYWC9HvfrASYlcsjnwEliNaZbat9Zys5xp6bfYXVg9GkO8JtpFgMea8wmuJ472LOC03wdltiG0oIaRCps3okHyUj0uY5d/1hi4jFPTKlKg2XSBIFPmfPS8G1X5YHFTzuBvn9gAd4JiRsuA09E4te2MQwlpEuJmGP4Ujca1yTOf7zLpapJu0ckZBCEYCoyIWAgVBaAd5ZWGWl06u9pHLfxpNICX8K1UjcMGlifFCg2kK7Qn1uBceZjLck5gTvj8NvatkbYrE',
}

headers = {
    'accept': '*/*',
    'accept-language': 'es-419,es;q=0.9,en;q=0.8',
    'cookie': 'session-id=131-8285060-6782665; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:PE"; ubid-main=132-8907738-0217012; lc-main=en_US; csm-hit=tb:T1N5CQ8YPXPFJRJ8Z3DA+s-BR4Q9SYBMKMW0YM53281|1724434070370&t:1724434070370&adb:adblk_yes; session-token=ZMwJX3oZmmrPMRC13eMI9y/XcizDsi42EHZETIfCxGhmL5GHMZg8p0+6JvVZGjfW7EZe5rlX4Gu983E/I3jJLXP2DuYWC9HvfrASYlcsjnwEliNaZbat9Zys5xp6bfYXVg9GkO8JtpFgMea8wmuJ472LOC03wdltiG0oIaRCps3okHyUj0uY5d/1hi4jFPTKlKg2XSBIFPmfPS8G1X5YHFTzuBvn9gAd4JiRsuA09E4te2MQwlpEuJmGP4Ujca1yTOf7zLpapJu0ckZBCEYCoyIWAgVBaAd5ZWGWl06u9pHLfxpNICX8K1UjcMGlifFCg2kK7Qn1uBceZjLck5gTvj8NvatkbYrE',
    'device-memory': '8',
    'downlink': '10',
    'dpr': '1',
    'ect': '4g',
    'priority': 'u=1, i',
    'referer': 'https://www.amazon.com/dp/B0815XFSGK?th=1',
    'rtt': '100',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '1297',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'viewport-width': '1297',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'query': 'peso',
    'asin': 'B0815XFSGK',
    'forumId': '',
    'liveSearchSessionId': '12a26ec7-a1fd-4a9a-b7ac-57f1c284cb5b',
    'liveSearchPageLoadId': 'fef5d708-5338-4d61-94b2-c0ce215a5fb7',
    'searchSource': 'LIVE_SEARCH_SOURCE',
    'askLanguage': '',
    'isFromSecondaryPage': '',
}

response = requests.get(
    'https://www.amazon.com/ask/livesearch/detailPageSearch/search',
    params=params,
    headers=headers,
)

print(response.text)