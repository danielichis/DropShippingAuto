from DropShippingAuto.src.utils.selectores import localizador
botonDeProductos=localizador("boton para ir a Productos","ul[class]>li:nth-child(3)>div>div>a[aria-expanded] ","css")
botonAgregarProducto=localizador("boton para agregar Producto Nuevo","a[href='/store/unaluka/products/new']","css") 
#aquí dejo el anterior en xpath   //span[text()='Agregar producto']
cajaNombreProducto=localizador("recuadro para llenar nombre del producto","input[placeholder='Camiseta de manga corta']","css")
frameDescripcionProducto=localizador("frame para llenar la descripción del producto","iframe[id=\"product-description_ifr\"]","css")
cajaDescripcionProducto=localizador("recuadro para llenar la Descripción del Producto","body[data-id='product-description']","css")
botonAgregarImagenesProducto=localizador("boton para agregar las imágenes del producto","//span[text()='Subir nuevo']","xpath")
cajaPrecioProducto=localizador("recuadro para agregar Precio Real del Producto","input[name='price']","css")
cajaStock=localizador("recuadro para colocar el stock 1 unidad","input[name='inventoryLevels[0]']","css")
botonElProductoTieneSKU=localizador("boton para marcar e indicar que el producto tiene SKU","input[id=':r2vi:']","css")
cajaSKU=localizador("recuadro para llenar el SKU del producto","input[id='InventoryCardSku']","css")
cajaPesoDelProducto=localizador("recuadro para llenar el peso del producto","input[id='ShippingCardWeight']","css")
botonEditarPublicacionMotorDeBusqueda=localizador("boton para editar cómo podría aparecer este(a) producto en los resultados de los motores de búsqueda.","//span[text()='Editar']","xpath")
cajaMetaDescripción=localizador("recuadro que se autocompleta con la descripción del producto de arriba y donde se quita SKU","textarea[id=':r3i8:']","css")
botonDeGuardar=localizador("botón para dar clic y guardar todo la información de Producto","button[aria-label='Guardar']","css")
cajaCategoriaProducto=localizador("recuadro para escoger la categoría del producto","input[id=':r4a5:']","css")
cajaTipoDeProducto=localizador("recuadro para escoger el tipo de producto","input[id='ProductOrganizationCustomType']","css")
cajaProveedor=localizador("recuadro para seleccionar al proveedor que es la marca del producto","input[id=':r4a9:']","css")
cajaColecciones=localizador("recuadro para escoger y seleccionar una o varias colecciones a las que pertenece el producto","input[id='CollectionsAutocompleteField1']","css")
cajaPrecioComparacion=localizador("recuadro para poner precio fantasma y denotar que hay oferta","input[name='compareAtPrice']","css")
cajaEtiquetas=localizador("recuadro para seleccionar una o varias palabras respecto del producto","input[id=':r4ad:']","css")




