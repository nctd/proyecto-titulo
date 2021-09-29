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
                    'tipo_venta':row[16],
                    'valor': row[13],
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
            
            list_tipo_venta = []
            for l in lineas:
                desp = l.despacho_id
                list_tipo_venta.append(str(l.tipo_venta))
            
            despacho = Despacho.objects.get(id_despacho=desp)
        
            
            data = {
                'orden_venta': ov,
                'cliente' : ov.cliente.nombre,
                'orden_compra': ov.orden_compra,
                'tipo_venta': list_tipo_venta,
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
    if lineas.count() > 0:
        
        valor_total = 0
        
        for lin in lineas:
            valor_total+= lin.valor

        sum_lineas = Linea.objects.filter().count()
        
        # 1STOCK_R
        cant_stock_r = lineas.filter(tipo_venta='1STOCK_R').count()
        prc_stock_r =  int(cant_stock_r * 100 / sum_lineas)
        val_stock_r = 0
        
        for stock_r in lineas.filter(tipo_venta='1STOCK_R'):
            val_stock_r += stock_r.valor
            
        prc_valor_stock_r = int(val_stock_r * 100 / valor_total)
        
        # 1STOCK
        cant_stock = lineas.filter(tipo_venta='1STOCK').count()
        prc_stock =  int(cant_stock * 100 / sum_lineas)
        val_stock = 0
        
        for stock in lineas.filter(tipo_venta='1STOCK'):
            val_stock += stock.valor
            
        prc_valor_stock = int(val_stock * 100 / valor_total)
        
        # 2CALZADO
        cant_calzado = lineas.filter(tipo_venta='2CALZADO').count()
        prc_calzado =  int(cant_calzado * 100 / sum_lineas)
        val_calzado = 0
        
        for calzado in lineas.filter(tipo_venta='2CALZADO'):
            val_calzado += calzado.valor
            
        prc_valor_calzado = int(val_calzado * 100 / valor_total)
        
        # 2LIQUIDA
        cant_liquida = lineas.filter(tipo_venta='2LIQUIDA').count()
        prc_liquida =  int(cant_liquida * 100 / sum_lineas)
        val_liquida = 0
        
        for liquida in lineas.filter(tipo_venta='2LIQUIDA'):
            val_liquida += liquida.valor
            
        prc_valor_liquida = int(val_liquida * 100 / valor_total)
        
        # 2PROYECT
        cant_proyect = lineas.filter(tipo_venta='2PROYECT').count()
        prc_proyect =  int(cant_proyect * 100 / sum_lineas)
        val_proyect = 0
        
        for proyect in lineas.filter(tipo_venta='2PROYECT'):
            val_proyect += proyect.valor
            
        prc_valor_proyect = int(val_proyect * 100 / valor_total)
        
        # OS
        cant_os = lineas.filter(tipo_venta='OS').count()
        prc_os =  int(cant_os * 100 / sum_lineas)
        val_os = 0
        
        for os in lineas.filter(tipo_venta='OS'):
            val_os += os.valor
            
        prc_valor_os = int(val_os * 100 / valor_total)

        
        data_no_liberada = Linea.objects.filter(estado='NO LIBERADA')
        data_picking = Linea.objects.filter(estado='EN PICKING')
        data_embalaje = Linea.objects.filter(estado='ENVIADA')
        data_reparto = Linea.objects.filter(estado='REPARTO')
        
        list_no_liberada = []
        list_picking = []
        list_embalaje = []
        list_reparto = []
        count = 1 
        
        for linea in data_no_liberada:
            list_no_liberada.append(str(count)+') '+ str(linea.orden_venta) + ' - Linea '+ str(linea.num_linea) + ' - ' + linea.articulo.descripcion + ' - ' + str(linea.cantidad))
            count +=1
        count = 1
        
        for linea in data_picking:
            list_picking.append(str(count)+') '+ str(linea.orden_venta) + ' - Linea '+ str(linea.num_linea) + ' - ' + linea.articulo.descripcion + ' - ' + str(linea.cantidad))
            count +=1
        count = 1
        
        for linea in data_embalaje:
            list_embalaje.append(str(count)+') '+ str(linea.orden_venta) + ' - Linea '+ str(linea.num_linea) + ' - ' + linea.articulo.descripcion + ' - ' + str(linea.cantidad))
            count +=1
        count = 1
        
        for linea in data_reparto:
            list_reparto.append(str(count)+') '+ str(linea.orden_venta) + ' - Linea '+ str(linea.num_linea) + ' - ' + linea.articulo.descripcion + ' - ' + str(linea.cantidad))
            count +=1


        prc_no_liberada = int(data_no_liberada.count() * 100 / sum_lineas)
        prc_picking = int(data_picking.count() * 100 / sum_lineas)
        prc_embalaje = int(data_embalaje.count() * 100 / sum_lineas)
        prc_reparto = int(data_reparto.count() * 100 / sum_lineas)
        
        lineas_exitosas = 0
        cant_stock_exitosas = 0
        for linea in lineas:
            if linea.despacho.guia_despacho != None and '-' not in linea.despacho.guia_despacho and 'GD' in linea.despacho.guia_despacho:
                lineas_exitosas +=1
                if linea.tipo_venta == '1STOCK':
                    cant_stock_exitosas+=1
                    
        
        prc_exitosas = int(lineas_exitosas * 100 / sum_lineas)
        prc_exitosas_stock = int(cant_stock_exitosas * 100 / cant_stock)
        data = {
            'lineas': lineas.values(),
            'ln_no_liberada': data_no_liberada.count(),
            'ln_picking': data_picking.count(),
            'ln_embalaje': data_embalaje.count(),
            'ln_reparto': data_reparto.count(),
            'sum_lineas': sum_lineas,
            'prc_no_liberada': prc_no_liberada,
            'prc_picking': prc_picking,
            'prc_embalaje': prc_embalaje,
            'prc_reparto': prc_reparto,
            'list_no_liberada':list_no_liberada,
            'list_picking':list_picking,
            'list_embalaje':list_embalaje,
            'list_reparto':list_reparto,
            'cant_stock':cant_stock,
            'prc_stock':prc_stock,
            'val_stock': val_stock,
            'prc_valor_stock': prc_valor_stock,
            'cant_stock_r':cant_stock_r,
            'prc_stock_r':prc_stock_r,
            'val_stock_r': val_stock_r,
            'prc_valor_stock_r': prc_valor_stock_r,
            'cant_calzado':cant_calzado,
            'prc_calzado':prc_calzado,
            'val_calzado': val_calzado,
            'prc_valor_calzado': prc_valor_calzado,
            'cant_liquida':cant_liquida,
            'prc_liquida':prc_liquida,
            'val_liquida': val_liquida,
            'prc_valor_liquida': prc_valor_liquida,
            'cant_proyect':cant_proyect,
            'prc_proyect':prc_proyect,
            'val_proyect': val_proyect,
            'prc_valor_proyect': prc_valor_proyect,
            'cant_os':cant_proyect,
            'prc_os':prc_os,
            'val_os': val_os,
            'prc_valor_os': prc_valor_os,
            'lineas_exitosas':lineas_exitosas,
            'prc_exitosas':prc_exitosas,
            'cant_stock_exitosas':cant_stock_exitosas,
            'prc_exitosas_stock': prc_exitosas_stock

        }

        return render(request,'indicadores/indicadores.html',data)
    return render(request,'indicadores/indicadores.html')