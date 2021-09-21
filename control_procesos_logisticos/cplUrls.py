from control_procesos_logisticos.views import home,planificacion,tracking,indicadores
from django.urls import path

urlpatterns = [
    path('',home, name='home'),
    path('planificacion/',planificacion, name='planificacion'),
    path('tracking/',tracking, name='tracking'),
    path('indicadores/',indicadores, name='indicadores'),
]