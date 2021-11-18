from os import name
from control_procesos_logisticos.views import agendarRetiro, anularRetiro, buscarRetiroPDF, finalizarBultoPL, home, lineaObtenerArticuloPL, packingList, packingListGenerarPDF, planificacion,tracking,indicadores,reporteGrafico,retiroGenerarPDF, validarOrdenVentaPL,\
    validarOrdenVentaRetiro, visualizarRetiros,generarReporteRetiros,registro
from django.urls import path


urlpatterns = [
    path('',home, name='home'),
    path('planificacion/',planificacion, name='planificacion'),
    path('tracking/',tracking, name='tracking'),
    path('indicadores/',indicadores, name='indicadores'),
    path('get/reporte/obtenerfechas', reporteGrafico, name='reporte_grafico'),
    path('agendar-retiro',agendarRetiro,name='agendar_retiro'),
    path('get/agendar/generar-retiro',retiroGenerarPDF,name='generar_pdf_retiro'),
    path('get/agendar/validar-ov',validarOrdenVentaRetiro,name='validar_orden'),
    path('buscar-retiro',visualizarRetiros,name='buscar_retiro'),
    path('get/agendar/buscar-retiro-pdf',buscarRetiroPDF,name='buscar_retiro_pdf'),
    path('get/agendar/reporte-retiros',generarReporteRetiros,name='reporte_retiros'),
    path('put/agendar/anular-retiro',anularRetiro,name='anular_retiro'),
    path('packing-list/',packingList,name='packing_list'),
    path('get/packing-list/validar-ov-pl',validarOrdenVentaPL,name='validar_orden_pl'),
    path('get/packing-list/obtener-articulo-pl',lineaObtenerArticuloPL,name='obtener_articulo_pl'),
    path('post/packing-list/finalizar-bulto-pl',finalizarBultoPL,name='finalizar_bulto_pl'),
    path('get/packing-list/pdf-pl',packingListGenerarPDF,name='pl_pdf')
    # path('/login',login_user,name='login'),
]