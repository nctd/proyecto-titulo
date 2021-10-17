from control_procesos_logisticos.views import agendarRetiro, home,planificacion,tracking,indicadores,reporteGrafico,retiroGenerarPDF, validarOrdenVentaRetiro
from django.urls import path

urlpatterns = [
    path('',home, name='home'),
    path('planificacion/',planificacion, name='planificacion'),
    path('tracking/',tracking, name='tracking'),
    path('indicadores/',indicadores, name='indicadores'),
    path('get/reporte/obtenerfechas', reporteGrafico, name='reporte_grafico'),
    path('agendar-retiro',agendarRetiro,name='agendar_retiro'),
    path('get/agendar/generar-retiro',retiroGenerarPDF,name='generar_pdf_retiro'),
    path('get/agendar/validar-ov',validarOrdenVentaRetiro,name='validar_orden')
]