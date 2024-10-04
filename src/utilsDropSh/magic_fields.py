from utils.dinamicMassivArgsExtractions import get_dinamic_args_extraction

def get_static_fields_with_openai(universeText):
    aditionalFields=["Titulo corto, maximo 30 caracteres","Breve resumen para vender","Peso en Kg del producto","Peso en Kg del envio"
                     ,"Dimensiones del producto en cm","Marca,proveedor o fabricante",
                     "Tipo de producto","¿Las unidades de peso y dimensiones,entre otras requieren conversion para que el producto se muestre en un mercado latinoamericano,responder si/no?",
                     "Titulo,corregido si está mal redactado, en un máximo de 150 caracteres con unidades convertidas de ser necesario",
                     "Titulo,corregido si está mal redactado, entre 110 y 120 caracteres con unidades convertidas de ser necesario",
                     "Titulo,corregido si está mal redactado, entre 80 y 90 caracteres con unidades convertidas de ser necesario"]
    
    if not "Acerca del producto" in universeText.keys():
        aditionalFields.append("Resumen de 2 a 3 parrafos separados por viñetas")

    listToSend=[]
    for field in aditionalFields:
        listToSend.append({"name":field,"fieldType":"input","options":[],"description":""})
    fields=get_dinamic_args_extraction(str(universeText),listToSend)
    
    return fields

def test_get_static_fields_with_openai():
    universeText="El producto es un pantalon de algodon, color azul, marca levis, talla 32, con 4 bolsillos"
    fields=get_static_fields_with_openai(universeText)
    print(fields)

if __name__ == "__main__":
    test_get_static_fields_with_openai()