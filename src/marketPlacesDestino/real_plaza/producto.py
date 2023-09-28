from utils.selectores import localizador

#Para crear nuevo producto - previa
boton_catalogo=localizador("botón para ingresar al catálogo de productos","ul[class='nav']>li:nth-child(3)","css")
boton_administradorDeProductos=localizador("botón para ingresar al administrador de productos","a[href='#/catalog/list']","css")
boton_crearProducto=localizador("botón para crear Producto Nuevo","div[class='row filter-row']>div>button:nth-child(2)","css")

#Crear nuevo producto
boton_categoría=localizador("botón para seleccionar la categoría","input[id='categoryFormatterHelp']","css")
input_nombre_producto=localizador("recuadro para llenar nombre del producto","input[aria-describedby='nombreInput__BV_description_ nombreInput__BV_feedback_invalid_']","css")
input_descripcion_producto=localizador("recuadro para llenar la Descripción del Producto","div[class='ql-editor ql-blank']","css")
input_marca_producto=localizador("recuadro para llenar la marca del producto","div[id='inputBrand']>div>div[class='multiselect__select']","css")
checkbox_Oechsle=localizador("chekbox para seleccionar el sitio Oechsle","label[class='custom-control custom-checkbox']:nth-child(2) span[class='custom-control-indicator']","css")
checkbox_PlazaVea=localizador("chekbox para seleccionar el sitio PlazaVea","label[class='custom-control custom-checkbox']:nth-child(3) span[class='custom-control-indicator']","css")
checkbox_Promart=localizador("chekbox para seleccionar el sitio Promart","label[class='custom-control custom-checkbox']:nth-child(4) span[class='custom-control-indicator']","css")
checkbox_RealPlaza=localizador("chekbox para seleccionar el sitio RealPlaza","label[class='custom-control custom-checkbox']:nth-child(5) span[class='custom-control-indicator']","css")

#el siguiente elemento declarado contiene todos los posibles elementos que aparecen en la lista de especficaciones
elemento_especificaciones=localizador("elemento para ubicar las especificaciones del producto a completar que aparecen según categoría","div[class='tab-content']>div[aria-expanded='true']>div:nth-child(2)>div:nth-child(2)","css")