from control_procesos_logisticos.views import home,planificacion
from django.urls import path

urlpatterns = [
    path('',home, name='home'),
    path('planificacion/',planificacion, name='planificacion'),
]