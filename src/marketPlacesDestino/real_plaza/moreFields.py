from utils.embeddings.embeding import get_best_similarity_option
from utils.managePaths import mp
import json
def get_best_real_plaza_category(contentProduct,realPlazaCategories):
    return get_best_similarity_option(contentProduct,realPlazaCategories)

def get_full_paths_real_plaza_categories():
    with open(mp.realPlazaFullPathCategoriesJsonPath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def test_get_best_real_plaza_category():
    sampleProductSkuData=mp.data_sku("B08NCDBT7Q")
    allPathsCategories=get_full_paths_real_plaza_categories()

    if sampleProductSkuData["clasificacion"]!="sin clasificacion":
        clasfication=str(sampleProductSkuData["clasificacion"])
    else:
        initialPromt="Esta es la informacion estructurada de un un producto de Amazon, por favor cual seria la mejor clasificacion para este producto ? :"
        clasfication=initialPromt+str(sampleProductSkuData)
    bestOption=get_best_similarity_option(allPathsCategories,clasfication)
    print(bestOption)
if __name__ == "__main__":
    test_get_best_real_plaza_category()
    