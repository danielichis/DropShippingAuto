from utils.embeddings.embeding import get_best_similarity_option
from utils.managePaths import mp
import json
from jsonpath_ng import jsonpath, parse
from jsonpath_ng.ext import parser



def get_full_category_based_on_fullpath(fullpath:str) -> str:
    tree_categories_path=mp.realPlazaTreeCategoriesJsonPath
    with open(tree_categories_path,encoding="utf-8") as json_file:
        savedRealPlazaCategories = json.load(json_file)
    searchString=f"$..*[?(@.namePath=='{fullpath}')]"
    jsonpath_expr = parser.parse(searchString)
    matches = jsonpath_expr.find(savedRealPlazaCategories)
    return matches[0].value

def get_best_path_real_plaza_category(AmazonCategories:str) -> str:
    fullpath_categories_path=mp.realPlazaFullPathCategoriesJsonPath
    with open(fullpath_categories_path,encoding="utf-8") as json_file:
        savedRealPlazaCategories = json.load(json_file)
    bestCategoryRl=get_best_similarity_option(savedRealPlazaCategories,AmazonCategories)
    categoryJson=get_full_category_based_on_fullpath(bestCategoryRl)
    return categoryJson
def test_get_best_path_real_plaza_category():
    amazonData=mp.data_sku("B0DBLNWH19")
    AmazonCategories=amazonData['clasificacion']
    category=get_best_path_real_plaza_category(str(AmazonCategories))
    print(category)
def test_full_category_based_on_fullpath():
    fullpath="Juguetes y Juegos/Juguetes/Otros juegos y juguetes/"
    id=get_full_category_based_on_fullpath(fullpath)
    print(id)
if __name__ == "__main__":
    test_get_best_path_real_plaza_category()
    #test_full_category_based_on_fullpath()