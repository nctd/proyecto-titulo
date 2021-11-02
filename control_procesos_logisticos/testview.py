import pandas as pd
import requests
from datetime import date,datetime,timedelta
from django.shortcuts import redirect, render

from control_procesos_logisticos.forms import ArticuloForm, ClienteForm, DespachoForm, LineaForm, OrdenVentaForm, PlanificacionForm, TransporteForm
from .models import Articulo, OrdenVenta,Cliente, Planificacion, Transporte

def planificacionTEST(request):
    data = {
        'form': PlanificacionForm,
        'response': '',
    }
    if request.method == 'POST':
        try:
            df = pd.read_excel(request.FILES['myfile'])
            df.fillna('-',inplace=True)
            
            for row in df.itertuples():
                response = requests.post('http://webservices.gruposentte.cl/DUOC/planificaciones.php', data={
                    'ov': row[1],
                    'linea' : row[2]
                })

                if response.json()['resultado'] == 0:
                    for value in response.json()['data']:
                        existe = Planificacion.objects.filter(orden_venta_id=value['ov']).exists()
                        if existe:
                            data = {'error': True,
                                    'form': PlanificacionForm,
                                    'detalles': 'La orden de venta ya existe en la planificación'}
                            return render(request,'planificacion/planificacion.html',data)
                        
            for row in df.itertuples():
                response = requests.post('http://webservices.gruposentte.cl/DUOC/planificaciones.php', data={
                    'ov': row[1],
                    'linea' : row[2]
                })

                if response.json()['resultado'] == 0:
                    for value in response.json()['data']:
                        data_cliente = {
                            'nombre': value['cliente'],
                            'direccion': value['direccion'],
                            'correo_contacto': value['correo_contacto']
                        }
                        cliente_exists = Cliente.objects.filter(nombre=value['cliente']).exists()
                        if cliente_exists:
                            id_cli = Cliente.objects.get(nombre=value['cliente'])
                        elif not cliente_exists:
                            cliente = ClienteForm(data=data_cliente)
                            if cliente.is_valid():
                                id_cli = cliente.save()
                                
                        data_orden_venta = {
                            'orden_venta': value['ov'],
                            'cliente': id_cli.pk,
                            'tipo_pago': value['tipo_pago'],
                            'canal_venta': value['canal_venta'],
                            'orden_compra': value['orden_compra'],
                            'tipo_venta': value['tipo_venta'],
                            'tipo_despacho': value['clausula'],
                        }
                        print(data_orden_venta)
                        ov_exists = OrdenVenta.objects.filter(orden_venta=value['ov']).exists()
                        if ov_exists:
                            print('existe')
                            id_ov = OrdenVenta.objects.get(orden_venta=value['ov'])
                        elif not ov_exists:
                            ov = OrdenVentaForm(data=data_orden_venta)
                            if ov.is_valid():
                                id_ov = ov.save()
                            
                        data_articulo = {
                            'cod_articulo': value['n_articulo'],
                            'descripcion': value['descripcion']
                        }
                        articulo_exists = Articulo.objects.filter(cod_articulo= value['n_articulo']).exists()
                        if articulo_exists:
                            id_art = Articulo.objects.get(cod_articulo= value['n_articulo'])
                        elif not articulo_exists:
                            articulo = ArticuloForm(data=data_articulo)
                            id_art = articulo.save()
                        else:
                            data = {
                                'error': True,
                                'detalles': 'Error al crear Articulo' + str(articulo.errors.values())
                            }                    
                            return render(request,'planificacion/planificacion.html',data)
                        
                        data_transporte = {
                            'ot': value['ot'],
                            'empresa': value['transporte']
                        }
                        transporte = TransporteForm(data=data_transporte)
                        if transporte.is_valid():
                            id_tsp = transporte.save()
                        else:
                            data = {
                                'error': True,
                                'detalles': 'Error al crear Transporte' + str(transporte.errors.values())
                            }                    
                            return render(request,'planificacion/planificacion.html',data)
                        data_despacho = {
                            'direccion': value['direccion'],
                            'guia_despacho': value['guia'],
                            'transporte': id_tsp.pk
                        }
                        despacho = DespachoForm(data=data_despacho)
                        if despacho.is_valid():
                            id_despacho = despacho.save()
                        else:
                            data = {
                                'error': True,
                                'detalles': 'Error al crear Despacho' + str(despacho.errors.values())
                            }                    
                            return render(request,'planificacion/planificacion.html',data)
                        
                        data_linea = {
                            'num_linea': value['linea'],
                            'cantidad': value['cantidad'],
                            'estado': value['solicitud_material'],
                            'valor': 250*int(value['cantidad']),
                            'orden_venta': id_ov.pk,
                            'articulo': id_art.pk,
                            'despacho': id_despacho.pk
                        }                        
                        print(data_linea)
                        linea = LineaForm(data=data_linea)
                        if linea.is_valid():
                            linea.save()
                        else:
                            data = {
                                'error': True,
                                'detalles': 'Error al crear Línea' + str(linea.errors.values())
                            }                    
                            return render(request,'planificacion/planificacion.html',data)

                        data_planificacion = {
                            'llave_busqueda': value['key'],
                            'fecha_planificacion': request.POST['fecha_planificacion'],
                            'orden_venta': id_ov.pk
                        }
                        pl = PlanificacionForm(data=data_planificacion)
                        if pl.is_valid():
                            pl.save()
                        else:
                            data = {
                                'error': True,
                                'detalles': 'Error al crear Planificación' + str(pl.errors.values())
                            }                    
                            return render(request,'planificacion/planificacion.html',data)
                        data['guardado'] = True
                        
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
                data = {'error': True, 'detalles': e.message}
                return render(request,'planificacion/planificacion.html',data)
            else:
                print(e)
    return render(request,'planificacion/planificacion.html',data)
        
    # data = {
    #     'form': PlanificacionForm,
    #     'response': '',
    # }
    
    # if request.method == 'POST':
    #     try:

    #         df = pd.read_excel(request.FILES['myfile'])
    #         df.fillna('-',inplace=True)
            
    #         #     # exists = OrdenVenta.objects.filter(orden_venta=row[0]).exists()
    #         #     # if exists:
    #         #     #     data['response'] += row[0] +', '
            
    #         fecha_pl = datetime.strptime(request.POST['fecha_planificacion'], "%d/%m/%Y").date()
            
    #         pl_exists = Planificacion.objects.filter(fecha_planificacion=fecha_pl).exists()
    #         if pl_exists:
    #             data['existe'] = 'Ya hay una planificacion para esta fecha'
    #             return render(request,'planificacion/planificacion.html',data)
            
    #         for row in df.itertuples():
    #             data_cli = {
    #                 'nombre': row[5],
    #                 'direccion': row[11],
    #                 'correo_contacto': row[17]
    #             }

    #             data_art = {
    #                 'cod_articulo': row[7],
    #                 'descripcion': row[8]
    #             }
    #             data_transporte = {
    #                 'empresa': row[9],
    #             }
    #             tsp_exists = Transporte.objects.filter(empresa=row[9]).exists()
    #             cli_exists = Cliente.objects.filter(nombre=row[5]).exists()  
                
    #             if not cli_exists:
    #                 cli = ClienteForm(data=data_cli)
    #                 if cli.is_valid():
    #                     id_cli = cli.save()
    #                     data_ov = {
    #                         'orden_venta':row[1],
    #                         'cliente':id_cli.pk,
    #                         'tipo_pago':row[6],
    #                         'canal_venta':row[19],
    #                         'orden_compra':row[20],
    #                         'tipo_venta':row[16],
    #                         'tipo_despacho':row[18],
    #                     }
    #                 else:
    #                     data = {
    #                         'error': True,
    #                         'detalles': 'Error al crear Cliente'
    #                     }
    #                     return render(request,'planificacion/planificacion.html',data)

                    
    #             if cli_exists:
    #                 cli = Cliente.objects.get(nombre=row[5])

    #                 data_ov = {
    #                     'orden_venta':row[1],
    #                     'cliente':cli.pk,
    #                     'tipo_pago':row[6],
    #                     'canal_venta':row[19],
    #                     'orden_compra':row[20],
    #                     'tipo_venta':row[16],
    #                     'tipo_despacho':row[18],
    #                 }
                    
    #             ov = OrdenVentaForm(data=data_ov)
    #             ov_exists = OrdenVenta.objects.filter(orden_venta=row[1]).exists()
    #             if ov_exists:
    #                 id_ov = OrdenVenta.objects.get(orden_venta=row[1])
    #             elif ov.is_valid():
    #                 id_ov = ov.save()
                
    #             else:
    #                 data = {
    #                         'error': True,
    #                         'detalles': 'Error al crear Orden de venta' + str(ov.errors.values())
    #                     }
    #                 return render(request,'planificacion/planificacion.html',data)
                
    #             articulo = ArticuloForm(data=data_art)
    #             art_exists = Articulo.objects.filter(cod_articulo=row[7]).exists()
    #             if art_exists:
    #                 id_art = Articulo.objects.get(cod_articulo=row[7])
    #             elif articulo.is_valid():
    #                 id_art = articulo.save()
    #             else:
    #                 data = {
    #                     'error': True,
    #                     'detalles': 'Error al crear Articulo' + str(articulo.errors.values())
    #                 }
                    
    #                 return render(request,'planificacion/planificacion.html',data)
                
    #             if not tsp_exists:
    #                 transporte = TransporteForm(data=data_transporte)
    #                 if transporte.is_valid():
    #                     id_tsp = transporte.save()
    #                 else:
    #                     data = {
    #                         'error': True,
    #                         'detalles': 'Error al crear Transporte'
    #                     }
    #                     return render(request,'planificacion/planificacion.html',data)
    #                 data_despacho = {
    #                     'direccion': row[11],
    #                     'guia_despacho': row[15],
    #                     'transporte': id_tsp.pk
    #                 }
    #             elif tsp_exists:
    #                 tsp = Transporte.objects.get(empresa=row[9])
    #                 data_despacho = {
    #                     'direccion': row[11],
    #                     'guia_despacho': row[15],
    #                     'transporte': tsp.pk
    #                 }
    #             despacho = DespachoForm(data=data_despacho)
    #             if despacho.is_valid():
    #                 id_desp = despacho.save()
    #             else:
    #                 data = {
    #                     'error': True,
    #                     'detalles': 'Error al crear Despacho' + str(despacho.errors.values())
    #                 }
    #                 return render(request,'planificacion/planificacion.html',data)
    #             data_linea = {
    #                 'num_linea': row[2],
    #                 'cantidad': row[12],
    #                 'estado': row[14],
    #                 'valor': row[13],
    #                 'orden_venta': id_ov.pk,
    #                 'articulo': id_art.pk,
    #                 'despacho': id_desp.pk
    #             }            
            
    #             linea = LineaForm(data=data_linea)
    #             if linea.is_valid():
    #                 linea.save()
    #             else:
    #                 data = {
    #                     'error': True,
    #                     'detalles': 'Error al crear linea'
    #                 }
    #                 return render(request,'planificacion/planificacion.html',data)
                
    #             data_temporal = {
    #                     'num_linea':row[2],
    #                     'orden_venta': id_ov.pk,
    #                 }
                    
    #             temporal = TemporalLineaForm(data=data_temporal)
    #             if temporal.is_valid():
    #                 temporal.save()
                
    #             data_pl = {
    #                 'llave_busqueda': row[3],
    #                 'fecha_planificacion':request.POST['fecha_planificacion'],
    #                 'orden_venta': id_ov.pk
    #             }
                    
    #             pl = PlanificacionForm(data=data_pl)
    #             if pl.is_valid():
    #                 pl.save()
    #             else:
    #                 data = {
    #                     'error': True,
    #                     'detalles': 'Error al crear la planificación'
    #                 }
    #                 return render(request,'planificacion/planificacion.html',data)
    #             data['guardado'] = True
                    
    #             # data['guardado'] = True
                    
    #     except ObjectDoesNotExist:
    #         data = {
    #             'error': True
    #         }
            
    #         return render(request,'planificacion/planificacion.html',data)
                    
 
    # return render(request,'planificacion/planificacion.html',data)