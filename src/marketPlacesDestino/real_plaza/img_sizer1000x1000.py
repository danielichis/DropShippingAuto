from PIL import Image

def resize_image(image_path, output_path):
    with Image.open(image_path) as image:
        resized_image = image.resize((1000, 1000))
        resized_image.save(output_path)