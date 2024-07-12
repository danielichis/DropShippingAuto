from utils.dinamicMassivArgsExtractions import get_dinamic_args_extraction

def get_static_fields_with_openai(universeText):
    aditionalFields=["Titulo corto, maximo 30 caracteres","Breve resumen para vender","Peso en Kg del producto","Peso en Kg del envio","Dimensiones del producto en cm","Titulo corto entre 110 y 120 caracteres"]
    
    if not universeText["Acerca del producto"]:
        aditionalFields.append("Resumen de 3 a 4 parrafos separados por viñetas")

    listToSend=[]
    for field in aditionalFields:
        listToSend.append({"name":field,"fieldType":"input","options":[]})
    fields=get_dinamic_args_extraction(str(universeText),listToSend)
    
    return fields

def test_get_static_fields_with_openai():
    universeText="El producto es un pantalon de algodon, color azul, marca levis, talla 32, con 4 bolsillos"
    fields=get_static_fields_with_openai(universeText)
    print(fields)

if __name__ == "__main__":
    test_get_static_fields_with_openai()