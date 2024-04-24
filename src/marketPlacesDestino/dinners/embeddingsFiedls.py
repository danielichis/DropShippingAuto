from utils.embeddings.embeding import get_top_n_match,get_openai_embeddings,get_similarity,get_openai_embedding
from utils.dinamicMassivArgsExtractions import get_dinamic_args_extraction
import os
from utils.managePaths import mp
import json
def get_brand_dinners(productData:dict,brands:list)->str:
    #validate if json file exists
    if not os.path.exists(mp.dinnersBrandsEmbedingsPath):
        print("Creating json file with brands embeddings")
        #create json with fields and embeddings
        brandsEmbeddings=get_openai_embeddings(brands)
        dictBrands=[]
        for i,brand in enumerate(brands):
            dictBrands.append({"field":brand,
                               "embedding":brandsEmbeddings[i]})
        with open(mp.dinnersBrandsEmbedingsPath,"w") as f:
            json.dump(dictBrands,f)
    else:
        print("Reading json file with brands embeddings")
        #read json file
        with open(mp.dinnersBrandsEmbedingsPath,"r") as f:
            dictBrands=json.load(f)
    #get top n matches
    productEmbedding=get_openai_embedding(productData)
    similarities=[]
    for i,brand in enumerate(dictBrands):
        #embedingBrand=dictBrands[i][brand]
        similarity=get_similarity(productEmbedding,brand['embedding'])
        rowdict={
            "brand":brand['field'],
            "similarity":similarity
        }
        similarities.append(rowdict)

    #sort by similarity
    similarities.sort(key=lambda x:x['similarity'],reverse=True)
    
    return similarities[0]['brand']

def add_brand_embedding(brand:str):
    with open(mp.dinnersBrandsEmbedingsPath,"r") as f:
        dictBrands=json.load(f)
    #get embeding
    embedding=get_openai_embedding(brand)
    dictBrands.append({"field":brand,
                       "embedding":embedding})
    with open(mp.dinnersBrandsEmbedingsPath,"w") as f:
        json.dump(dictBrands,f)
def get_brand_with_f_calling(productData)->str:

    brand=[{"name":"Marca","fieldType":"input","options":[]
    }]
    brand=get_dinamic_args_extraction(str(productData),brand)
    return brand['Marca']



def test_get_brand_dinners():
    productData={
        "title":"Zapatillas Nike",
        "description":"Zapatillas Nike para correr",
        "price":"50",
        "images":["https://www.nike.com"],
        "category":"Zapatillas",
    }
    brands=["Nike","Adidas","Reebok"]
    brand=get_brand_dinners(productData,brands)
    print(brand)

if __name__=="__main__":
    add_brand_embedding("No definido")
