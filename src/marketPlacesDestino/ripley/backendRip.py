import copy
import json
import requests

cookies = {
    '_ga': 'GA1.3.397895214.1721248399',
    '_hjSessionUser_1266356': 'eyJpZCI6IjMyZjFhMmJjLTBjYzUtNWMwZS04NzFlLTU4ZDJlM2E1MjExNiIsImNyZWF0ZWQiOjE3MjIzNjU1OTY2MTIsImV4aXN0aW5nIjp0cnVlfQ==',
    '_ga': 'GA1.1.397895214.1721248399',
    'XSRF-TOKEN': '82c723ea-eae1-45f9-b130-562cb3bd13e6',
    '_gid': 'GA1.3.576861606.1722559628',
    '_hjSession_1266356': 'eyJpZCI6IjljN2QyNjQ4LWVjYjQtNDYyZS05ZmYyLTgyZWM5M2QwZWNhOSIsImMiOjE3MjI1NjgwMTI2ODMsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
    '_gat': '1',
    '_ga_P32X25ZF51': 'GS1.3.1722568006.15.1.1722568080.0.0.0',
    'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJta3BpbnRlckB1bmFsdWthLmNvbSIsImF1ZCI6InJpcGxleXBlcnUtcHJvZCIsImF1dGhlbnRpY2F0aW9uLW9yaWdpbiI6Ik1JUkFLTF9TU08iLCJleHRyYSI6eyJ0b3MiOiJ0cnVlIiwiYXV0aDAtaWQtdG9rZW4iOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0k2SWtwWFZDSXNJbXRwWkNJNklrNVVWVEJOVlVwRlVsVk5lVkpFVmtaUk1FVXpUWHBhUjAxVVJrWk9SR3QzVFRCT1JGRnFhelJOZWsxNVVsUkdSVkpGU1ROU1p5SjkuZXlKb2RIUndjem92TDIxcGNtRnJiQzVqYjIwdmNtOXNaWE1pT2xzaVpHOWpkVzFsYm5SaGRHbHZianBTVDB4RlgxTkZURXhGVWlKZExDSm9kSFJ3Y3pvdkwyMXBjbUZyYkM1amIyMHZiM0pwWjJsdUlqb2liV2x5WVd0c1gzTnpieUlzSW1oMGRIQnpPaTh2YldseVlXdHNMbU52YlM5c2IyTmhiR1VpT2lKbGN5SXNJbVZ0WVdsc0lqb2liV3R3YVc1MFpYSkFkVzVoYkhWcllTNWpiMjBpTENKbGJXRnBiRjkyWlhKcFptbGxaQ0k2ZEhKMVpTd2lhWE56SWpvaWFIUjBjSE02THk5c2IyZHBiaTV0YVhKaGEyd3VibVYwTHlJc0ltRjFaQ0k2SWxWT1VFSTBTMkpUZWpFd1drVjRSbmxTYzA1Uk5rcElZa3RDWlZjNU5HNXhJaXdpYVdGMElqb3hOekl5TlRZNE1ERXhMQ0psZUhBaU9qRTNNakkyTURRd01URXNJbk4xWWlJNkltRjFkR2d3ZkRZell6Z3dNR0UzWm1ZNE1qSmpabUUyTWpReFltWm1NaUlzSW5OcFpDSTZJa1pxTWpaUFkwMWFiRFZsVW1aamJHbFNNbEozWDA5YWVXVTFaRGxGYkV4Tklpd2libTl1WTJVaU9pSXdZVk0wZFdocFZrbHdRMjVJTVZrdE5FVmtlbTVWZW5Bd2QxcERVMjR0Y0dGSmQyaG1lWEJWV0ZKbkluMC5VM0pONTUtdFFSeVpmWXdzTmZKc1J0dVpoY3V4Vjc2ZklqNl9fbEp1bTZDRk56NXFlMGt3Yl93OHA2RzNpWUVJTkpSdFkxb1IzdmZ1MmZxM2t5SlJxQmVaX2NEU3lPZjVRVWd1WUhnMG1mNFJXRi1mREtfSGtFMDFmdms5eWsyT252OENBN0pKeEJSTW41NHB1T3BzazRITWpydEZ1Zmt0RExKTWotck5BV1Rfai02d1A0RlhmZkZlb0NsNDBwYktIZFA0WjVpN2NDV3FGT0Mya3BPZ2tqNG5aRkcwLU5tblNFTkRYaHZnQm8wOVl2VFdWbC13akdMWE5yT3VZUnlKTmhWRkRKdzExNVVmaDVjeWVLR2JfeGM0Q2xjOUFWNHVVaXhLT2pDaHR5RnRmbF9oSjVXWWRuX1dzV0hTWlgwTndZTF9iWE1mTndHUGk1UFZDUVJ0SEEifSwiZXhwIjoxNzIyNTY5ODgyLCJzaWQiOiI2N2JjMTQ3Yi02MWQ1LTRhYjYtOTY4NC01NDJmMWM4YzNkMTgifQ.fD_lgfF_QyJqVuN5lVX_3XyHljzLyXC0BM3XrBxMO-aYnbz1USIjaRcrBlJaQbNF7IVcsLySW6DCQ07KW2N8tw',
    '_ga_8THW8XBF2T': 'GS1.1.1722568014.8.1.1722568083.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'es-419,es;q=0.9',
    # 'cookie': '_ga=GA1.3.397895214.1721248399; _hjSessionUser_1266356=eyJpZCI6IjMyZjFhMmJjLTBjYzUtNWMwZS04NzFlLTU4ZDJlM2E1MjExNiIsImNyZWF0ZWQiOjE3MjIzNjU1OTY2MTIsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.397895214.1721248399; XSRF-TOKEN=82c723ea-eae1-45f9-b130-562cb3bd13e6; _gid=GA1.3.576861606.1722559628; _hjSession_1266356=eyJpZCI6IjljN2QyNjQ4LWVjYjQtNDYyZS05ZmYyLTgyZWM5M2QwZWNhOSIsImMiOjE3MjI1NjgwMTI2ODMsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _gat=1; _ga_P32X25ZF51=GS1.3.1722568006.15.1.1722568080.0.0.0; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJta3BpbnRlckB1bmFsdWthLmNvbSIsImF1ZCI6InJpcGxleXBlcnUtcHJvZCIsImF1dGhlbnRpY2F0aW9uLW9yaWdpbiI6Ik1JUkFLTF9TU08iLCJleHRyYSI6eyJ0b3MiOiJ0cnVlIiwiYXV0aDAtaWQtdG9rZW4iOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0k2SWtwWFZDSXNJbXRwWkNJNklrNVVWVEJOVlVwRlVsVk5lVkpFVmtaUk1FVXpUWHBhUjAxVVJrWk9SR3QzVFRCT1JGRnFhelJOZWsxNVVsUkdSVkpGU1ROU1p5SjkuZXlKb2RIUndjem92TDIxcGNtRnJiQzVqYjIwdmNtOXNaWE1pT2xzaVpHOWpkVzFsYm5SaGRHbHZianBTVDB4RlgxTkZURXhGVWlKZExDSm9kSFJ3Y3pvdkwyMXBjbUZyYkM1amIyMHZiM0pwWjJsdUlqb2liV2x5WVd0c1gzTnpieUlzSW1oMGRIQnpPaTh2YldseVlXdHNMbU52YlM5c2IyTmhiR1VpT2lKbGN5SXNJbVZ0WVdsc0lqb2liV3R3YVc1MFpYSkFkVzVoYkhWcllTNWpiMjBpTENKbGJXRnBiRjkyWlhKcFptbGxaQ0k2ZEhKMVpTd2lhWE56SWpvaWFIUjBjSE02THk5c2IyZHBiaTV0YVhKaGEyd3VibVYwTHlJc0ltRjFaQ0k2SWxWT1VFSTBTMkpUZWpFd1drVjRSbmxTYzA1Uk5rcElZa3RDWlZjNU5HNXhJaXdpYVdGMElqb3hOekl5TlRZNE1ERXhMQ0psZUhBaU9qRTNNakkyTURRd01URXNJbk4xWWlJNkltRjFkR2d3ZkRZell6Z3dNR0UzWm1ZNE1qSmpabUUyTWpReFltWm1NaUlzSW5OcFpDSTZJa1pxTWpaUFkwMWFiRFZsVW1aamJHbFNNbEozWDA5YWVXVTFaRGxGYkV4Tklpd2libTl1WTJVaU9pSXdZVk0wZFdocFZrbHdRMjVJTVZrdE5FVmtlbTVWZW5Bd2QxcERVMjR0Y0dGSmQyaG1lWEJWV0ZKbkluMC5VM0pONTUtdFFSeVpmWXdzTmZKc1J0dVpoY3V4Vjc2ZklqNl9fbEp1bTZDRk56NXFlMGt3Yl93OHA2RzNpWUVJTkpSdFkxb1IzdmZ1MmZxM2t5SlJxQmVaX2NEU3lPZjVRVWd1WUhnMG1mNFJXRi1mREtfSGtFMDFmdms5eWsyT252OENBN0pKeEJSTW41NHB1T3BzazRITWpydEZ1Zmt0RExKTWotck5BV1Rfai02d1A0RlhmZkZlb0NsNDBwYktIZFA0WjVpN2NDV3FGT0Mya3BPZ2tqNG5aRkcwLU5tblNFTkRYaHZnQm8wOVl2VFdWbC13akdMWE5yT3VZUnlKTmhWRkRKdzExNVVmaDVjeWVLR2JfeGM0Q2xjOUFWNHVVaXhLT2pDaHR5RnRmbF9oSjVXWWRuX1dzV0hTWlgwTndZTF9iWE1mTndHUGk1UFZDUVJ0SEEifSwiZXhwIjoxNzIyNTY5ODgyLCJzaWQiOiI2N2JjMTQ3Yi02MWQ1LTRhYjYtOTY4NC01NDJmMWM4YzNkMTgifQ.fD_lgfF_QyJqVuN5lVX_3XyHljzLyXC0BM3XrBxMO-aYnbz1USIjaRcrBlJaQbNF7IVcsLySW6DCQ07KW2N8tw; _ga_8THW8XBF2T=GS1.1.1722568014.8.1.1722568083.0.0.0',
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

    #print(response)
    #print(response.text)
    #print(response.json())
    responseLoad=response.json()
    return responseLoad

def get_json_categories(category_code:str):
    
    category_params = {
    'hierarchyCode': '',
    'selectedLocale': 'es_PE',}

    category_params["hierarchyCode"]=category_code
    category_json= generate_response(category_params,cookies,headers)
    return category_json

def response_to_json(responseLoad,name:str):
    print("Saving response to json...")
    with open("DropShippingAuto/src/marketPlacesDestino/ripley/CategoriesTree/"+name+".json","w",encoding="utf-8") as json_file:
        json.dump(responseLoad,json_file,indent=4,ensure_ascii=False)

def get_children(child):
    if child["children"]==True:
        print(child["code"]+"has children")
        childResponse=get_json_categories(child["code"])
        child["child"]=childResponse
        for child in childResponse:
            get_children(child)
    else:
        print(child["code"]+"has no children")
        child["child"]=[]    

def get_children_w_path(parent):
    if parent["children"]==True:
        print(parent["code"]+"has children")
        childResponse=get_json_categories(parent["code"])
        parent["child"]=childResponse
        for child in parent["child"]:
            child["path"]=copy.deepcopy(parent["path"])
            child["path"].append(child["label"])
            get_children_w_path(child)
    else:
        print(parent["code"]+"has no children")
        
    
def get_categories_tree(root_categories_dict):
    for root_cat in root_categories_dict:
        get_children_w_path(root_cat)

def get_product_type_list():


    cookies = {
        '_ga': 'GA1.3.1709013107.1717449309',
        '_ga': 'GA1.1.1709013107.1717449309',
        '_hjSessionUser_1266356': 'eyJpZCI6IjQwY2JiZjY1LTE5ZWQtNTU5Yy1iYWRiLTNjMjM0YTVmY2RlMCIsImNyZWF0ZWQiOjE3MTc0NDkzODM1MzQsImV4aXN0aW5nIjp0cnVlfQ==',
        '_ga_8THW8XBF2T': 'deleted',
        '_ga_8THW8XBF2T': 'deleted',
        '_gid': 'GA1.3.1567928137.1725305542',
        'XSRF-TOKEN': '86c71d5d-1148-4a18-89e3-3d8ae2bf5d82',
        '_hjSession_1266356': 'eyJpZCI6IjFiNmRmMTMxLTU2YmMtNGRiNC1iZTRmLTQ0YjlmZTM5NjhiOCIsImMiOjE3MjUzMTQwNjkwNTksInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
        '_ga_8THW8XBF2T': 'GS1.1.1725314073.38.1.1725314224.0.0.0',
        'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJta3BpbnRlckB1bmFsdWthLmNvbSIsImF1ZCI6InJpcGxleXBlcnUtcHJvZCIsImF1dGhlbnRpY2F0aW9uLW9yaWdpbiI6Ik1JUkFLTF9TU08iLCJleHRyYSI6eyJ0b3MiOiJ0cnVlIiwiYXV0aDAtaWQtdG9rZW4iOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0k2SWtwWFZDSXNJbXRwWkNJNklrNVVWVEJOVlVwRlVsVk5lVkpFVmtaUk1FVXpUWHBhUjAxVVJrWk9SR3QzVFRCT1JGRnFhelJOZWsxNVVsUkdSVkpGU1ROU1p5SjkuZXlKb2RIUndjem92TDIxcGNtRnJiQzVqYjIwdmNtOXNaWE1pT2xzaVpHOWpkVzFsYm5SaGRHbHZianBTVDB4RlgxTkZURXhGVWlKZExDSm9kSFJ3Y3pvdkwyMXBjbUZyYkM1amIyMHZiM0pwWjJsdUlqb2liV2x5WVd0c1gzTnpieUlzSW1oMGRIQnpPaTh2YldseVlXdHNMbU52YlM5c2IyTmhiR1VpT2lKbGN5SXNJbVZ0WVdsc0lqb2liV3R3YVc1MFpYSkFkVzVoYkhWcllTNWpiMjBpTENKbGJXRnBiRjkyWlhKcFptbGxaQ0k2ZEhKMVpTd2lhWE56SWpvaWFIUjBjSE02THk5c2IyZHBiaTV0YVhKaGEyd3VibVYwTHlJc0ltRjFaQ0k2SWxWT1VFSTBTMkpUZWpFd1drVjRSbmxTYzA1Uk5rcElZa3RDWlZjNU5HNXhJaXdpYVdGMElqb3hOekkxTXpFME1EWTFMQ0psZUhBaU9qRTNNalV6TlRBd05qVXNJbk4xWWlJNkltRjFkR2d3ZkRZell6Z3dNR0UzWm1ZNE1qSmpabUUyTWpReFltWm1NaUlzSW1GamNpSTZJbWgwZEhBNkx5OXpZMmhsYldGekxtOXdaVzVwWkM1dVpYUXZjR0Z3WlM5d2IyeHBZMmxsY3k4eU1EQTNMekEyTDIxMWJIUnBMV1poWTNSdmNpSXNJbUZ0Y2lJNld5SnRabUVpWFN3aWMybGtJam9pU0VadFNGTnVibkozY1hSM1FURnhXVjgzUWxOalh6SkZXVmt6Y1VSZldHOGlMQ0p1YjI1alpTSTZJbTVGZDFCQ05HaHdZM0Z5TUMxWmFFSlRZMGwwT0Zod01HMURXWGxTVUhOTU5XUnBjVE5uTTFKSFlUQWlmUS5OWGNrcm9jTzZWZU5RUmxYRFdIRU96OVpQM1hiWUF2aldnVTEtX3BjT2VhcG1XcjVmZ0VRem13azdYWXhuZkp6RTRfQUk0UmkxWlBHelF4UTRLNXVSWU5qY1pka2F6X1l5aUNpLVhJcTlmMkdSU1F3SlZCbUhHaVYwUUQwaHRBTlFKNUdlLUVOQ1plaWl5QXJINk1wbHhaZVo5VEtCVkNCd0JuSmMwRF8tVTU1VVVvY1gzdnRIc21MRlJlYU9URWN4SFY2NkFOUTBCQnBWeWFmXzBXTWh5N0tHQ05saFZZYldtRjVfNEdmd2I4Q0tmMDIyZW9XNVFJVHV5VXR1QnpkOVJtLTZLb1ZFa3NiYW5IN3VZZ1lPREZmNG95dHU3N2VUYnJnMGxXb0xqVk8wczExcVg0NUhyUm8xclF1THNOSk56Z3prN3l3cmhWRXFwTlVLQmZZdncifSwiZXhwIjoxNzI1MzE3MzYzLCJzaWQiOiI3ZjZkOTIzOS0yYjIyLTRlODktOTM5Ny1iZmYwYTc4YzU5ZmEifQ.VaEeouSQghenIYVjXg1fQbTGw8Jn73A3a-LaoYOPysTH1pRtLjJ1HDKClXTurEQxy9z21ca4FKQQzvPC2JfCtw',
        'JSESSIONID': '064389472AFC7DFABDC8D644BB4FF64D',
        '_ga_P32X25ZF51': 'GS1.3.1725313953.95.1.1725315564.0.0.0',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'es-419,es;q=0.9',
        # 'cookie': '_ga=GA1.3.1709013107.1717449309; _ga=GA1.1.1709013107.1717449309; _hjSessionUser_1266356=eyJpZCI6IjQwY2JiZjY1LTE5ZWQtNTU5Yy1iYWRiLTNjMjM0YTVmY2RlMCIsImNyZWF0ZWQiOjE3MTc0NDkzODM1MzQsImV4aXN0aW5nIjp0cnVlfQ==; _ga_8THW8XBF2T=deleted; _ga_8THW8XBF2T=deleted; _gid=GA1.3.1567928137.1725305542; XSRF-TOKEN=86c71d5d-1148-4a18-89e3-3d8ae2bf5d82; _hjSession_1266356=eyJpZCI6IjFiNmRmMTMxLTU2YmMtNGRiNC1iZTRmLTQ0YjlmZTM5NjhiOCIsImMiOjE3MjUzMTQwNjkwNTksInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; _ga_8THW8XBF2T=GS1.1.1725314073.38.1.1725314224.0.0.0; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJta3BpbnRlckB1bmFsdWthLmNvbSIsImF1ZCI6InJpcGxleXBlcnUtcHJvZCIsImF1dGhlbnRpY2F0aW9uLW9yaWdpbiI6Ik1JUkFLTF9TU08iLCJleHRyYSI6eyJ0b3MiOiJ0cnVlIiwiYXV0aDAtaWQtdG9rZW4iOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0k2SWtwWFZDSXNJbXRwWkNJNklrNVVWVEJOVlVwRlVsVk5lVkpFVmtaUk1FVXpUWHBhUjAxVVJrWk9SR3QzVFRCT1JGRnFhelJOZWsxNVVsUkdSVkpGU1ROU1p5SjkuZXlKb2RIUndjem92TDIxcGNtRnJiQzVqYjIwdmNtOXNaWE1pT2xzaVpHOWpkVzFsYm5SaGRHbHZianBTVDB4RlgxTkZURXhGVWlKZExDSm9kSFJ3Y3pvdkwyMXBjbUZyYkM1amIyMHZiM0pwWjJsdUlqb2liV2x5WVd0c1gzTnpieUlzSW1oMGRIQnpPaTh2YldseVlXdHNMbU52YlM5c2IyTmhiR1VpT2lKbGN5SXNJbVZ0WVdsc0lqb2liV3R3YVc1MFpYSkFkVzVoYkhWcllTNWpiMjBpTENKbGJXRnBiRjkyWlhKcFptbGxaQ0k2ZEhKMVpTd2lhWE56SWpvaWFIUjBjSE02THk5c2IyZHBiaTV0YVhKaGEyd3VibVYwTHlJc0ltRjFaQ0k2SWxWT1VFSTBTMkpUZWpFd1drVjRSbmxTYzA1Uk5rcElZa3RDWlZjNU5HNXhJaXdpYVdGMElqb3hOekkxTXpFME1EWTFMQ0psZUhBaU9qRTNNalV6TlRBd05qVXNJbk4xWWlJNkltRjFkR2d3ZkRZell6Z3dNR0UzWm1ZNE1qSmpabUUyTWpReFltWm1NaUlzSW1GamNpSTZJbWgwZEhBNkx5OXpZMmhsYldGekxtOXdaVzVwWkM1dVpYUXZjR0Z3WlM5d2IyeHBZMmxsY3k4eU1EQTNMekEyTDIxMWJIUnBMV1poWTNSdmNpSXNJbUZ0Y2lJNld5SnRabUVpWFN3aWMybGtJam9pU0VadFNGTnVibkozY1hSM1FURnhXVjgzUWxOalh6SkZXVmt6Y1VSZldHOGlMQ0p1YjI1alpTSTZJbTVGZDFCQ05HaHdZM0Z5TUMxWmFFSlRZMGwwT0Zod01HMURXWGxTVUhOTU5XUnBjVE5uTTFKSFlUQWlmUS5OWGNrcm9jTzZWZU5RUmxYRFdIRU96OVpQM1hiWUF2aldnVTEtX3BjT2VhcG1XcjVmZ0VRem13azdYWXhuZkp6RTRfQUk0UmkxWlBHelF4UTRLNXVSWU5qY1pka2F6X1l5aUNpLVhJcTlmMkdSU1F3SlZCbUhHaVYwUUQwaHRBTlFKNUdlLUVOQ1plaWl5QXJINk1wbHhaZVo5VEtCVkNCd0JuSmMwRF8tVTU1VVVvY1gzdnRIc21MRlJlYU9URWN4SFY2NkFOUTBCQnBWeWFmXzBXTWh5N0tHQ05saFZZYldtRjVfNEdmd2I4Q0tmMDIyZW9XNVFJVHV5VXR1QnpkOVJtLTZLb1ZFa3NiYW5IN3VZZ1lPREZmNG95dHU3N2VUYnJnMGxXb0xqVk8wczExcVg0NUhyUm8xclF1THNOSk56Z3prN3l3cmhWRXFwTlVLQmZZdncifSwiZXhwIjoxNzI1MzE3MzYzLCJzaWQiOiI3ZjZkOTIzOS0yYjIyLTRlODktOTM5Ny1iZmYwYTc4YzU5ZmEifQ.VaEeouSQghenIYVjXg1fQbTGw8Jn73A3a-LaoYOPysTH1pRtLjJ1HDKClXTurEQxy9z21ca4FKQQzvPC2JfCtw; JSESSIONID=064389472AFC7DFABDC8D644BB4FF64D; _ga_P32X25ZF51=GS1.3.1725313953.95.1.1725315564.0.0.0',
        'priority': 'u=1, i',
        'referer': 'https://ripleyperu-prod.mirakl.net/mmp/shop/sell/product/create',
        'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': '86c71d5d-1148-4a18-89e3-3d8ae2bf5d82',
    }

    params = {
        'namedListId': '1646',
        'searchString': '',
        'pageSize': '100',
        'offset': '100',
        '_': '1725314220979',
    }

    response = requests.get(
        'https://ripleyperu-prod.mirakl.net/mmp/shop/setting/named-list/value/search-json',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    print(response.status_code)
    if response.status_code==200:
        print(response.json())
        print("Lista de productos obtenidos.")
        return response.json()
    else:
        print("Error al obtener la lista de productos.")
    

def create_product_ripley():
 

    cookies = {
        '_ga': 'GA1.3.1709013107.1717449309',
        '_ga': 'GA1.1.1709013107.1717449309',
        '_hjSessionUser_1266356': 'eyJpZCI6IjQwY2JiZjY1LTE5ZWQtNTU5Yy1iYWRiLTNjMjM0YTVmY2RlMCIsImNyZWF0ZWQiOjE3MTc0NDkzODM1MzQsImV4aXN0aW5nIjp0cnVlfQ==',
        '_ga_8THW8XBF2T': 'deleted',
        '_ga_8THW8XBF2T': 'deleted',
        '_gid': 'GA1.3.1963483883.1726083102',
        '_hjSession_1266356': 'eyJpZCI6IjUxNjRhMDE3LTk0ZTItNDEwMS1hNzIyLTc5N2FlMTcyZWJmZCIsImMiOjE3MjYwODMxMTE3MTAsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        'XSRF-TOKEN': '82e634a4-d175-43aa-b278-c855abaffecf',
        '_ga_8THW8XBF2T': 'GS1.1.1726083113.40.1.1726084261.0.0.0',
        'JSESSIONID': '72AE49F7BEC164125341D57B4C6E2EBA',
        'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJta3BpbnRlckB1bmFsdWthLmNvbSIsImF1ZCI6InJpcGxleXBlcnUtcHJvZCIsImF1dGhlbnRpY2F0aW9uLW9yaWdpbiI6Ik1JUkFLTF9TU08iLCJleHRyYSI6eyJ0b3MiOiJ0cnVlIiwiYXV0aDAtaWQtdG9rZW4iOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0k2SWtwWFZDSXNJbXRwWkNJNklrNVVWVEJOVlVwRlVsVk5lVkpFVmtaUk1FVXpUWHBhUjAxVVJrWk9SR3QzVFRCT1JGRnFhelJOZWsxNVVsUkdSVkpGU1ROU1p5SjkuZXlKb2RIUndjem92TDIxcGNtRnJiQzVqYjIwdmNtOXNaWE1pT2xzaVpHOWpkVzFsYm5SaGRHbHZianBTVDB4RlgxTkZURXhGVWlKZExDSm9kSFJ3Y3pvdkwyMXBjbUZyYkM1amIyMHZiM0pwWjJsdUlqb2liV2x5WVd0c1gzTnpieUlzSW1oMGRIQnpPaTh2YldseVlXdHNMbU52YlM5c2IyTmhiR1VpT2lKbGN5SXNJbVZ0WVdsc0lqb2liV3R3YVc1MFpYSkFkVzVoYkhWcllTNWpiMjBpTENKbGJXRnBiRjkyWlhKcFptbGxaQ0k2ZEhKMVpTd2lhWE56SWpvaWFIUjBjSE02THk5c2IyZHBiaTV0YVhKaGEyd3VibVYwTHlJc0ltRjFaQ0k2SWxWT1VFSTBTMkpUZWpFd1drVjRSbmxTYzA1Uk5rcElZa3RDWlZjNU5HNXhJaXdpYVdGMElqb3hOekkyTURnME1qRTNMQ0psZUhBaU9qRTNNall4TWpBeU1UY3NJbk4xWWlJNkltRjFkR2d3ZkRZell6Z3dNR0UzWm1ZNE1qSmpabUUyTWpReFltWm1NaUlzSW5OcFpDSTZJbk5OYmpjMmExOW5UM0JpVDNGelRYSlRaVzA0YUZjeVdqZFFVa013V2pJMklpd2libTl1WTJVaU9pSm1OMkV6T1VWbk0yOUJTWEpWYUVsTFVFcElVR2MyWmxSNWJrOTFSbWhIYlY4MmJFbDJaekIzUzA5ckluMC4yMEpmVExLd05KUFpGT0Q4eHJKaldwa2VEZFI1MjM3VzNudENlRUpPaFNJNUpsOUs1Z1lwVTdUX09aclRFWENzV2tWX19kMjVINkQ2RnlkcmpWNl9HYlcyLTBFdGV2U19wZV9nUlVBWmZGN0xyamNBVVJVVi1tU3MtV25sWVh0NHBEZVVGbFpGVmRkckRzMnk2cmozU0VSSmFLTEduS0pRSGlwbzkweUFuWEgxOWdpR3FzVmlFckhvSVZnUFY5ZjFvSnZZeEN5LUZ1VHRHanNiUG5sUElER2RTRHpHVm9tNHpnRkk3RWgzeVBSM0VHM1BlUlhjemk1WnMwcnNtczkxdXgzMTlwdWRNVFVzV29qWGFSLUFBUlY2c2FwSzRZemdsZXhidDVDRnY4aFJxQnp6bUZ3ZGVEZXBxVGgyVDBnWVY2YWp1N2NXWXFKUTJfbkR6c2ZqS0EifSwiZXhwIjoxNzI2MDg2MTc5LCJzaWQiOiI0MGViYWFjMS02NDYxLTQwODAtYjA1MC1mMmU5ZTdmNTkxOTgifQ.OG2Sx6fElrrSfaegG8iaWk6b3wTc0xpBpu1rnxCYfxNpscg0Y4_QAxmWK764dzoX4euB2o9W5QicD_nZcamMaA',
        '_ga_P32X25ZF51': 'GS1.3.1726083102.97.1.1726084379.0.0.0',
        '_gali': 'addProductAndOffer',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'es-419,es;q=0.9',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryBz3b4rH5ea2DhrAZ',
        # 'cookie': '_ga=GA1.3.1709013107.1717449309; _ga=GA1.1.1709013107.1717449309; _hjSessionUser_1266356=eyJpZCI6IjQwY2JiZjY1LTE5ZWQtNTU5Yy1iYWRiLTNjMjM0YTVmY2RlMCIsImNyZWF0ZWQiOjE3MTc0NDkzODM1MzQsImV4aXN0aW5nIjp0cnVlfQ==; _ga_8THW8XBF2T=deleted; _ga_8THW8XBF2T=deleted; _gid=GA1.3.1963483883.1726083102; _hjSession_1266356=eyJpZCI6IjUxNjRhMDE3LTk0ZTItNDEwMS1hNzIyLTc5N2FlMTcyZWJmZCIsImMiOjE3MjYwODMxMTE3MTAsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; XSRF-TOKEN=82e634a4-d175-43aa-b278-c855abaffecf; _ga_8THW8XBF2T=GS1.1.1726083113.40.1.1726084261.0.0.0; JSESSIONID=72AE49F7BEC164125341D57B4C6E2EBA; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJta3BpbnRlckB1bmFsdWthLmNvbSIsImF1ZCI6InJpcGxleXBlcnUtcHJvZCIsImF1dGhlbnRpY2F0aW9uLW9yaWdpbiI6Ik1JUkFLTF9TU08iLCJleHRyYSI6eyJ0b3MiOiJ0cnVlIiwiYXV0aDAtaWQtdG9rZW4iOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0k2SWtwWFZDSXNJbXRwWkNJNklrNVVWVEJOVlVwRlVsVk5lVkpFVmtaUk1FVXpUWHBhUjAxVVJrWk9SR3QzVFRCT1JGRnFhelJOZWsxNVVsUkdSVkpGU1ROU1p5SjkuZXlKb2RIUndjem92TDIxcGNtRnJiQzVqYjIwdmNtOXNaWE1pT2xzaVpHOWpkVzFsYm5SaGRHbHZianBTVDB4RlgxTkZURXhGVWlKZExDSm9kSFJ3Y3pvdkwyMXBjbUZyYkM1amIyMHZiM0pwWjJsdUlqb2liV2x5WVd0c1gzTnpieUlzSW1oMGRIQnpPaTh2YldseVlXdHNMbU52YlM5c2IyTmhiR1VpT2lKbGN5SXNJbVZ0WVdsc0lqb2liV3R3YVc1MFpYSkFkVzVoYkhWcllTNWpiMjBpTENKbGJXRnBiRjkyWlhKcFptbGxaQ0k2ZEhKMVpTd2lhWE56SWpvaWFIUjBjSE02THk5c2IyZHBiaTV0YVhKaGEyd3VibVYwTHlJc0ltRjFaQ0k2SWxWT1VFSTBTMkpUZWpFd1drVjRSbmxTYzA1Uk5rcElZa3RDWlZjNU5HNXhJaXdpYVdGMElqb3hOekkyTURnME1qRTNMQ0psZUhBaU9qRTNNall4TWpBeU1UY3NJbk4xWWlJNkltRjFkR2d3ZkRZell6Z3dNR0UzWm1ZNE1qSmpabUUyTWpReFltWm1NaUlzSW5OcFpDSTZJbk5OYmpjMmExOW5UM0JpVDNGelRYSlRaVzA0YUZjeVdqZFFVa013V2pJMklpd2libTl1WTJVaU9pSm1OMkV6T1VWbk0yOUJTWEpWYUVsTFVFcElVR2MyWmxSNWJrOTFSbWhIYlY4MmJFbDJaekIzUzA5ckluMC4yMEpmVExLd05KUFpGT0Q4eHJKaldwa2VEZFI1MjM3VzNudENlRUpPaFNJNUpsOUs1Z1lwVTdUX09aclRFWENzV2tWX19kMjVINkQ2RnlkcmpWNl9HYlcyLTBFdGV2U19wZV9nUlVBWmZGN0xyamNBVVJVVi1tU3MtV25sWVh0NHBEZVVGbFpGVmRkckRzMnk2cmozU0VSSmFLTEduS0pRSGlwbzkweUFuWEgxOWdpR3FzVmlFckhvSVZnUFY5ZjFvSnZZeEN5LUZ1VHRHanNiUG5sUElER2RTRHpHVm9tNHpnRkk3RWgzeVBSM0VHM1BlUlhjemk1WnMwcnNtczkxdXgzMTlwdWRNVFVzV29qWGFSLUFBUlY2c2FwSzRZemdsZXhidDVDRnY4aFJxQnp6bUZ3ZGVEZXBxVGgyVDBnWVY2YWp1N2NXWXFKUTJfbkR6c2ZqS0EifSwiZXhwIjoxNzI2MDg2MTc5LCJzaWQiOiI0MGViYWFjMS02NDYxLTQwODAtYjA1MC1mMmU5ZTdmNTkxOTgifQ.OG2Sx6fElrrSfaegG8iaWk6b3wTc0xpBpu1rnxCYfxNpscg0Y4_QAxmWK764dzoX4euB2o9W5QicD_nZcamMaA; _ga_P32X25ZF51=GS1.3.1726083102.97.1.1726084379.0.0.0; _gali=addProductAndOffer',
        'origin': 'https://ripleyperu-prod.mirakl.net',
        'priority': 'u=1, i',
        'referer': 'https://ripleyperu-prod.mirakl.net/mmp/shop/sell/product/create',
        'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': '82e634a4-d175-43aa-b278-c855abaffecf',
    }

    files = [
        ('_csrf', (None, '82e634a4-d175-43aa-b278-c855abaffecf')),
        ('label', (None, '2161399')),
        ('label', (None, '15584899')),
        ('attributeValuesFormCommand.attributeValues[0].operatorAttribute.code', (None, 'categoria')),
        ('attributeValuesFormCommand.attributeValues[0].operatorAttribute.id', (None, '1100')),
        ('attributeValuesFormCommand.attributeValues[0].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[1].operatorAttribute.id', (None, '1101')),
        ('attributeValuesFormCommand.attributeValues[1].disabled', (None, 'true')),
        ('attributeValuesFormCommand.attributeValues[2].attributeValue', (None, 'Pantuflas de mujer con cara sonriente, estilo retro, suaves, cálidas, sin cordones, acogedoras para interiores y exteriores.')),
        ('attributeValuesFormCommand.attributeValues[2].operatorAttribute.id', (None, '1102')),
        ('attributeValuesFormCommand.attributeValues[2].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[3].attributeValue', (None, 'Compra tu Pantuflas de cara sonriente en Ripley Internacional')),
        ('attributeValuesFormCommand.attributeValues[3].operatorAttribute.id', (None, '3781')),
        ('attributeValuesFormCommand.attributeValues[3].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[4].attributeValue', (None, '• Patrones divertidos: pantuflas de felpa de estilo retro con patrón de cara de sonrisa a la moda e interesante, el impacto de los elementos, ilumina tu buen estado de ánimo diario\n• Diseño perfecto: las pantuflas de la marca Coundymer cuentan con un diseño antideslizante y un cómodo forro de felpa sintética que envolverá tus pies muy bien y te proporcionará una comodidad cálida\n• Elección de regalo: las pantuflas sonrientes son el elemento clásico más popular hoy en día, disponibles en 7 colores, un regalo perfecto para ancianos, amantes y madres, con la esperanza de calentarlas este invierno\n• SKU:B0CY1R9CXC\n• Material de la suela:Caucho\n• Tipo de cierre:Sin cordones\n• Nivel de resistencia al agua:A prueba de agua\n')),
        ('attributeValuesFormCommand.attributeValues[4].operatorAttribute.id', (None, '1103')),
        ('attributeValuesFormCommand.attributeValues[4].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[5].attributeValue', (None, '379699333')),
        ('attributeValuesFormCommand.attributeValues[5].operatorAttribute.id', (None, '1104')),
        ('attributeValuesFormCommand.attributeValues[5].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[6].attributeValue', ('resizedImg_750x555_0.jpg', '', 'image/jpeg')),
        ('attributeValuesFormCommand.attributeValues[6].operatorAttribute.id', (None, '1105')),
        ('attributeValuesFormCommand.attributeValues[6].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[7].attributeValue', ('resizedImg_750x555_0.jpg', '', 'image/jpeg')),
        ('attributeValuesFormCommand.attributeValues[7].operatorAttribute.id', (None, '1109')),
        ('attributeValuesFormCommand.attributeValues[7].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[8].attributeValue', ('resizedImg_750x555_2.jpg', '', 'image/jpeg')),
        ('attributeValuesFormCommand.attributeValues[8].operatorAttribute.id', (None, '1533')),
        ('attributeValuesFormCommand.attributeValues[8].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[9].attributeValue', ('resizedImg_750x555_3.jpg', '', 'image/jpeg')),
        ('attributeValuesFormCommand.attributeValues[9].operatorAttribute.id', (None, '1534')),
        ('attributeValuesFormCommand.attributeValues[9].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[10].attributeValue', ('resizedImg_750x555_4.jpg', '', 'image/jpeg')),
        ('attributeValuesFormCommand.attributeValues[10].operatorAttribute.id', (None, '4137')),
        ('attributeValuesFormCommand.attributeValues[10].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[11].attributeValue', ('resizedImg_750x555_5.jpg', '', 'image/jpeg')),
        ('attributeValuesFormCommand.attributeValues[11].operatorAttribute.id', (None, '4138')),
        ('attributeValuesFormCommand.attributeValues[11].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[12].operatorAttribute.id', (None, '4139')),
        ('attributeValuesFormCommand.attributeValues[12].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[13].attributeValue', (None, '30')),
        ('attributeValuesFormCommand.attributeValues[13].operatorAttribute.id', (None, '1117')),
        ('attributeValuesFormCommand.attributeValues[13].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[14].attributeValue', (None, '36')),
        ('attributeValuesFormCommand.attributeValues[14].operatorAttribute.id', (None, '1116')),
        ('attributeValuesFormCommand.attributeValues[14].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[15].attributeValue', (None, '16')),
        ('attributeValuesFormCommand.attributeValues[15].operatorAttribute.id', (None, '1115')),
        ('attributeValuesFormCommand.attributeValues[15].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[16].attributeValue', (None, '0.28')),
        ('attributeValuesFormCommand.attributeValues[16].operatorAttribute.id', (None, '150774')),
        ('attributeValuesFormCommand.attributeValues[16].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[17].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[17].operatorAttribute.id', (None, '222409')),
        ('attributeValuesFormCommand.attributeValues[17].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[18].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[18].operatorAttribute.id', (None, '337333')),
        ('attributeValuesFormCommand.attributeValues[18].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[19].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[19].operatorAttribute.id', (None, '340442')),
        ('attributeValuesFormCommand.attributeValues[19].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[20].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[20].operatorAttribute.id', (None, '340461')),
        ('attributeValuesFormCommand.attributeValues[20].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[21].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[21].operatorAttribute.id', (None, '340312')),
        ('attributeValuesFormCommand.attributeValues[21].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[22].operatorAttribute.id', (None, '272493')),
        ('attributeValuesFormCommand.attributeValues[22].disabled', (None, 'true')),
        ('attributeValuesFormCommand.attributeValues[23].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[23].operatorAttribute.id', (None, '272494')),
        ('attributeValuesFormCommand.attributeValues[23].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[24].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[24].operatorAttribute.id', (None, '272495')),
        ('attributeValuesFormCommand.attributeValues[24].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[25].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[25].operatorAttribute.id', (None, '272496')),
        ('attributeValuesFormCommand.attributeValues[25].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[26].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[26].operatorAttribute.id', (None, '272497')),
        ('attributeValuesFormCommand.attributeValues[26].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[27].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[27].operatorAttribute.id', (None, '272498')),
        ('attributeValuesFormCommand.attributeValues[27].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[28].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[28].operatorAttribute.id', (None, '272499')),
        ('attributeValuesFormCommand.attributeValues[28].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[29].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[29].operatorAttribute.id', (None, '272500')),
        ('attributeValuesFormCommand.attributeValues[29].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[30].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[30].operatorAttribute.id', (None, '272501')),
        ('attributeValuesFormCommand.attributeValues[30].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[31].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[31].operatorAttribute.id', (None, '272502')),
        ('attributeValuesFormCommand.attributeValues[31].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[32].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[32].operatorAttribute.id', (None, '272503')),
        ('attributeValuesFormCommand.attributeValues[32].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[33].operatorAttribute.id', (None, '272504')),
        ('attributeValuesFormCommand.attributeValues[33].disabled', (None, 'true')),
        ('attributeValuesFormCommand.attributeValues[34].attributeValue', (None, '')),
        ('attributeValuesFormCommand.attributeValues[34].operatorAttribute.id', (None, '272505')),
        ('attributeValuesFormCommand.attributeValues[34].disabled', (None, 'false')),
        ('attributeValuesFormCommand.attributeValues[35].attributeValue', (None, '342535833')),
        ('attributeValuesFormCommand.attributeValues[35].operatorAttribute.id', (None, '272506')),
        ('attributeValuesFormCommand.attributeValues[35].disabled', (None, 'false')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[0].operatorAttribute.code", (None, 'categoria')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[0].operatorAttribute.id", (None, '1100')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[0].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[1].attributeValue", (None, 'B0CY1R9CXC')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[1].operatorAttribute.id", (None, '1101')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[1].disabled", (None, 'false')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[2].operatorAttribute.id", (None, '1102')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[2].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[3].operatorAttribute.id", (None, '3781')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[3].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[4].operatorAttribute.id", (None, '1103')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[4].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[5].operatorAttribute.id", (None, '1104')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[5].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[6].operatorAttribute.id", (None, '1105')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[6].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[7].operatorAttribute.id", (None, '1109')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[7].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[8].operatorAttribute.id", (None, '1533')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[8].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[9].operatorAttribute.id", (None, '1534')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[9].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[10].operatorAttribute.id", (None, '4137')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[10].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[11].operatorAttribute.id", (None, '4138')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[11].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[12].operatorAttribute.id", (None, '4139')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[12].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[13].operatorAttribute.id", (None, '1117')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[13].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[14].operatorAttribute.id", (None, '1116')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[14].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[15].operatorAttribute.id", (None, '1115')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[15].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[16].operatorAttribute.id", (None, '150774')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[16].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[17].operatorAttribute.id", (None, '222409')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[17].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[18].operatorAttribute.id", (None, '337333')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[18].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[19].operatorAttribute.id", (None, '340442')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[19].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[20].operatorAttribute.id", (None, '340461')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[20].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[21].operatorAttribute.id", (None, '340312')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[21].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[22].attributeValue", (None, '')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[22].operatorAttribute.id", (None, '272493')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[22].disabled", (None, 'false')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[23].operatorAttribute.id", (None, '272494')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[23].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[24].operatorAttribute.id", (None, '272495')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[24].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[25].operatorAttribute.id", (None, '272496')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[25].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[26].operatorAttribute.id", (None, '272497')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[26].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[27].operatorAttribute.id", (None, '272498')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[27].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[28].operatorAttribute.id", (None, '272499')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[28].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[29].operatorAttribute.id", (None, '272500')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[29].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[30].operatorAttribute.id", (None, '272501')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[30].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[31].operatorAttribute.id", (None, '272502')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[31].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[32].operatorAttribute.id", (None, '272503')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[32].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[33].attributeValue", (None, '268585333')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[33].operatorAttribute.id", (None, '272504')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[33].disabled", (None, 'false')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[34].operatorAttribute.id", (None, '272505')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[34].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[35].operatorAttribute.id", (None, '272506')),
        ("offerAndVariantsCommand['ui-id-0'].attributeValuesFormCommand.attributeValues[35].disabled", (None, 'true')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.currencyCode", (None, 'PEN')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.shopUuid", (None, '2813603')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.stateCode", (None, '11')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.quantity", (None, '0')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.runningPricing.pricingPoints[0].price", (None, 'PEN 9000')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.runningPricing.state", (None, 'RUNNING')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.pendingPriceAdded", (None, 'false')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.logisticClassCode", (None, '')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.priceAdditionalInfo", (None, '')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.description", (None, '')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.shopSku", (None, 'B0CY1R9CXC')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.availableStarted", (None, '')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.availableEnded", (None, '')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.internalDescription", (None, '')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.minQuantityAlert", (None, '')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.runningPricing.pricingPoints[0].discountPrice", (None, 'PEN 8000')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.runningPricing.pricingPoints[0].quantity", (None, '1')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.runningPricing.discountValidityInterval.start", (None, '2024-09-11T14:51')),
        ("offerAndVariantsCommand['ui-id-0'].offerCommand.runningPricing.discountValidityInterval.end", (None, '')),
    ]

    response = requests.post(
        'https://ripleyperu-prod.mirakl.net/mmp/shop/sell/product/import',
        cookies=cookies,
        headers=headers,
        files=files,
    )


if __name__ == "__main__":
    #responseLoad=generate_response(params,cookies,headers)
    #response_to_json(responseLoad,"root_categories")
    # file_path="DropShippingAuto/src/marketPlacesDestino/ripley/CategoriesTree/root_categories.json"
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     root_categories_dict = json.load(file)
    # print(root_categories_dict)

    # #create path key for each root category
    # for root_cat in root_categories_dict:
    #     root_cat["path"]=[root_cat["label"]]
    # print(root_categories_dict)


    # get_categories_tree(root_categories_dict)
    # response_to_json(root_categories_dict,"CategoryTreeWithPaths")
    product_type_list=get_product_type_list()