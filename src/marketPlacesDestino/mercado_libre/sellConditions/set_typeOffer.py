import requests

cookies = {
    '_d2id': '81f95596-2882-451a-acde-7fd08b0faa67',
    '_hjSessionUser_720735': 'eyJpZCI6ImY0ODJhYWI0LTk5ZDItNTcwYS1hMWVmLTgwNDkzMmFkYzkzYiIsImNyZWF0ZWQiOjE3MjQzNzEzNzY0NDAsImV4aXN0aW5nIjp0cnVlfQ==',
    'ssid': 'ghy-082317-Ba0Caa4mQiMw3OtENkxDPAv82vDqQv-__-139265276-__-1819054933953--RRR_0-RRR_0',
    'orguserid': '70H947Zt9Zht',
    'orguseridp': '139265276',
    'ftid': 'NqrmeVMzSqK6ekNriwsF6bZKPuaodpNH-1724371394772',
    'orgnickp': 'UNALUKA%20INTERNACIONAL',
    'cp': 'PE-LMA_UEUtTE1BTWlyYWZsb3Jlcw',
    '_hjSessionUser_550932': 'eyJpZCI6IjAzOTEzZTNhLWQxYTItNWE2ZS04MjQ3LThjZDQ3NzdmZGVmZCIsImNyZWF0ZWQiOjE3MjQ0NDg2NDgyNjMsImV4aXN0aW5nIjp0cnVlfQ==',
    '_gcl_au': '1.1.1152252877.1724448649',
    'dsid': '5bf94e8b-8b4d-49b4-b87b-c769fc466104-1724449606124',
    'p_dsid': '80e1a0a6-1a46-4755-99c6-b41d695e9816-1724449606132',
    'cookiesPreferencesLoggedFallback': '%7B%22userId%22%3A139265276%2C%22categories%22%3A%7B%22advertising%22%3Atrue%2C%22functionality%22%3Anull%2C%22performance%22%3Anull%2C%22traceability%22%3Anull%7D%7D',
    '_hjSessionUser_783944': 'eyJpZCI6IjVmMTQyYTE3LWQzMGEtNTA1My04MTRmLWVhNzE3NTFjMGZiOCIsImNyZWF0ZWQiOjE3MjUxMDA3MTQxMTMsImV4aXN0aW5nIjpmYWxzZX0=',
    '_ga': 'GA1.3.1122180072.1725824160',
    'c_ui-navigation': '6.6.82',
    '_csrf': 'E57wQehH3UnLp5vbTbas_NLF',
    'XSRF-TOKEN': 'Sr6rDRNW-G0YHZSO_EIu-AO-SureUsxiiMLY',
    '_gid': 'GA1.3.100333500.1726337340',
    '_mldataSessionId': 'ba65614d-acce-4e82-21d2-c3874b71ce32',
    'ttl': '1726357445099',
    'rtid': '420f2175-1606-4dcb-81fd-42d9377c0400',
    'edsid': '313661c3-710a-3254-934a-faa396201358-1726364605747',
    'p_edsid': 'fc4a6d3d-795d-34f5-bb2f-8cc5d3b18608-1726364605763',
    'x-meli-session-id': 'armor.2d135197e84ed4519bf5e37c7b74a09f9e45a4b9bb2142342336e4dab055957a2c46ae3256a403ac0fde37ec40c588c6d80385c97d4007283c352f08c46bfcf13bc4e22dc837c1781137d86a18c355ffd7c4d11937f61ca4a9c0d0ea73c9f7a3.7d9c313ba7e5dd0bc47ee16461636734',
    'cookiesPreferencesLogged': '%7B%22userId%22%3A139265276%2C%22categories%22%3A%7B%22advertising%22%3Atrue%2C%22functionality%22%3Anull%2C%22performance%22%3Anull%2C%22traceability%22%3Anull%7D%7D',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'es-419,es;q=0.9,en;q=0.8',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': '_d2id=81f95596-2882-451a-acde-7fd08b0faa67; _hjSessionUser_720735=eyJpZCI6ImY0ODJhYWI0LTk5ZDItNTcwYS1hMWVmLTgwNDkzMmFkYzkzYiIsImNyZWF0ZWQiOjE3MjQzNzEzNzY0NDAsImV4aXN0aW5nIjp0cnVlfQ==; ssid=ghy-082317-Ba0Caa4mQiMw3OtENkxDPAv82vDqQv-__-139265276-__-1819054933953--RRR_0-RRR_0; orguserid=70H947Zt9Zht; orguseridp=139265276; ftid=NqrmeVMzSqK6ekNriwsF6bZKPuaodpNH-1724371394772; orgnickp=UNALUKA%20INTERNACIONAL; cp=PE-LMA_UEUtTE1BTWlyYWZsb3Jlcw; _hjSessionUser_550932=eyJpZCI6IjAzOTEzZTNhLWQxYTItNWE2ZS04MjQ3LThjZDQ3NzdmZGVmZCIsImNyZWF0ZWQiOjE3MjQ0NDg2NDgyNjMsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.1152252877.1724448649; dsid=5bf94e8b-8b4d-49b4-b87b-c769fc466104-1724449606124; p_dsid=80e1a0a6-1a46-4755-99c6-b41d695e9816-1724449606132; cookiesPreferencesLoggedFallback=%7B%22userId%22%3A139265276%2C%22categories%22%3A%7B%22advertising%22%3Atrue%2C%22functionality%22%3Anull%2C%22performance%22%3Anull%2C%22traceability%22%3Anull%7D%7D; _hjSessionUser_783944=eyJpZCI6IjVmMTQyYTE3LWQzMGEtNTA1My04MTRmLWVhNzE3NTFjMGZiOCIsImNyZWF0ZWQiOjE3MjUxMDA3MTQxMTMsImV4aXN0aW5nIjpmYWxzZX0=; _ga=GA1.3.1122180072.1725824160; c_ui-navigation=6.6.82; _csrf=E57wQehH3UnLp5vbTbas_NLF; XSRF-TOKEN=Sr6rDRNW-G0YHZSO_EIu-AO-SureUsxiiMLY; _gid=GA1.3.100333500.1726337340; _mldataSessionId=ba65614d-acce-4e82-21d2-c3874b71ce32; ttl=1726357445099; rtid=420f2175-1606-4dcb-81fd-42d9377c0400; edsid=313661c3-710a-3254-934a-faa396201358-1726364605747; p_edsid=fc4a6d3d-795d-34f5-bb2f-8cc5d3b18608-1726364605763; x-meli-session-id=armor.2d135197e84ed4519bf5e37c7b74a09f9e45a4b9bb2142342336e4dab055957a2c46ae3256a403ac0fde37ec40c588c6d80385c97d4007283c352f08c46bfcf13bc4e22dc837c1781137d86a18c355ffd7c4d11937f61ca4a9c0d0ea73c9f7a3.7d9c313ba7e5dd0bc47ee16461636734; cookiesPreferencesLogged=%7B%22userId%22%3A139265276%2C%22categories%22%3A%7B%22advertising%22%3Atrue%2C%22functionality%22%3Anull%2C%22performance%22%3Anull%2C%22traceability%22%3Anull%7D%7D',
    'device-memory': '8',
    'downlink': '10',
    'dpr': '1',
    'ect': '4g',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6Ijk4OTU4NiIsImFwIjoiMTgzNDkzNTM3NyIsImlkIjoiODczMDk5NWQ4NjU5OTc2YyIsInRyIjoiNWYxMWI2OTkzYWZiYzkzYzljOTIxMTU4MmM2ZTM5ZmQiLCJ0aSI6MTcyNjM2NTQ2OTE2NiwidGsiOiIxNzA5NzA3In19',
    'origin': 'https://www.mercadolibre.com.pe',
    'priority': 'u=1, i',
    'referer': 'https://www.mercadolibre.com.pe/publicar/bomni/139265276-list_omnichannel-e48e07b44a68/sales_condition_form',
    'rtt': '150',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-5f11b6993afbc93c9c9211582c6e39fd-8730995d8659976c-01',
    'tracestate': '1709707@nr=0-1-989586-1834935377-8730995d8659976c----1726365469166',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'viewport-width': '1280',
    'x-csrf-token': 'b8uBr3rc-dP-NJbGCgZBQox9mfujNCO6JDY0',
    'x-newrelic-id': 'XQ4OVF5VGwIIVlNbDgQCXlc=',
    'x-xsrf-token': 'Sr6rDRNW-G0YHZSO_EIu-AO-SureUsxiiMLY',
}

json_data = {
    'method': 'PATCH',
    'path': 'list/139265276-list_omnichannel-e48e07b44a68/sales_condition_form/listing-type-default',
    'loadingEvents': [],
    'errorEvents': [],
    'queryParams': {
        'isWebview': False,
        'domain': 'www.mercadolibre.com.pe',
        'formId': 'sales_condition_form',
    },
    'pathParams': [],
    'bodyParams': [],
    'headers': {},
    'body': {
        'output': {
            'value': {
                'listingType': {
                    'selected': 'bronze',
                    'channels': [
                        {
                            'channel': 'ml',
                            'campaign': '',
                        },
                    ],
                },
            },
        },
    },
    'params': {
        'isWebview': False,
        'domain': 'www.mercadolibre.com.pe',
        'formId': 'sales_condition_form',
    },
}

response = requests.put(
    'https://www.mercadolibre.com.pe/publicar/omni/api/event-request',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"method":"PATCH","path":"list/139265276-list_omnichannel-e48e07b44a68/sales_condition_form/listing-type-default","loadingEvents":[],"errorEvents":[],"queryParams":{"isWebview":false,"domain":"www.mercadolibre.com.pe","formId":"sales_condition_form"},"pathParams":[],"bodyParams":[],"headers":{},"body":{"output":{"value":{"listingType":{"selected":"bronze","channels":[{"channel":"ml","campaign":""}]}}}},"params":{"isWebview":false,"domain":"www.mercadolibre.com.pe","formId":"sales_condition_form"}}'
#response = requests.put(
#    'https://www.mercadolibre.com.pe/publicar/omni/api/event-request',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)
print(response.json())