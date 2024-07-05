import os
from PIL import Image

def get_images_paths(img_path)->list:
    imagesPaths=[]
    imagesPath=os.path.dirname(img_path)
    print(imagesPath)
    for image in os.listdir(imagesPath):
        #cambio
        if os.path.splitext(image)[1] == '.jpg':
            #cambio
            imagesPaths.append(os.path.join(imagesPath,image))
    return imagesPaths

def image_resize(img_path,size_tuple,index=0)->str:
    imgDirectory="/Users/macbook/Desktop/img_test"
    resImgFolderDir=os.path.join(imgDirectory,"test750x555")
    print("Redimensionando imagen...")
    original_image=Image.open(img_path)
    print(original_image.size)
    resized_img=original_image.copy()
    resized_img.thumbnail(size_tuple,Image.Resampling.LANCZOS)
    print(resized_img.size)
    resized_image_path=os.path.join(resImgFolderDir,f"resizedImg_ripley{str(index)}.jpg")
    resized_img.save(resized_image_path)
    print("Imagen redimensionada")
    return resized_image_path

def create_background_rgb(size_tuple,color_code_rgb):
    im = Image.new(mode = "RGB", size = size_tuple,color = color_code_rgb)
    #im.show()
    return im

def resize_w_background(img_path,size_tuple,color_code_rgb,index=0):
    resized_img=Image.open(image_resize(img_path,size_tuple,index))
    width,height=resized_img.size
    left=(size_tuple[0]-width)//2
    top=(size_tuple[1]-height)//2
    paste_coordinates=(left,top)
    background=create_background_rgb(size_tuple,color_code_rgb)
    background.paste(resized_img,paste_coordinates)
    print("Imagen redimensionada")
    print("Guardando la imagen")
    imgDirectory="/Users/macbook/Desktop/img_test"
    backgroundFolderDir=os.path.join(imgDirectory,"test750x555/background")
    os.makedirs(backgroundFolderDir,exist_ok=True)
    background_image_path=os.path.join(backgroundFolderDir,f"resizedImg_ripley_background{str(index)}.jpg")
    background.save(background_image_path)
    print(f"Imagen redimensionada guardada {index}")


def resize_w_background_same_folder(img_path,size_tuple,color_code_rgb,index=0):
    resized_img=Image.open(image_resize(img_path,size_tuple,index))
    width,height=resized_img.size
    left=(size_tuple[0]-width)//2
    top=(size_tuple[1]-height)//2
    paste_coordinates=(left,top)
    background=create_background_rgb(size_tuple,color_code_rgb)
    background.paste(resized_img,paste_coordinates)
    print("Imagen redimensionada")
    print("Guardando la imagen")
    imgDirectory="/Users/macbook/Desktop/img_test"
    backgroundFolderDir=os.path.join(imgDirectory,"test750x555")
    os.makedirs(backgroundFolderDir,exist_ok=True)
    background_image_path=os.path.join(backgroundFolderDir,f"resizedImg_ripley{str(index)}.jpg")
    background.save(background_image_path)
    print(f"Imagen redimensionada guardada {index}")    

def add_background_to_img(img_path,size_tuple,color_code_rgb,index=0):
    resized_img=img_path
    width,height=resized_img.size
    left=(size_tuple[0]-width)//2
    top=(size_tuple[1]-height)//2
    paste_coordinates=(left,top)
    background=create_background_rgb(size_tuple,color_code_rgb)
    background.paste(resized_img,paste_coordinates)
    print("Imagen redimensionada")
    print("Guardando la imagen")
    imgDirectory="/Users/macbook/Desktop/img_test"
    backgroundFolderDir=os.path.join(imgDirectory,"test750x555/background")
    os.makedirs(backgroundFolderDir,exist_ok=True)
    background_image_path=os.path.join(backgroundFolderDir,f"resizedImg_ripley_background{str(index)}.jpg")
    background.save(background_image_path)
    print(f"Imagen redimensionada guardada {index}")

if __name__ == "__main__":
    test_img="/Users/macbook/Desktop/img_test/81b40L47zLL._AC_SL1500_.jpg"
    ripleyCustomSize=(750,555)
    color="white"
    #image_resize(test_img,ripleyCustomSize)
    #create_background_rgb((750,555),"white")
    img_paths=get_images_paths(test_img)
    for i,img in enumerate(img_paths):
        resize_w_background_same_folder(img,ripleyCustomSize,color_code_rgb=color,index=i)
    print("Se redimensionaron todas las imágenes")
