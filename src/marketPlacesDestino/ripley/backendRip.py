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