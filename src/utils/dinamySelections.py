import random
import re
def search_best_option(palabra_a_comparar,lista_opciones,marketplace_comodin):
    seEncontro=False

    for opcion in lista_opciones:
        if palabra_a_comparar.lower() == opcion.lower():
            seEncontro=True
            print("se encontro exactamente")
            return opcion
    for opcion in lista_opciones:
        if palabra_a_comparar.lower() in opcion.lower():
            print("se encontro aproximadamente")
            seEncontro=True
            return opcion
    
    if seEncontro==False:
        if marketplace_comodin!="-":
            print("se encontro en el marketplace comodin")
            seEncontro=True
            return marketplace_comodin
    
    if seEncontro==False:
        #aleatorio de la lista
        print("enviar advertencia para que lo corrigan")
        return random.choice(lista_opciones)