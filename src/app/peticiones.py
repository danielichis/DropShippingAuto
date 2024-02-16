import requests

def get_peticion():
    response = requests.get("https://script.googleusercontent.com/macros/echo?user_content_key=wi-dGukKTxIdBWO2nUEJwk_lfEtDbg3a70mdJT1aCcDtqymFysQYcyiDXIQhk2jbh5UxQLh_eCssKtYOjWDxQ8OOXmSWdvbmm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnHBqarQPJxN9sPV-R0qY_9ERJmJXrHLaHYSuDpqD7MxrOsXlAaApKmspYVdDrOW_j8__b7FXxWpFRqpYRzllmkhhJS2V6-9fu9z9Jw9Md8uu&lib=MatdM_wtrLfsXpuqglIPqzXM8TnYCn21l")
    #obtenemos el contenido de la peticion
    response = response.json()
    return response

print(get_peticion())

