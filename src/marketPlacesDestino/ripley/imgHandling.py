import os
from PIL import Image


def image_resize(img_path,size_tuple)->str:
    imgDirectory="/Users/macbook/Desktop/img_test"
    resImgFolderDir=os.path.join(imgDirectory,"test750x555")
    print("Redimensionando imagen...")
    original_image=Image.open(img_path)
    print(original_image.size)
    resized_img=original_image
    resized_img.thumbnail(size_tuple,Image.Resampling.LANCZOS)
    resized_image_path=os.path.join(resImgFolderDir,f"resizedImg_ripley.jpg")
    resized_img.save(resized_image_path)
    print("Imagen redimensionada")
    return resized_image_path


def create_background_rgb(size_tuple,color_code_rgb):
    im = Image.new(mode = "RGB", size = size_tuple,color = color_code_rgb)
    #im.show()
    return im

def resize_w_background(img_path,size_tuple,color_code_rgb):
    resized_img=Image.open(image_resize(img_path,size_tuple))
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
    background_image_path=os.path.join(backgroundFolderDir,f"resizedImg_ripley_background.jpg")
    background.save(background_image_path)
    print("Imagen redimensionada guardada")

if __name__ == "__main__":
    test_img="/Users/macbook/Desktop/img_test/71utSH0Tr0L._AC_SL1500_.jpg"
    ripleyCustomSize=(750,555)
    color="black"
    #print(image_resize(test_img,ripleyCustomSize))
    #create_background_rgb((750,555),"white")
    resize_w_background(test_img,ripleyCustomSize,color_code_rgb=color)
