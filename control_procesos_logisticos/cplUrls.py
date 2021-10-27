from control_procesos_logisticos.views import agendarRetiro, buscarRetiroPDF, home, planificacion,tracking,indicadores,reporteGrafico,retiroGenerarPDF, validarOrdenVentaRetiro, visualizarRetiros,generarReporteRetiros
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
]