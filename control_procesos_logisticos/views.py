from django.http import response
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist

from control_procesos_logisticos.forms import ArticuloForm, ClienteForm, DespachoForm, LineaForm, OrdenVentaForm, PlanificacionForm, TemporalLineaForm, TransporteForm

from .models import Cliente, Despacho, Linea, OrdenVenta, Planificacion,Transporte,TemporalLinea
from django.contrib import messages
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
                    'direccion': row[11],
                    'correo_contacto': row[17]
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
            
            
            tsp_exists = Transporte.objects.filter(empresa=row[9]).exists()
        
            if tsp_exists:
                pass
            else: 
                data_transporte = {
                    'empresa': row[9],
                }
                        
                transporte = TransporteForm(data=data_transporte)
                if transporte.is_valid():
                    id_tsp = transporte.save()
            # desp_exists = Despacho.objects.filter(direccion=row[11]).exists()
        
            # if desp_exists:
            #     pass
            # else:
            data_despacho = {
                'direccion': row[11],
                'guia_despacho': row[15],
                'transporte': id_tsp.pk
            }

            despacho = DespachoForm(data=data_despacho)
            if despacho.is_valid():
                id_desp = despacho.save()
            


            
            
            data_linea = {
                'num_linea': row[2],
                'cantidad': row[12],
                'estado': row[14],
                'orden_venta': id_ov.pk,
                'articulo': id_art.pk,
                'despacho': id_desp.pk
            }            
            
            linea = LineaForm(data=data_linea)
            if linea.is_valid():
                linea.save()
        
            data_temporal = {
                'num_linea':row[2],
                'orden_venta': id_ov.pk,
            }
            
            temporal = TemporalLineaForm(data=data_temporal)
            if temporal.is_valid():
                temporal.save()
        
            data_pl = {
                # 'llave_busqueda': row[3],
                'fecha_planificacion':request.POST['fecha_planificacion'],
                'orden_venta': id_ov.pk
            }
            
            pl = PlanificacionForm(data=data_pl)
            if pl.is_valid():
                pl.save()

        
        # messages.success(request,'Planificacion creada',data)
                    
 
    return render(request,'planificacion/planificacion.html',data)

def tracking(request):
    if('id_ov' in request.GET):
        lineas_ov =[]
        try:
            ov = OrdenVenta.objects.get(orden_venta=request.GET['id_ov'])

            lineas = Linea.objects.filter(orden_venta=ov.orden_venta)
            
            for l in lineas.values():
                desp = l['despacho_id']
            
            despacho = Despacho.objects.get(id_despacho=desp)
        
            
            data = {
                'orden_venta': ov,
                'cliente' : ov.cliente.nombre,
                'orden_compra': ov.orden_compra,
                'tipo_venta': ov.tipo_venta,
                'canal_venta': ov.canal_venta,
                'despacho': despacho,
                'lineas': lineas
            }
            
            data['response'] = 'OV ENCONTRADA'
            messages.success(request,'OV EXISTE')
            return render(request,'tracking/tracking.html',data)
        except ObjectDoesNotExist:
            data = {
                'response': 'No se encontro la OV'
                
            }
            
            return render(request,'tracking/tracking.html',data)
    else:
        return render(request,'tracking/tracking.html')



    