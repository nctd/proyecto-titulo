from django.core.exceptions import RequestAborted
from django.shortcuts import render
from control_procesos_logisticos.forms import LineaForm, OrdenVentaForm, PlanificacionForm
from .resources import OrdenVentaResource
from .models import Linea, OrdenVenta, Planificacion
from django.contrib import messages
from tablib import Dataset

# Create your views here.
def home(request):
    return render(request,'index.html')

def planificacion(request):
    data = {
        'form': PlanificacionForm,
        'response': '',
    }
    if request.method == 'POST':
        # ov_resource = OrdenVentaResource()
        dataset = Dataset()
        planificaciones = request.FILES['myfile']
        
        imported_data = dataset.load(planificaciones.read())
        # print(request.POST['fecha_planificacion'])

        
        for row in imported_data:
            # exists = OrdenVenta.objects.filter(orden_venta=row[0]).exists()
            # if exists:
            #     data['response'] += row[0] +', '

            # else:   
            
            data_ov = {
                'orden_venta':row[0],
                'cliente':row[4],
                'tipo_pago':row[5],
                'tipo_venta':row[15],
                'canal_venta':row[18],
                'orden_compra':row[19]
            }
        
            ov = OrdenVentaForm(data=data_ov)
            if ov.is_valid():
                id_ov = ov.save()
            # ov = OrdenVenta(datos)
            # ovs.append(ov)
            # if len(ovs) > 3000:
            #     OrdenVenta.objects.bulk_create(ovs)
            #     ovs = []
            # ov.save()
        
            data_linea = {
                'num_linea': row[1],
                'cantidad': row[11],
                'estado': row[13],
                'orden_venta': id_ov.pk
            }
            
            linea = LineaForm(data=data_linea)
            if linea.is_valid():
                linea.save()
        
        
            # data_pl = {
            #     'llave_busqueda': row[2],
            #     'fecha_planificacion':request.POST['fecha_planificacion'],
            #     'orden_venta': id_ov.pk
            # }
            
            # pl = PlanificacionForm(data=data_pl)
            # if pl.is_valid():
            #     pl.save()
                
        
        messages.success(request,'Planificacion creada',data)
                    
 
    return render(request,'planificacion/planificacion.html',data)

def tracking(request):
    return render(request,'tracking/tracking.html')