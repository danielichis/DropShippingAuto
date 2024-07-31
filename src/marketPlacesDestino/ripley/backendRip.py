import copy
import json
import requests

cookies = {
    '_ga': 'GA1.3.397895214.1721248399',
    '_gid': 'GA1.3.1227843975.1722365107',
    '_hjSessionUser_1266356': 'eyJpZCI6IjMyZjFhMmJjLTBjYzUtNWMwZS04NzFlLTU4ZDJlM2E1MjExNiIsImNyZWF0ZWQiOjE3MjIzNjU1OTY2MTIsImV4aXN0aW5nIjp0cnVlfQ==',
    '_ga': 'GA1.1.397895214.1721248399',
    'XSRF-TOKEN': '82c723ea-eae1-45f9-b130-562cb3bd13e6',
    '_hjSession_1266356': 'eyJpZCI6IjEzZjRmOWY5LTBlNjgtNGZhNy05YWU5LTEzODFlOWIxNDQ5ZiIsImMiOjE3MjIzODcxMDgyMTMsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
    '_gat': '1',
    'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJta3BpbnRlckB1bmFsdWthLmNvbSIsImF1ZCI6InJpcGxleXBlcnUtcHJvZCIsImF1dGhlbnRpY2F0aW9uLW9yaWdpbiI6Ik1JUkFLTF9TU08iLCJleHRyYSI6eyJ0b3MiOiJ0cnVlIiwiYXV0aDAtaWQtdG9rZW4iOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0k2SWtwWFZDSXNJbXRwWkNJNklrNVVWVEJOVlVwRlVsVk5lVkpFVmtaUk1FVXpUWHBhUjAxVVJrWk9SR3QzVFRCT1JGRnFhelJOZWsxNVVsUkdSVkpGU1ROU1p5SjkuZXlKb2RIUndjem92TDIxcGNtRnJiQzVqYjIwdmNtOXNaWE1pT2xzaVpHOWpkVzFsYm5SaGRHbHZianBTVDB4RlgxTkZURXhGVWlKZExDSm9kSFJ3Y3pvdkwyMXBjbUZyYkM1amIyMHZiM0pwWjJsdUlqb2liV2x5WVd0c1gzTnpieUlzSW1oMGRIQnpPaTh2YldseVlXdHNMbU52YlM5c2IyTmhiR1VpT2lKbGN5SXNJbVZ0WVdsc0lqb2liV3R3YVc1MFpYSkFkVzVoYkhWcllTNWpiMjBpTENKbGJXRnBiRjkyWlhKcFptbGxaQ0k2ZEhKMVpTd2lhWE56SWpvaWFIUjBjSE02THk5c2IyZHBiaTV0YVhKaGEyd3VibVYwTHlJc0ltRjFaQ0k2SWxWT1VFSTBTMkpUZWpFd1drVjRSbmxTYzA1Uk5rcElZa3RDWlZjNU5HNXhJaXdpYVdGMElqb3hOekl5TXpnM01UQTNMQ0psZUhBaU9qRTNNakkwTWpNeE1EY3NJbk4xWWlJNkltRjFkR2d3ZkRZell6Z3dNR0UzWm1ZNE1qSmpabUUyTWpReFltWm1NaUlzSW5OcFpDSTZJa2hNTFZKSE1sZEdOemszZVhKSU5VcHdUR2t5VkZoUFIyTmlWVTV6VFVoVklpd2libTl1WTJVaU9pSlVOVTlDY0ZCVlozZHlNVVpNUVhCcFJuaE1XbVZYYnpoTlEwaGhWakpHTmxSdVRXVnNVR1JTTVdWVkluMC5hWVFtbFRKNjNMeDRwSW9qWWFNWnJlQl9fXzRSSUhrSXc2ckRuZ2hJWV9TRlRXdUI5ZUowV2lCTEduVVdERk9IOFlXVFg3eXRyRUExdGVSdlVIMFlCdUNKRDNoMVI4NGdndHgxTE12aUJQeFMzT0xYaEY5aTd5aFNYMldtY3VQZzZ6X3dFMFJpc00wQmdydmpYMV9EYmpta0hQdTBadkRvNENnYURBZHZ2TXYwS0tObG05RVVZdExHYmdwbVJNOWljZ0E2OFduaTRKc2gxYjZ4Ym10ZE9veHh1cXkyQ0dUQXlSV0NOWGRjeUdkUHUxTWxEZ3hTb0paMnZJZnNyRkFqNFVPTHVWNmJuNTA2QzkzMUZScE00aE9yenhEUHRqVGFqcWE2T3pqU2VwazFSNWo2RG9sMlVsOUtiTnJjam0wTF82c1JLNG96OENRSFNKMnlUYmp5T0EifSwiZXhwIjoxNzIyMzg5MDQ1LCJzaWQiOiJhZGVjODZiYS0wNThhLTRkYTAtODRhZi1mMmY3MWQ0ZDlmNTgifQ.kctnS7-X9v_7D8a9sfXMqu_dCpLy49-QtNC47t-EEfXRHJjLn1ZR56CGyqi1i1mSlq4u8A6sGTeAdMmYDp4UTg',
    '_ga_P32X25ZF51': 'GS1.3.1722387102.12.1.1722387244.0.0.0',
    '_ga_8THW8XBF2T': 'GS1.1.1722387109.5.1.1722387245.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'es-419,es;q=0.9',
    # 'cookie': '_ga=GA1.3.397895214.1721248399; _gid=GA1.3.1227843975.1722365107; _hjSessionUser_1266356=eyJpZCI6IjMyZjFhMmJjLTBjYzUtNWMwZS04NzFlLTU4ZDJlM2E1MjExNiIsImNyZWF0ZWQiOjE3MjIzNjU1OTY2MTIsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.397895214.1721248399; XSRF-TOKEN=82c723ea-eae1-45f9-b130-562cb3bd13e6; _hjSession_1266356=eyJpZCI6IjY3Y2NlYzQ2LWE3Y2QtNGJkOC04ODIxLTFlZDg3MzhmMGM4ZCIsImMiOjE3MjIzODQ3OTE2NzgsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _ga_P32X25ZF51=GS1.3.1722384783.11.1.1722384898.0.0.0; _ga_8THW8XBF2T=GS1.1.1722384793.4.1.1722384899.0.0.0; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJta3BpbnRlckB1bmFsdWthLmNvbSIsImF1ZCI6InJpcGxleXBlcnUtcHJvZCIsImF1dGhlbnRpY2F0aW9uLW9yaWdpbiI6Ik1JUkFLTF9TU08iLCJleHRyYSI6eyJ0b3MiOiJ0cnVlIiwiYXV0aDAtaWQtdG9rZW4iOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0k2SWtwWFZDSXNJbXRwWkNJNklrNVVWVEJOVlVwRlVsVk5lVkpFVmtaUk1FVXpUWHBhUjAxVVJrWk9SR3QzVFRCT1JGRnFhelJOZWsxNVVsUkdSVkpGU1ROU1p5SjkuZXlKb2RIUndjem92TDIxcGNtRnJiQzVqYjIwdmNtOXNaWE1pT2xzaVpHOWpkVzFsYm5SaGRHbHZianBTVDB4RlgxTkZURXhGVWlKZExDSm9kSFJ3Y3pvdkwyMXBjbUZyYkM1amIyMHZiM0pwWjJsdUlqb2liV2x5WVd0c1gzTnpieUlzSW1oMGRIQnpPaTh2YldseVlXdHNMbU52YlM5c2IyTmhiR1VpT2lKbGN5SXNJbVZ0WVdsc0lqb2liV3R3YVc1MFpYSkFkVzVoYkhWcllTNWpiMjBpTENKbGJXRnBiRjkyWlhKcFptbGxaQ0k2ZEhKMVpTd2lhWE56SWpvaWFIUjBjSE02THk5c2IyZHBiaTV0YVhKaGEyd3VibVYwTHlJc0ltRjFaQ0k2SWxWT1VFSTBTMkpUZWpFd1drVjRSbmxTYzA1Uk5rcElZa3RDWlZjNU5HNXhJaXdpYVdGMElqb3hOekl5TXpnME56a3dMQ0psZUhBaU9qRTNNakkwTWpBM09UQXNJbk4xWWlJNkltRjFkR2d3ZkRZell6Z3dNR0UzWm1ZNE1qSmpabUUyTWpReFltWm1NaUlzSW5OcFpDSTZJa1I1UlVSRVJFcDVTbkJUU1Zwa1lYUk1TalY2U1ZSbFR6SmxZVE5zZVhOcUlpd2libTl1WTJVaU9pSmpNMGxmWkhsc1lVazNSak4wU3pSd2FYZFZSWFE0WTB0SVIyOUVaWGw1VTBsUmNWTkxUR2hEWDNOTkluMC5Cd3BLUld5ejVsUTBucDNDSTF1YlQ2cEQ2OHc3ZE9BTHlSQUZQYVlZd1JWVHhkQmxmLWp5dnVtQ0xnRVBQbTVzNEVMWXduTGotYU1DRmI4MngxTkRPZi1TNUNkNHlxSnFFRWZmc05IR2s5QkdsZW83ZmhFbllHdUd5elVnZUN5aWM3Q0xLbFFmZzRfTmtMdzJSZVA2anNnWnIxeHJ4UzB6UjdFVFduci14SVZSNmhkcTZIbE4tUDVnTG9GZmkwVHViOHozZnFTajlzeHZ3dHA5eEZ2NGF6Nm0xSkdJRDFzWXFXbDBPbUNmVE1ISGdtSEpMSU56VVVMM25Fbnlqc0hoVnFYdS10VGZrMU1NQU9NT3Raalp2VnU5ODhKc0NKZTlJdmRXTlJGU0RYNnplNjNRVTF0eFNmM2NLY1pPSjNYUXRCcmE4TU13c2tGTzZZWXFESlhSS3cifSwiZXhwIjoxNzIyMzg2NzQyLCJzaWQiOiJiODQxNjI2My0xNDE2LTRkNzEtOGE5Ni1hMmE2MGFmYzkxOTMifQ.IeCghv86rpriCRbo5gg3ax7VBKVioCYjFm3MqAQmZL8jgtCjroGbEVOcYS9Suyf0zw47skbExO-J7Z42OYeGzA',
    'priority': 'u=1, i',
    'referer': 'https://ripleyperu-prod.mirakl.net/mmp/shop/catalog/template/configure?modelType=PRODUCTS_OFFERS',
    'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': '82c723ea-eae1-45f9-b130-562cb3bd13e6',
}

params = {
    'hierarchyCode': '',
    'selectedLocale': 'es_PE',
}


def generate_response(params,cookies,headers):
    
    response = requests.get(
        'https://ripleyperu-prod.mirakl.net/mmp/private/catalog/hierarchy/children',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    print(response)
    print(response.text)
    print(response.json())

    responseLoad=response.json()
    return responseLoad

def response_to_json(responseLoad,name:str):
    with open("DropShippingAuto/src/marketPlacesDestino/ripley/CategoriesTree/"+name+".json","w",encoding="utf-8") as json_file:
        json.dump(responseLoad,json_file,indent=4,ensure_ascii=False)


if __name__ == "__main__":
    responseLoad=generate_response(params,cookies,headers)
    response_to_json(responseLoad,"root_categories")
    print("Done")
    params_children=copy.deepcopy(params)
    for child in responseLoad:
        if child["children"]==True:
            print(child["code"]+"has children")
            params_children["hierarchyCode"]=child["code"]
            childResponse=generate_response(params_children,cookies,headers)
            response_to_json(childResponse,child["code"])
        else:
            print(child["code"]+"has no children")

    print("Done")