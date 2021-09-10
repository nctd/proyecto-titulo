from control_procesos_logisticos.forms import planificacionRegistro
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

def planificacion(request):
    return render(request,'planificacion/planificacion.html')

def tracking(request):
    return render(request,'tracking/tracking.html')