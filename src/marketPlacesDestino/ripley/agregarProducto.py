from utils.selectores import localizador

botonDePreciosYexistencias=localizador("boton para escoger la opcion Ofertas donde se crea un producto nuevo","ul[class='Box__StyledBox-sc-1l7cvey-0 kjcjC Flex__StyledBox-sc-1u1p1x3-0 idgEJy _Sidebar__StyledUl-sc-tw9a8s-3 cnOIuJ']>li:nth-child(6)>div>button>div>div","css")
botonOfertas=localizador("botón para ingresar a Ofertas donde se crea un producto nuevo","ul[aria-label='Precios y existencias']>li:nth-child(1)>a>div","css")
botonAñadirOferta=localizador("botón para ingresar a Añadir Oferta donde se creará el producto nuevo","a[data-clickid='add-an-offer']","css")
botonCrearProducto=localizador("botón para crar un producto nuevo","a[id='rightSideCreateProduct']","css")

#Parte 1
desplegableCategoria=localizador("desplegable para escoger la categoría","div[id='s2id_selectHierachy-0']>a>span>b","css")
desplegableSubcategoriaUno=localizador("desplegable para escoger subcategoría 1","div[id='s2id_selectHierachy-1']>a>span>b","css")
desplegableSubcategoriaDos=localizador("desplegable para escoger subcategoría 2","div[id='s2id_selectHierachy-2']>a>span>b","css")
desplegableSubcategoriaTres=localizador("desplegable para escoger subcategoría 3","div[id='s2id_selectHierachy-3']>a>span>b","css")

#Parte 2 con campos de computadora

cajaNombreProducto=localizador("recuadro para ingresar el nombre del producto","textarea[id='productAndOffersCommand-attributeValuesFormCommand-1102']","css")
cajaDescripciónCorta=localizador("recuadro para ingresar descripción corta del producto","textarea[id='productAndOffersCommand-attributeValuesFormCommand-3781']","css")
cajaDescripción=localizador("recuadro para ingresar descripción más completa","textarea[id='productAndOffersCommand-attributeValuesFormCommand-1103']","css")
desplegableMarca=localizador("recuadro para ingresar Marca del Producto","span[id='select2-chosen-47']","css") #este lo seleccioné sin ul ni nada en toería deberia dar clic, quiero probar eso
botonImagenPrincipal=localizador("para ingresar link de imagen principal","input[id='productAndOffersCommand-attributeValuesFormCommand-1105']","css")
botonImagenMiniatura=localizador("para ingresar link de imagen miniatura","input[id='productAndOffersCommand-attributeValuesFormCommand-1109']","css")
botonImagenDos=localizador("para ingresar link de imagen dos","input[id='productAndOffersCommand-attributeValuesFormCommand-1533']","css")
botonImagenTres=localizador("para ingresar link de imagen tres","input[id='productAndOffersCommand-attributeValuesFormCommand-1534']","css")
botonImagenCuatro=localizador("para ingresar link de imagen cuatro","input[id='productAndOffersCommand-attributeValuesFormCommand-4137']","css")
botonImagenCinco=localizador("para ingresar link de imagen cinco","input[id='productAndOffersCommand-attributeValuesFormCommand-4138']","css")
botonImagenSeis=localizador("para ingresar link de imagen seis","productAndOffersCommand-attributeValuesFormCommand-4139","css")
cajaAltoEmpaque=localizador("para ingresar Alto Empaque","input[id='productAndOffersCommand-attributeValuesFormCommand-1117']","css")
cajaAnchoEmpaque=localizador("para ingresar Ancho Empaque","input[id='productAndOffersCommand-attributeValuesFormCommand-1116']","css")
cajaLargoEmpaque=localizador("para ingresar Larga Empaque","input[id='productAndOffersCommand-attributeValuesFormCommand-1115']","css")
cajaPesoKg=localizador("para ingresar el Peso del producto en Kg","productAndOffersCommand-attributeValuesFormCommand-287510","css")
cajaEanUpc=localizador("para ingesar el UPC","input[id='productAndOffersCommand-attributeValuesFormCommand-222409']","css") #ni idea que es esto
desplegableTipoDeProducto=localizador("para seleccionar el tipo de producto","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287503']>a>span>b","css")
cajaModelo=localizador("para ingresar el modelo del equipo","input[id='productAndOffersCommand-attributeValuesFormCommand-287504']","css")
cajaConectividad=localizador("para ingresar información sobre conectividad","input[id='productAndOffersCommand-attributeValuesFormCommand-287505']","css")
cajaCamara=localizador("para ingresar calidad de camara en base a megapixeles","input[id='productAndOffersCommand-attributeValuesFormCommand-287506']","css")
desplegableProcesador=localizador("para seleccionar el tipo de procesador","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287507']>a>span>b","css")
desplegableMemoriaRam=localizador("para seleccionar tipo de Memoria RAM","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287508']>a>span>b","css")
desplegableDiscoDuro=localizador("para seleccionar capacidad del disco duro","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287509']>a>span>b","css")
cajaTarjetaGrafica=localizador("para ingresar información sobre tarjeta gráfica","input[id='productAndOffersCommand-attributeValuesFormCommand-287511']","css")
desplegableSistemaOperativo=localizador("para seleccionar el sistema operativo","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287512']>a>span>b","css")
cajaVelocidadProcesador=localizador("para ingresar velocidad del procesador","input[id='productAndOffersCommand-attributeValuesFormCommand-287513']","css")
cajaTamañoPantalla=localizador("para ingresar tamaño de pantalla en puglgadas","input[id='productAndOffersCommand-attributeValuesFormCommand-287514']","css")
desplegableTipoPantalla=localizador("desplegable para indicar el tipo de pantalla","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287515']>a>span>b","css")
desplegablePantallaTouch=localizador("desplegable para indicar si la pantalla es touch","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287516']>a>span>b","css")
cajaResoluciónPantalla=localizador("para ingresar la resolución de la pantalla en pixeles","input[id='productAndOffersCommand-attributeValuesFormCommand-287517']","css")
cajaTipoProcesador=localizador("para ingresar el tipo de procesador","input[id='productAndOffersCommand-attributeValuesFormCommand-287518']","css")
desplegableTipoDeMemoria=localizador("desplegabale para indicar el tipo de memoria","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287519']>a>span>b","css")
desplegableLectorDeTarjetas=localizador("despleagble para indicar si el equipo tiene lector de tarjetas","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287520']>a>span>b","css")
cajaTipoDiscoDuro=localizador("para ingresar el tipo de disco duro","input[id='productAndOffersCommand-attributeValuesFormCommand-287521']","css")
cajaMemoriaRamExpandible=localizador("para indicar la capacidad de la memoria expandible en gb","input[id='productAndOffersCommand-attributeValuesFormCommand-287522']","css")
desplegableCantidadPuertosUSB=localizador("desplegable para señalar la cantidad de puertos USB","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287523']>a>span>b","css")
desplegablePuertosHDMI=localizador("desplegable para señalar la cantidad de puertos HDMI","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287524']>a>span>b","css")
cajaTipodebatería=localizador("para ingresar el tipo de batería","input[id='productAndOffersCommand-attributeValuesFormCommand-287525']","css")
desplegableUnidadOptica=localizador("desplegable para indicar si posee unidad optica","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287526']>a>span>b","css")
desplegableWiFi=localizador("desplegable para indicar si posee WiFi","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287527']>a>span>b","css")
desplegableResolucionVideo=localizador("desplegable para indicar la resolución de video","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287528']>a>span>b","css")
desplegableBluetooth=localizador("desplegable para indicar si posee Bluetooth","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287529']>a>span>b","css")
desplegableEntradaVga=localizador("desplegable para indicar cantidad de entradas VGA","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287530']>a>span>b","css")
desplegableNfc=localizador("desplegable para indicar si posee NFC","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287531']>a>span>b","css")
desplegablePuertoEthernet=localizador("desplegable para indicar si posee puerto ethernet","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287532']>a>span>b","css")
desplegableEntradaAudio=localizador("desplegable para indicar si posee entrada de audio","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287533']>a>span>b","css")
cajaDuraciónBatería=localizador("para indicar la duración de la batería en horas","input[id='productAndOffersCommand-attributeValuesFormCommand-287534']","css")
desplegableMicrofonoIntegrado=localizador("desplegable para indicar si posee microfono integrado","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287535']>a>span>b","css")
desplegableTamañoPantalla=localizador("desplegable para indicar el tamaño de la pantalla en rango","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287536']>a>span>b","css")
desplegableIncluyeMouse=localizador("desplegable para indicar si incluye mouse","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287537']>a>span>b","css")
desplegableTecladoNumérico=localizador("desplegable para indicar si posee teclado numérico","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287538']>a>span>b","css")
cajaParlantes=localizador("para ingresar información sobre parlantes","input[id='productAndOffersCommand-attributeValuesFormCommand-287539']","css")
cajaCapacidadBatería=localizador("para ingresar la capacidad de la batería","input[id='productAndOffersCommand-attributeValuesFormCommand-287540']","css")
cajaAlto=localizador("para ingresar el alto del producto en cm","input[id='productAndOffersCommand-attributeValuesFormCommand-287542']","css")
cajaAncho=localizador("para ingresar el ancho del producto en cm","input[id='productAndOffersCommand-attributeValuesFormCommand-287543']","css")
cajaLargo=localizador("para ingresar el largo del producto en cm","input[id='productAndOffersCommand-attributeValuesFormCommand-287544']","css")
cajaGarantía=localizador("para ingresar la garantía del producto en meses","input[id='productAndOffersCommand-attributeValuesFormCommand-287545']","css")
desplegableNúmeroDeNúcleos=localizador("desplegable para indicar el número de núcleos","div[id='s2id_productAndOffersCommand-attributeValuesFormCommand-287546']>a>span>b","css")
# div[id='']>a>span>b
# input[id='']



#Parte 3 - No hay

#Parte 4
cajaSkuSeller=localizador("recuadro para llenar el SKU Seller","input[id='productAndOffersCommand-offerAndVariantsCommandui-id-0-attributeValuesFormCommand-1101']","css")
#no sé que es eso o si nos sirve, lo pongo por si acaso
desplegableColor=localizador("recuadro para seleccionar color del producto","div[id='s2id_productAndOffersCommand-offerAndVariantsCommandui-id-0-attributeValuesFormCommand-287541']>a>span>b","css")
cajaCantidad=localizador("recuadro para llenar cantidad disponible del producto","input[id='quantity']","css")
cajaPrecioProducto=localizador("recuadro para llenar el Precio del Producto","input[id='ui-id-0unitPrice']","css")
desplegableClaseLogística=localizador("recuadro para seleccionar Clase Logística","select[id='logisticClassCode']","css")
cajaInformaciónPrecios=localizador("llenar información complementaria para clientes","input[id='priceAdditionalInfo']","css")
cajaDescripcion=localizador("recuadro para llenar descripción Información de Precios","textarea[id='description']","css")
skuOferta=localizador("recuadro para llenar SKU de la Oferta","input[id='shopSku']","css")
cajaDisponiblidadInicio=localizador("recuadro para colocar la fecha de inicio disponibilidad","input[id='ui-id-0availableStarted']","css")
cajaDisponibiladFin=localizador("recuadro para colocar la fecha de fin disponibilidad","input[id='ui-id-0availableEnded']","css")
cajaDescripcionInterna=localizador("recuadro para colocar la descripción interna","textarea[id='internalDescription']","css")
cajaAlertaCantidad=localizador("recuadro para colocar mínimo de existencias por debajo del cual se enviará una alerta","input[id='minQuantityAlert']","css")
cajaPrecioDescuento=localizador("recuadro para colocar Precio con Descuento","input[id='ui-id-0defaultpoints0discountPrice']","css")
cajaPeriodoDescuentoInicio=localizador("recuadro para llenar el fecha inicio del descuento","input[id='ui-id-0runningPricing-discountValidityInterval-start']","css")
cajaPeriodoDescuentoFin=localizador("recuadro para llenar el fecha fin del descuento","input[id='ui-id-0runningPricing-discountValidityInterval-end']","css")
#ojo los campos obligatorios