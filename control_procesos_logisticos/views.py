from django.core.exceptions import RequestAborted
from django.http import response
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist

from control_procesos_logisticos.forms import ArticuloForm, ClienteForm, LineaForm, OrdenVentaForm, PlanificacionForm

from .models import Cliente, Linea, OrdenVenta, Planificacion
from django.contrib import messages
from tablib import Dataset
import pandas as pd

# Create your views here.
def home(request):
    return render(request,'index.html')

def planificacion(request):
    data = {
        'form': PlanificacionForm,
        'response': '',
    }
    if request.method == 'POST':
        df = pd.read_excel(request.FILES['myfile'])
        df.fillna('-',inplace=True)
        
        #     # exists = OrdenVenta.objects.filter(orden_venta=row[0]).exists()
        #     # if exists:
        #     #     data['response'] += row[0] +', '

        for row in df.itertuples():
            
            cli_exists = Cliente.objects.filter(nombre=row[5]).exists()
            if cli_exists:
                pass
            else:
                data_cli = {
                    'nombre': row[5],
                    'direccion': row[11]
                }
            
                cli = ClienteForm(data=data_cli)
                if cli.is_valid():
                    id_cli = cli.save()
            
            
            data_ov = {
                'orden_venta':row[1],
                'cliente':id_cli.pk,
                'tipo_pago':row[6],
                'tipo_venta':row[16],
                'canal_venta':row[19],
                'orden_compra':row[20]
            }
            
            ov = OrdenVentaForm(data=data_ov)
            if ov.is_valid():
                id_ov = ov.save()


            data_art = {
                'cod_articulo': row[7],
                'descripcion': row[8]
            }
            
            articulo = ArticuloForm(data=data_art)
            if articulo.is_valid():
                id_art = articulo.save()

            data_linea = {
                'num_linea': row[2],
                'cantidad': row[12],
                'estado': row[14],
                'orden_venta': id_ov.pk,
                'articulo': id_art.pk
            }
            
            linea = LineaForm(data=data_linea)
            if linea.is_valid():
                linea.save()
        
        
            data_pl = {
                'llave_busqueda': row[3],
                'fecha_planificacion':request.POST['fecha_planificacion'],
                'orden_venta': id_ov.pk
            }
            
            pl = PlanificacionForm(data=data_pl)
            if pl.is_valid():
                pl.save()

        
        
        
        # ov_resource = OrdenVentaResource()
        # dataset = Dataset()
        # planificaciones = request.FILES['myfile']
        
        # imported_data = dataset.load(planificaciones.read())
        # # print(request.POST['fecha_planificacion'])
        # items  = imported_data._get_dict()
        # print(items[0]['CLIENTE'])
        
        # for fila in items:
        #     print(fila['CLIENTE'])
        #     test_ov = {
        #         'orden_venta':fila['OV'],
        #         'cliente':fila['CLIENTE'],
        #         'tipo_pago':fila['TIPO DE PAGO'],
        #         'tipo_venta':fila['TIPO DE VENTA'],
        #         'canal_venta':fila['CANAL DE VENTA'],
        #         'orden_compra':fila['ORDEN DE COMPRA']
        #     }
            
        #     ov = OrdenVentaForm(data=test_ov)
        #     if ov.is_valid():
        #         ov.save()
        
        # for row in imported_data:
        #     # exists = OrdenVenta.objects.filter(orden_venta=row[0]).exists()
        #     # if exists:
        #     #     data['response'] += row[0] +', '

        #     # else:   
            
        #     data_ov = {
        #         'orden_venta':row[0],
        #         'cliente':row[4],
        #         'tipo_pago':row[5],
        #         'tipo_venta':row[15],
        #         'canal_venta':row[18],
        #         'orden_compra':row[19]
        #     }
        #     # print(row[4])
        
        #     ov = OrdenVentaForm(data=data_ov)
        #     if ov.is_valid():
        #         id_ov = ov.save()
        #     # ov = OrdenVenta(datos)
        #     # ovs.append(ov)
        #     # if len(ovs) > 3000:
        #     #     OrdenVenta.objects.bulk_create(ovs)
        #     #     ovs = []
        #     # ov.save()
        
        #     data_linea = {
        #         'num_linea': row[1],
        #         'cantidad': row[11],
        #         'estado': row[13],
        #         'orden_venta': id_ov.pk
        #     }
            
        #     linea = LineaForm(data=data_linea)
        #     if linea.is_valid():
        #         linea.save()
        
        
        #     # data_pl = {
        #     #     'llave_busqueda': row[2],
        #     #     'fecha_planificacion':request.POST['fecha_planificacion'],
        #     #     'orden_venta': id_ov.pk
        #     # }
            
        #     # pl = PlanificacionForm(data=data_pl)
        #     # if pl.is_valid():
        #     #     pl.save()
                
        
        # messages.success(request,'Planificacion creada',data)
                    
 
    return render(request,'planificacion/planificacion.html',data)

def tracking(request):
    if('id_ov' in request.GET):
        try:
            ov = OrdenVenta.objects.get(orden_venta=request.GET['id_ov'])

            print(ov.cliente.nombre)
            data = {
                'orden_venta': ov,
                'cliente' : ov.cliente.nombre,
                'orden_compra': ov.orden_compra,
                'tipo_venta': ov.tipo_venta,
                'canal_venta': ov.canal_venta
            }
            data['response'] = 'OV ENCONTRADA'
            return render(request,'tracking/tracking.html',data)
        except ObjectDoesNotExist:
            data = {
                'response': 'No se encontro la OV'
            }
            return render(request,'tracking/tracking.html',data)
    else:
        return render(request,'tracking/tracking.html')



    