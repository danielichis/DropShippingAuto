from utils.selectores import localizador

#PARTE 1: PARA IR A CREAR PRODUCTO

boton_perfil_unaluka=localizador("botón para ingresar al perfil","div[class='nav-header-user'] span>span:nth-child(2)","css")
boton_publicaciones=localizador("botón para ingresar a las publicaciones","div[class='user-menu__main']>ul>li:nth-child(8)>a","css")
boton_publicar=localizador("botón para ir y empezar la creación de un producto para su publicación","button[id='react-aria-2']>span>span","css")
boton_de_forma_individual=localizador("botón para ir publicar de forma individual","li[id='andes-button-dropdown__menu-item-0']>a>div","css")

#si es que no hay productos en borrador, el bot debe darle clic directo a boton_productos
#si es que sí hay productos en borrador, el bot debe darle clic a boton_iniciar_nueva_publicación y luego a boton_productos
boton_iniciar_nueva_publicación=localizador("botón para inicar nueva publicación de producto","div[class='sc-ui-card-body sc-ui-card-body--separator'] a[role='button']","css")
boton_productos=localizador("botón para ir a productos","div[id='hub_container']>div:nth-child(1) span[class='hub-box__image']","css")

#------------------------------------------------------------------------------------------------------------

#PARTE 2: CREAR EL PRODUCTO Y CONDICIONES DE VENTA

# Paso 1 de 2: Datos del Producto
input_indica_el_producto=localizador("input para indicar el tipo del producto","input[id='products_finder_input']","css")
boton_comenzar=localizador("botón para comenzar","button[class='andes-button andes-button--large andes-button--loud']","css")
boton_categorización_producto=localizador("botón para aceptar la categorización del producto y continuar","img[class='andes-list__item-image']","css")
boton_otras_marcas=localizador("botón para seleccionar otras marcas","div[class='searchable-option-values-container__list']>div:nth-child(4)>ul>li:last-child","css")
boton_confirmar_categoría=localizador("botón para confirmar la categoría","span[class='andes-button__content']","css")
input_marca=localizador("input para ingresar la marca","input[name='BRAND']","css")
input_modelo=localizador("input para ingresar el modelo","input[name='MODEL']","css") #se puede escribir o ubicar
boton_confirmar_datos_pdto_uno=localizador("botón para confirmar una parte de los datos del producto","div[class='sc-ui-card sc-ui-card sc-ui-card--big sc-ui-card--default'] button:first-child>span","css")
boton_condicion_nuevo=localizador("botón para indicar que el producto es nuevo","ul[class='andes-list andes-list--default andes-list--selectable']>li:first-child>div>div","css")
input_completa_título_pdto=localizador("input para completar el título del producto","input[placeholder='Ej: Celular Samsung Galaxy S9 64 GB negro']","css")
boton_continuar_en_datos_pdto=localizador("botón para continuar en los datos del producto","form[id='title_task'] div[class='sc-ui-card-footer sc-ui-card-footer--align-right'] button:first-child span","css")
boton_confirmar_datos_pdto_dos=("botón para confirmar una parte de los datos del producto","form[id='main_variation_attribute_COLOR_task'] button[type='submit']:first-child>span","css")
boton_subir_foto=localizador("botón para subir fotos","a[class='sc-ui-image-uploader__link']","css") #se usa para todo
input_cantidad_pdto=localizador("input para indicar la cantidad del producto","input[inputmode='numeric']","css")
boton_confirmar_datos_pdto_tres=localizador("botón para confirmar una parte de los datos del producto","form[id='specifications_task'] button[type='submit']:first-child span","css")
input_UPC=localizador("input para indicar el Código Universal del Producto","form[id='product_identifier_task'] input[inputmode='numeric']","css")
boton_confirmar_UPC=localizador("botón para confirmar el UPC","form[id='product_identifier_task'] button[type='submit']:first-child>span[class='andes-button__content']","css")
desplegable_marca_procesador=localizador("desplegable para seleccionar la marca del procesador","div[class='sell-ui-attribute-list sell-ui-attribute-list--default-value'] div[class='andes-dropdown__arrow']","css")
boton_confirmar_info_completa_producto=localizador("botón para confirmar la información completa del producto","div[class='sc-ui-card sc-ui-card-expandable sc-ui-card--big sc-ui-card--open sc-ui-card-optional--is-open sc-ui-card--default'] button[type='submit']:first-child>span","css")
boton_siguiente=localizador("botón para ir a la siguiente página","div[id='connection_button_task'] span","css")

#Paso 2 de 2: Condiciones de Venta
input_precio=localizador("input para indicar el precio del producto","input[type='text']","css")

#el elemento asociado al boton_confimar_condiciones_de_venta, es el mismo para los siguientes 4 casos
boton_confirmar_condiciones_de_venta_=localizador("botón para confirmar las condiciones de venta del producto","div[class='sc-ui-card-footer sc-ui-card-footer--align-right']>button:first-child>span","css")

boton_publicación_premium=localizador("botón para indicar el tipo de publicación","div[class='syi-commons-listing-types__container']>div:nth-child(2) button>span","css")

#escoger uno de los siguientes dos botones
boton_si_retiro_en_persona=localizador("botón para indicar que el comprador puede recoger el producto en persona","ul[class='andes-list andes-list--default andes-list--selectable']>li:first-child span>div","css")
boton_solo_envios=localizador("botón para indicar que el comprador solo puede recibir el producto por envío","ul[class='andes-list andes-list--default andes-list--selectable']>li:nth-child(2) span>div","css")

boton_garantía_de_fabrica=localizador("botón para indicar que es garantia de fábrica","div[class='syi-warranty__radio-group']>div:nth-child(2) span","css")
input_meses_garantía=localizador("input para indicar los meses de garantía","div[class='syi-warranty__radio-group']>div:nth-child(3) input","css")
boton_agregar_descripción=localizador("botón para agregar descripción","div[id='description_task'] svg>path:nth-child(2)","css")
input_descripción=localizador("input para agregar descripción","textarea[id='description']","css")
boton_publicar=localizador("botón para publicar producto creado","div[id='connection_button_task'] span","css")

