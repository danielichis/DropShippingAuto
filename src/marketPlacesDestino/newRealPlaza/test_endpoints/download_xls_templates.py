import requests
from openpyxl import load_workbook

headers = {
    'accept': 'application/json',
    'accept-language': 'es-419,es;q=0.9,en;q=0.8',
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjAwYy1lM0JZd0Y0UVFQOHROZDluaiJ9.eyJpc3MiOiJodHRwczovL2lybWFya2V0cGxhY2UudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0MmM4Nzk2MjIzYTU4OGI5NzA4YjhkNiIsImF1ZCI6Imh0dHBzOi8vaXJtYXJrZXRwbGFjZS51cy5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTcyNzUxMzE0MSwiZXhwIjoxNzI3NTk5NTQxLCJzY29wZSI6InJlYWQ6Y3VycmVudF91c2VyIHVwZGF0ZTpjdXJyZW50X3VzZXJfbWV0YWRhdGEgZGVsZXRlOmN1cnJlbnRfdXNlcl9tZXRhZGF0YSBjcmVhdGU6Y3VycmVudF91c2VyX21ldGFkYXRhIGNyZWF0ZTpjdXJyZW50X3VzZXJfZGV2aWNlX2NyZWRlbnRpYWxzIGRlbGV0ZTpjdXJyZW50X3VzZXJfZGV2aWNlX2NyZWRlbnRpYWxzIHVwZGF0ZTpjdXJyZW50X3VzZXJfaWRlbnRpdGllcyBvZmZsaW5lX2FjY2VzcyIsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoiUGFTZkNJMHo3ZmxuQW9ObHlaNkljRFVtazRWYmhkelIifQ.ovAmLRPybHZxWcquRipjw7pWKv0vKCes9pT5UvN-UKxiYfRiDjaax0N8jUDygUc3Mhemok3oiH75XtaoAd3A1y1NIkOYWBSUJDYh34K3Lp1hD7VKYY4kmM0mNkKpdRBKMsIIb-iCkpIhGEwpo4vX3vU5I4A3k_GSPQG4GgFgwsqnoAfOxIO0tOu7cOXRRWkmrJqEFfV6vXsMKpJ4-GJvo4if_HLnH7hF78_2D4bUhoeR9yp9Cu606b4eIVyH50k2zF9EIEWGl_RKk_ZUYy9tlVQSUTNnUm-wngRs9wM06OvZqeZt8WCAphj3UPrpPNjG_nyaSS1656bWUGgSWjDRDQ',
    'content-type': 'application/json',
    'origin': 'https://sellercenter.intercorpretail.pe',
    'priority': 'u=1, i',
    'referer': 'https://sellercenter.intercorpretail.pe/',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

params = {
    'categoryId': '06pgM4YBkHnmclXq-6Dc',
}

response = requests.get(
    'https://prd.api.mp.sellercenter.pe/seller-product-service/v1/product/file-format',
    params=params,
    headers=headers,
)
with open("file.xlsx", "wb") as f:
    f.write(response.content)