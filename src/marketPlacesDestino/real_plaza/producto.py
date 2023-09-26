from utils.selectores import localizador

boton_catalogo=localizador("botón para ingresar al catálogo de productos","ul[class='nav']>li:nth-child(3)","css")
boton_administradorDeProductos=localizador("botón para ingresar al administrador de productos","a[href='#/catalog/list']","css")
boton_crearProducto=localizador("botón para crear Producto Nuevo","div[class='row filter-row']>div>button:nth-child(2)","css")
boton_categoría=localizador("botón para seleccionar la categoría","input[id='categoryFormatterHelp']","css")
input_nombre_producto=localizador("recuadro para llenar nombre del producto","input[aria-describedby='nombreInput__BV_description_ nombreInput__BV_feedback_invalid_']","css")
input_descripcion_producto=localizador("recuadro para llenar la Descripción del Producto","div[class='ql-editor ql-blank']","css")
input_marca_producto=localizador("recuadro para llenar la marca del producto","div[id='inputBrand']>div>div[class='multiselect__select']","css")
checkbox_Oechsle=localizador("chekbox para seleccionar el sitio Oechsle","div[id='__BVID__207_']>label:nth-child(2)>span[class='custom-control-indicator']","css")
checkbox_PlazaVea=localizador("chekbox para seleccionar el sitio PlazaVea","div[id='__BVID__207_']>label:nth-child(3)>span[class='custom-control-indicator']","css")
checkbox_Promart=localizador("chekbox para seleccionar el sitio Promart","div[id='__BVID__207_']>label:nth-child(4)>span[class='custom-control-indicator']","css")
checkbox_RealPlaza=localizador("chekbox para seleccionar el sitio RealPlaza","div[id='__BVID__207_']>label:nth-child(5)>span[class='custom-control-indicator']","css")

#el siguiente elemento declarado contiene todos los posibles elementos que aparecen en la lista de especficaciones
elemento_especificaciones=localizador("elemento para ubicar las especificaciones del producto a completar que aparecen según categoría","div[class='card-body']>div[class='container-fluid']>div']","css")