import requests

cookies = {
    'session-id': '131-8285060-6782665',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'sp-cdn': '"L5Z9:PE"',
    'ubid-main': '132-8907738-0217012',
    'lc-main': 'en_US',
    'session-token': 'm2KQgG8XTKURdEXYUp3S40OW0CtWIycXohDI+8V+vOm7OShxDzCUthruQwmZpopSPfzM9zOJuVqGMpvzGDtJUnbc+Poxk79ghifDGloeVyXnyY4kCn2i8K1TFvTDY9oCyx49f3wJBDph+HudeYktL0mWhtdIq0ZMExGSj5WmAkCYHKjjarUB7eaolVMcNV4Yq3fI6N78NMtVOr9oNFBTLlH2sZFHapSCeSahJexKwahXDxEO/YkaZ6cpXMjXbZJusinh7q+T7MIJxnRT18a0g9NtutCEij+erXhNS9Yz3sNUi9VDcoKCyUcQNamV5TUrDwJkrBIcaN2B4IbHrgD56fXqzngGcFJe',
    'csm-hit': 'tb:s-C8M0DRQ5VWTWTP0GGWQY|1726074434757&t:1726074438405&adb:adblk_yes',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'es-419,es;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'session-id=131-8285060-6782665; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:PE"; ubid-main=132-8907738-0217012; lc-main=en_US; session-token=m2KQgG8XTKURdEXYUp3S40OW0CtWIycXohDI+8V+vOm7OShxDzCUthruQwmZpopSPfzM9zOJuVqGMpvzGDtJUnbc+Poxk79ghifDGloeVyXnyY4kCn2i8K1TFvTDY9oCyx49f3wJBDph+HudeYktL0mWhtdIq0ZMExGSj5WmAkCYHKjjarUB7eaolVMcNV4Yq3fI6N78NMtVOr9oNFBTLlH2sZFHapSCeSahJexKwahXDxEO/YkaZ6cpXMjXbZJusinh7q+T7MIJxnRT18a0g9NtutCEij+erXhNS9Yz3sNUi9VDcoKCyUcQNamV5TUrDwJkrBIcaN2B4IbHrgD56fXqzngGcFJe; csm-hit=tb:s-C8M0DRQ5VWTWTP0GGWQY|1726074434757&t:1726074438405&adb:adblk_yes',
    'device-memory': '8',
    'downlink': '10',
    'dpr': '1',
    'ect': '4g',
    'priority': 'u=0, i',
    'rtt': '50',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '1304',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'viewport-width': '1304',
}

params = {
    'th': '1',
}

response = requests.get('https://www.amazon.com/dp/B0815XFSGK', params=params, cookies=cookies, headers=headers)

print(response.status_code)
print(response.text)