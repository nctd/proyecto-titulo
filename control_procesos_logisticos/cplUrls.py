from control_procesos_logisticos.views import home,planificacion,tracking,indicadores,reporteGrafico
from django.urls import path

urlpatterns = [
    path('',home, name='home'),
    path('planificacion/',planificacion, name='planificacion'),
    path('tracking/',tracking, name='tracking'),
    path('indicadores/',indicadores, name='indicadores'),
    path('get/reporte/obtenerfechas', reporteGrafico, name='reporte_grafico')
]