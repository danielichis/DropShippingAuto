import os
from pathlib import Path
from src.utils.manipulateDicts import dc
import sys
import json
class managePaths:
    def __init__(self):
        pass
    def get_current_path(self,up_tree=0):
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)    
        new_parent=Path(application_path)
        for i in range(up_tree):
            new_parent=new_parent.parent
        return new_parent
    def get_root_path(self):
        root_path = os.getcwd()
        return root_path
    def data_sku(self,sku):
        crrpaht=self.get_current_path(2)
        skuPath=os.path.join(crrpaht,"src","marketPlacesOrigen","amazon","skus_Amazon",sku)
        dataSkuPath=os.path.join(skuPath,"data.json")
        imagesPath=os.path.join(skuPath,"images")
        images=os.listdir(imagesPath)
        absPathImages=[]
        for image in images:
            absPathImage=os.path.join(imagesPath,image)
            absPathImages.append(absPathImage)
        with open(dataSkuPath,encoding="utf-8") as json_file:
            data = json.load(json_file)
        data['asbPathImages']=absPathImages
        return data

mp=managePaths()


