from utils.target import Target
INPUT_LIST_IMAGES=Target("INPUT PARA AGREGAR IMAGENES","//input[@type='file']")
INPUT_MARCA=Target("INPUT INGRESAR LA MARCA","//span[contains(text(),'Marca')]/parent::div//input")

INPUT_LIST_MARCAS=Target("COMBOX PARA OBTENER LA LISTA DE MARCAS","//span[contains(text(),'Marca')]/parent::div//ul/li")


INPUT_CATEGORIA=Target("INPUT PARA INGRESAR LA CATEGORIA","//span[contains(text(),'Categoría')]/parent::div//input")

INPUT_LIST_CATEGORIAS=Target("COMBOX PARA OBTENER LA LISTA DE CATEGORIAS","//span[contains(text(),'Categoría')]/parent::div//ul/li")

INPUT_NOMBRE_PRODUCTO=Target("INPUT PARA INGRESAR EL NOMBRE DEL PRODUCTO","//span[contains(text(),'Nombre Producto')]/parent::div/input")

INPUT_DESCRIPCION_PRODUCTO=Target("INPUT PARA INGRESAR LA DESCRIPCION DEL PRODUCTO","//span[contains(text(),'Descripción')]/parent::div//span[contains(text(),'Enter text here...')]")

INPUT_PRECIO_BASE=Target("INPUT PARA INGRESAR EL PRECIO BASE DEL PRODUCTO","//span[contains(text(),'Precio Base')]/parent::div/input")

INPUT_PRECIO_ESPECIAL=Target("INPUT PARA INGRESAR EL PRECIO ESPECIAL DEL PRODUCTO","//span[contains(text(),'Precio Especial')]/parent::div/input")

INPUT_COSTO_POR_ARTICULO=Target("INPUT PARA INGRESAR EL COSTO POR ARTICULO DEL PRODUCTO","//span[contains(text(),'Costo por artículo')]/parent::div/input")

INPUT_MARGEN_DE_GANANCIA=Target("INPUT PARA INGRESAR EL MARGEN DE GANANCIA DEL PRODUCTO","//span[contains(text(),'Margen')]/parent::div/input")

INPUT_GANANCIA=Target("INPUT PARA INGRESAR LA GANANCIA DEL PRODUCTO","//span[contains(text(),'Ganancia')]/parent::div/input")

INPUT_SKU=Target("INPUT PARA INGRESAR EL SKU DEL PRODUCTO","//span[contains(text(),'SKU (código de artículo)')]/parent::div/input")

INPUT_CODIGO_DE_BARRAS=Target("INPUT PARA INGRESAR EL CODIGO DE BARRAS DEL PRODUCTO","//span[contains(text(),'Código de barras (ISBN, UPC, GTIN, etc.)')]/parent::div/input")

INPUT_STOCK=Target("INPUT PARA INGRESAR EL STOCK DEL PRODUCTO","//span[contains(text(),'Stock')]/parent::div/input")

INPUT_LARGO=Target("INPUT PARA INGRESAR EL LARGO DEL PRODUCTO","//span[contains(text(),'Largo (cm)')]/parent::div/input")

INPUT_ANCHO=Target("INPUT PARA INGRESAR EL ANCHO DEL PRODUCTO","//span[contains(text(),'Ancho (cm)')]/parent::div/input")

INPUT_ALTURA=Target("INPUT PARA INGRESAR LA ALTURA DEL PRODUCTO","//span[contains(text(),'Altura (cm)')]/parent::div/input")

INPUT_PESO=Target("INPUT PARA INGRESAR EL PESO DEL PRODUCTO","//span[contains(text(),'Peso (gramos)')]/parent::div/input")

BUTTON_CREAR_PRODUCTO=Target("BOTON PARA CREAR UN PRODUCTO","//button[contains(text(),'Crear Producto')]")








