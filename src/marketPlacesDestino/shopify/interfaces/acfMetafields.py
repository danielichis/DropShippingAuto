from DropShippingAuto.src.utils.selectores import localizador

#Para llenar especificaciones adicionales en la app Metafields

botonAplicaciones=localizador("para ingresar a buscar la App ACF Metafields","ul[class]>li[class='IypnU']:nth-child(2)>div>button>span>span","css")
botonAppAcfMetafields=localizador("para acceder a esta app donde se agrega más especificaciones","//div[text()='ACF: Metafields Custom Fields']","xpath")
botonProductosDeMetaFields=localizador("para ingresar, ubicar nuestro producto nuevo y agregar más especificaciones","button[id='products']>span[class]","css")
cajaBuscadorProductosActivos=localizador("para ubicar nuestro producto nuevo y activo y agregarle lo que falta","input[id='PolarisTextField1']","css")
botonBuscarProducto=localizador("boton para buscar el producto que le falta agregar detalles","//span[text()='Search']","xpath")
listaProductoParaEditar=localizador("lista obtenida de poner el nombre del producto para ubicar el cual se añadirán las espcficaciones","ul[class='Polaris-ResourceList'] li","css")
clicDesplegableDisponibilidad=localizador("desplegable que contiene los tipos disponibilidad a elegir","div[class='Polaris-Select']","css")
#duda porque probé en la consola y me salio undefined, y así me sale cuando si se clickea pera acá es clic para activar desplegable
listaDisponibilidad=localizador("contienen la lista de los tipos de disponibilidad", "select[id='PolarisSelect1']","css")
#duda porque no puedo ver si literalmente coge a los 4 tipos de disponibilidad
cajaShortDescription=localizador("recuadro para ingresar breve descripción","div[class='fr-element fr-view']","css") 
#puede ser este tb div[class='fr-wrapper'] no estoy segura porque ya tenía texto y no sabía donde sería el click para escribir
#botonGuardarMetaFields=localizador()
#incompleto porque al parecer no lo puedo ubicar porque no he creado un producto nuevo y no se encuentra el elemento

#para validar que se publica, sería en la página de unluka, buscarlo por el nombre del producto