from os import name
from control_procesos_logisticos.views import agendarRetiro, anularRetiro, buscarRetiroPDF, despachoAgendamiento, despachoGenerarPDF, generarReporteCitas, home, lineaObtenerArticuloPL, packingList, \
                                              packingListGenerarPDF, planificacion,tracking,indicadores,reporteGrafico,retiroGenerarPDF, validarOrdenVentaPL,\
                                              validarOrdenVenta, visualizarDespachoAgendamiento, visualizarRetiros,generarReporteRetiros,validarLineaPL,validarLineaRetiro
from django.urls import path


urlpatterns = [
    path('',home, name='home'),
    path('planificacion/',planificacion, name='planificacion'),
    path('tracking/',tracking, name='tracking'),
    path('indicadores/',indicadores, name='indicadores'),
    path('get/reporte/obtenerfechas', reporteGrafico, name='reporte_grafico'),
    path('agendar-retiro',agendarRetiro,name='agendar_retiro'),
    path('get/agendar/generar-retiro',retiroGenerarPDF,name='generar_pdf_retiro'),
    path('get/agendar/validar-linea-retiro',validarLineaRetiro,name='validar_linea_retiro'),
    path('get/validar-ov',validarOrdenVenta,name='validar_orden'),
    path('buscar-retiro',visualizarRetiros,name='buscar_retiro'),
    path('get/agendar/buscar-retiro-pdf',buscarRetiroPDF,name='buscar_retiro_pdf'),
    path('get/agendar/reporte-retiros',generarReporteRetiros,name='reporte_retiros'),
    path('put/agendar/anular-retiro',anularRetiro,name='anular_retiro'),
    path('packing-list/',packingList,name='packing_list'),
    path('get/packing-list/validar-ov-pl',validarOrdenVentaPL,name='validar_orden_pl'),
    path('get/packing-list/obtener-articulo-pl',lineaObtenerArticuloPL,name='obtener_articulo_pl'),
    path('get/packing-list/pdf-pl',packingListGenerarPDF,name='pl_pdf'),
    path('get/packing-list/validar-linea-pl',validarLineaPL,name='validar_linea_pl'),
    path('despacho-agendamiento',despachoAgendamiento,name='despacho_agendamiento'),    
    path('buscar-despacho-agendamiento',visualizarDespachoAgendamiento,name='buscar_despacho_agendamiento'),    
    path('get/despacho-agendamiento/pdf-cita',despachoGenerarPDF,name='cita_pdf'),    
    path('get/despacho-agendamiento/reporte-citas',generarReporteCitas,name='reporte_citas'),    
]