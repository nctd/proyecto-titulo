from django.http import response
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist

from control_procesos_logisticos.forms import ArticuloForm, ClienteForm, DespachoForm, LineaForm, OrdenVentaForm, PlanificacionForm, TemporalLineaForm, TransporteForm

from .models import Articulo, Cliente, Despacho, Linea, OrdenVenta, Planificacion,Transporte,TemporalLinea
from django.contrib import messages
from datetime import datetime
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
        try:

            df = pd.read_excel(request.FILES['myfile'])
            df.fillna('-',inplace=True)
            
            #     # exists = OrdenVenta.objects.filter(orden_venta=row[0]).exists()
            #     # if exists:
            #     #     data['response'] += row[0] +', '
            
            fecha_pl = datetime.strptime(request.POST['fecha_planificacion'], "%d/%m/%Y").date()
            
            pl_exists = Planificacion.objects.filter(fecha_planificacion=fecha_pl).exists()
            if pl_exists:
                data['existe'] = 'Ya hay una planificacion para esta fecha'
                return render(request,'planificacion/planificacion.html',data)
            
            for row in df.itertuples():

                # cli_exists = Cliente.objects.filter(nombre=row[5]).exists()
                # if cli_exists:
                #     pass
                # else:
                #     data_cli = {
                #         'nombre': row[5],
                #         'direccion': row[11],
                #         'correo_contacto': row[17]
                #     }
                
                #     cli = ClienteForm(data=data_cli)
                #     if cli.is_valid():
                #         id_cli = cli.save()
                
                    
                #     data_ov = {
                #         'orden_venta':row[1],
                #         'cliente':id_cli.pk,
                #         'tipo_pago':row[6],
                #         'tipo_venta':row[16],
                #         'canal_venta':row[19],
                #         'orden_compra':row[20]
                #     }
                    
                #     ov = OrdenVentaForm(data=data_ov)
                #     if ov.is_valid():
                #         id_ov = ov.save()


                # data_art = {
                #     'cod_articulo': row[7],
                #     'descripcion': row[8]
                # }
                
                # articulo = ArticuloForm(data=data_art)
                # if articulo.is_valid():
                #     id_art = articulo.save()
                    
                    
                # tsp_exists = Transporte.objects.filter(empresa=row[9]).exists()
            
                # if tsp_exists:
                #     pass
                # else: 
                #     data_transporte = {
                #         'empresa': row[9],
                #     }
                            
                #     transporte = TransporteForm(data=data_transporte)
                #     if transporte.is_valid():
                #         id_tsp = transporte.save()

                #     data_despacho = {
                #         'direccion': row[11],
                #         'guia_despacho': row[15],
                #         'transporte': id_tsp.pk
                #     }

                #     despacho = DespachoForm(data=data_despacho)
                #     if despacho.is_valid():
                #         id_desp = despacho.save()
                        


                #     data_linea = {
                #         'num_linea': row[2],
                #         'cantidad': row[12],
                #         'estado': row[14],
                #         'orden_venta': id_ov.pk,
                #         'articulo': id_art.pk,
                #         'despacho': id_desp.pk
                #     }            
                
                #     linea = LineaForm(data=data_linea)
                #     if linea.is_valid():
                #         linea.save()
                    
                #     data_temporal = {
                #         'num_linea':row[2],
                #         'orden_venta': id_ov.pk,
                #     }
                    
                #     temporal = TemporalLineaForm(data=data_temporal)
                #     if temporal.is_valid():
                #         temporal.save()
                
                # data_pl = {
                #     'llave_busqueda': row[3],
                #     'fecha_planificacion':request.POST['fecha_planificacion'],
                #     'orden_venta': id_ov.pk
                # }
                    
                # pl = PlanificacionForm(data=data_pl)
                # if pl.is_valid():
                #     pl.save()
                data_cli = {
                    'nombre': row[5],
                    'direccion': row[11],
                    'correo_contacto': row[17]
                }

                data_art = {
                    'cod_articulo': row[7],
                    'descripcion': row[8]
                }
                data_transporte = {
                    'empresa': row[9],
                }
                tsp_exists = Transporte.objects.filter(empresa=row[9]).exists()
                cli_exists = Cliente.objects.filter(nombre=row[5]).exists()  
                
                if not cli_exists:
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
                    else:
                        data = {
                            'error': True,
                            'detalles': 'Error al crear Cliente'
                        }
                        return render(request,'planificacion/planificacion.html',data)

                    
                if cli_exists:
                    cli = Cliente.objects.get(nombre=row[5])
                    print(cli.pk)
                    data_ov = {
                        'orden_venta':row[1],
                        'cliente':cli.pk,
                        'tipo_pago':row[6],
                        'tipo_venta':row[16],
                        'canal_venta':row[19],
                        'orden_compra':row[20]
                    }
                    
                ov = OrdenVentaForm(data=data_ov)
                ov_exists = OrdenVenta.objects.filter(orden_venta=row[1]).exists()
                if ov_exists:
                    id_ov = OrdenVenta.objects.get(orden_venta=row[1])
                elif ov.is_valid():
                    id_ov = ov.save()
                
                else:
                    data = {
                            'error': True,
                            'detalles': 'Error al crear Orden de venta' + str(ov.errors.values())
                        }
                    return render(request,'planificacion/planificacion.html',data)
                
                articulo = ArticuloForm(data=data_art)
                art_exists = Articulo.objects.filter(cod_articulo=row[7]).exists()
                if art_exists:
                    id_art = Articulo.objects.get(cod_articulo=row[7])
                elif articulo.is_valid():
                    id_art = articulo.save()
                else:
                    data = {
                        'error': True,
                        'detalles': 'Error al crear Articulo' + str(articulo.errors.values())
                    }
                    
                    return render(request,'planificacion/planificacion.html',data)
                
                if not tsp_exists:
                    transporte = TransporteForm(data=data_transporte)
                    if transporte.is_valid():
                        id_tsp = transporte.save()
                    else:
                        data = {
                            'error': True,
                            'detalles': 'Error al crear Transporte'
                        }
                        return render(request,'planificacion/planificacion.html',data)
                    data_despacho = {
                        'direccion': row[11],
                        'guia_despacho': row[15],
                        'transporte': id_tsp.pk
                    }
                elif tsp_exists:
                    tsp = Transporte.objects.get(empresa=row[9])
                    data_despacho = {
                        'direccion': row[11],
                        'guia_despacho': row[15],
                        'transporte': tsp.pk
                    }
                despacho = DespachoForm(data=data_despacho)
                if despacho.is_valid():
                    id_desp = despacho.save()
                else:
                    data = {
                        'error': True,
                        'detalles': 'Error al crear Despacho' + str(despacho.errors.values())
                    }
                    return render(request,'planificacion/planificacion.html',data)
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
                else:
                    data = {
                        'error': True,
                        'detalles': 'Error al crear linea'
                    }
                    return render(request,'planificacion/planificacion.html',data)
                
                data_temporal = {
                        'num_linea':row[2],
                        'orden_venta': id_ov.pk,
                    }
                    
                temporal = TemporalLineaForm(data=data_temporal)
                if temporal.is_valid():
                    temporal.save()
                
                data_pl = {
                    'llave_busqueda': row[3],
                    'fecha_planificacion':request.POST['fecha_planificacion'],
                    'orden_venta': id_ov.pk
                }
                    
                pl = PlanificacionForm(data=data_pl)
                if pl.is_valid():
                    pl.save()
                else:
                    data = {
                        'error': True,
                        'detalles': 'Error al crear la planificación'
                    }
                    return render(request,'planificacion/planificacion.html',data)
                data['guardado'] = True
                    
                # data['guardado'] = True
                    
        except ObjectDoesNotExist:
            data = {
                'error': True
            }
            
            return render(request,'planificacion/planificacion.html',data)
                    
 
    return render(request,'planificacion/planificacion.html',data)

def tracking(request):
    if('id_ov' in request.GET):
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
            data['tipodespacho'] = 'DESPACHO DIRECTO'
            data['guiadespacho'] = 'GD252900'
            data['ot'] = 'AB123'
            data['cita'] = '123456'
            data['existe'] = True
            return render(request,'tracking/tracking.html',data)
        except ObjectDoesNotExist:
            data = {
                'error': True
            }
            
            return render(request,'tracking/tracking.html',data)
    else:
        return render(request,'tracking/tracking.html')



def indicadores(request):
    lineas = Linea.objects.all()
    sum_lineas = Linea.objects.filter().count()
    
    ln_no_liberada = 0
    ln_picking = 0
    ln_embalaje = 0
    ln_reparto = 0
    
    data_embalaje = {
        
    }
    
    for lin in lineas:
        if lin.estado == 'NO LIBERADA':
            ln_no_liberada +=1
        if lin.estado == 'EN PICKING':
            ln_picking +=1
        if lin.estado == 'ENVIADA':
            ln_embalaje +=1
        if lin.estado == 'REPARTO':
            ln_reparto +=1
        
    prc_no_liberada = int(ln_no_liberada * 100 / sum_lineas)
    prc_picking = int(ln_picking * 100 / sum_lineas)
    prc_embalaje = int(ln_embalaje * 100 / sum_lineas)
    prc_reparto = int(ln_reparto * 100 / sum_lineas)
    
    data = {
        'lineas': lineas.values(),
        'ln_no_liberada': ln_no_liberada,
        'ln_picking': ln_picking,
        'ln_embalaje': ln_embalaje,
        'ln_reparto': ln_reparto,
        'sum_lineas': sum_lineas,
        'prc_no_liberada': prc_no_liberada,
        'prc_picking': prc_picking,
        'prc_embalaje': prc_embalaje,
        'prc_reparto': prc_reparto,
    }
    print(lineas)
    return render(request,'indicadores/indicadores.html',data)