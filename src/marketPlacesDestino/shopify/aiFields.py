from utils.dinamicMassivArgsExtractions import get_dinamic_args_extraction


def get_provider_with_f_calling(productData)->str:
    providerList=[{"name":"Marca","fieldType":"input","options":[]
    }]
    provider=get_dinamic_args_extraction(str(productData),providerList)
    return provider['Marca']