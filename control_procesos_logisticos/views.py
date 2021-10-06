from django.http import response
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.contrib import messages

from pandas.io import json

from control_procesos_logisticos.forms import ArticuloForm, ClienteForm, DespachoForm, IndicadorTipoVentaForm, LineaForm, OrdenVentaForm, PlanificacionForm, TemporalLineaForm, TransporteForm

from .models import Articulo, Cliente, Despacho, IndicadorTipoVenta, Linea, OrdenVenta, Planificacion,Transporte,TemporalLinea
from datetime import date,datetime
import pandas as pd
import cx_Oracle


def getLineaTipoVenta(tipo_venta):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cant_lineas = cursor.var(cx_Oracle.NUMBER)
    valor = cursor.var(cx_Oracle.NUMBER)
    porc_lineas = cursor.var(cx_Oracle.NUMBER)
    porc_valor = cursor.var(cx_Oracle.NUMBER)
    
    cursor.callproc('SP_DATOS_REPORTE_VENTA', [tipo_venta,cant_lineas,valor,porc_lineas,porc_valor])
    cursor.close()
    
    datos_linea = {
        'cant_lineas' : int(cant_lineas.getvalue()),
        'valor' : int(valor.getvalue()),
        'porc_lineas' : int(porc_lineas.getvalue()),
        'porc_valor' : int(porc_valor.getvalue()),
    }
    return datos_linea

def getLineaTipoDespacho(tipo_despacho):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cant_lineas = cursor.var(cx_Oracle.NUMBER)
    valor = cursor.var(cx_Oracle.NUMBER)
    porc_lineas = cursor.var(cx_Oracle.NUMBER)
    porc_valor = cursor.var(cx_Oracle.NUMBER)
    
    cursor.callproc('SP_DATOS_REPORTE_DESPACHO', [tipo_despacho,cant_lineas,valor,porc_lineas,porc_valor])
    cursor.close()
    
    datos_linea = {
        'cant_lineas' : int(cant_lineas.getvalue()),
        'valor' : int(valor.getvalue()),
        'porc_lineas' : int(porc_lineas.getvalue()),
        'porc_valor' : int(porc_valor.getvalue()),
    }
    return datos_linea

def getEstadoCargaTarea(estado):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cant_lineas = cursor.var(cx_Oracle.NUMBER)
    porc_lineas = cursor.var(cx_Oracle.NUMBER)
    
    cursor.callproc('SP_ESTADO_CARGA', [estado,cant_lineas,porc_lineas])
    cursor.close()
    
    datos_linea = {
        'cant_lineas' : int(cant_lineas.getvalue()),
        'porc_lineas' : int(porc_lineas.getvalue()),
    }
    return datos_linea

def getTotalProgresoDiario():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cant_lineas = cursor.var(cx_Oracle.NUMBER)
    cant_exito_lineas = cursor.var(cx_Oracle.NUMBER)
    porc_exito_lineas = cursor.var(cx_Oracle.NUMBER)
    
    cursor.callproc('SP_OBTENER_TOTAL_PROGRESO', [cant_lineas,cant_exito_lineas,porc_exito_lineas])
    cursor.close()
    
    datos_linea = {
        'cant_lineas' : int(cant_lineas.getvalue()),
        'cant_exito_lineas' : int(cant_exito_lineas.getvalue()),
        'porc_exito_lineas' : int(porc_exito_lineas.getvalue()),
    }
    return datos_linea

def getProgresoDiarioTipoDespacho(tipo_despacho):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cant_lineas = cursor.var(cx_Oracle.NUMBER)
    cant_exito_lineas = cursor.var(cx_Oracle.NUMBER)
    porc_exito_lineas = cursor.var(cx_Oracle.NUMBER)
    
    cursor.callproc('SP_OBTENER_PROGRESO_DIARIO_DESPACHO', [tipo_despacho,cant_lineas,cant_exito_lineas,porc_exito_lineas])
    cursor.close()
    
    datos_linea = {
        'cant_lineas' : int(cant_lineas.getvalue()),
        'cant_exito_lineas' : int(cant_exito_lineas.getvalue()),
        'porc_exito_lineas' : int(porc_exito_lineas.getvalue()),
    }
    return datos_linea

def getProgresoDiarioTipoVenta(tipo_venta):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cant_lineas = cursor.var(cx_Oracle.NUMBER)
    cant_exito_lineas = cursor.var(cx_Oracle.NUMBER)
    porc_exito_lineas = cursor.var(cx_Oracle.NUMBER)
    
    cursor.callproc('SP_OBTENER_PROGRESO_DIARIO_VENTA', [tipo_venta,cant_lineas,cant_exito_lineas,porc_exito_lineas])
    cursor.close()
    
    datos_linea = {
        'cant_lineas' : int(cant_lineas.getvalue()),
        'cant_exito_lineas' : int(cant_exito_lineas.getvalue()),
        'porc_exito_lineas' : int(porc_exito_lineas.getvalue()),
    }
    return datos_linea


    
# Create your views here.
def home(request):
    data = {
        'linea': getLineaTipoVenta('1STOCK')
    }
    return render(request,'index.html',data)

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
                            'orden_compra':row[20],
                            'tipo_venta':row[16],
                            'tipo_despacho':row[21],
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
                        'orden_compra':row[20],
                        'tipo_venta':row[16],
                        'tipo_despacho':row[21],
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
            
            # list_tipo_venta = []
            for l in lineas:
                desp = l.despacho_id
                # list_tipo_venta.append(str(l.tipo_venta))
            
            despacho = Despacho.objects.get(id_despacho=desp)
        
            
            data = {
                'orden_venta': ov,
                'cliente' : ov.cliente.nombre,
                'orden_compra': ov.orden_compra,
                'tipo_venta': ov.tipo_venta,
                'tipo_despacho': ov.tipo_despacho,
                'canal_venta': ov.canal_venta,
                'despacho': despacho,
                'lineas': lineas,
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
        
        # Lineas a despachar segun tipo de despacho
        # Despacho directo
        datos_despacho_directo = getLineaTipoDespacho('DESPACHO DIRECTO')
        # Traspaso entre sucursales
        datos_despacho_traspaso = getLineaTipoDespacho('TRASPASO ENTRE SUCURSALES')
        # Embalaje
        datos_despacho_embalaje = getLineaTipoDespacho('EMBALAJE')
        # Exportaciones
        datos_despacho_exportaciones = getLineaTipoDespacho('EXPORTACIONES')
        # Retira cliente
        datos_despacho_retira = getLineaTipoDespacho('RETIRA CLIENTE')        
        
        # Lineas a despachar segun tipo de venta
        # 1STOCK_R
        datos_stock_r = getLineaTipoVenta('1STOCK_R')
        # 1STOCK
        datos_stock =  getLineaTipoVenta('1STOCK')
        # 2CALZADO
        datos_calzado =  getLineaTipoVenta('2CALZADO')       
        # 2LIQUIDA
        datos_liquida =  getLineaTipoVenta('2LIQUIDA')
        # 2PROYECT
        datos_proyect = getLineaTipoVenta('2PROYECT')
        # OS
        datos_os = getLineaTipoVenta('OS')


        # Estado de carga por tarea
        datos_no_liberada = getEstadoCargaTarea('NO LIBERADA')
        datos_picking = getEstadoCargaTarea('EN PICKING')
        datos_embalaje = getEstadoCargaTarea('ENVIADA')
        datos_reparto = getEstadoCargaTarea('REPARTO')
        
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

        # Progreso diario de despachos - Total
        progreso_total = getTotalProgresoDiario()
        # Progreso diario de despachos - Tipo de despacho
        # DESPACHO DIRECTO
        progreso_despacho_directo = getProgresoDiarioTipoDespacho('DESPACHO DIRECTO')
        # TRASPASO ENTRE SUCURSALES
        progreso_despacho_traspaso = getProgresoDiarioTipoDespacho('TRASPASO ENTRE SUCURSALES')
        # EMBALAJE
        progreso_despacho_embalaje = getProgresoDiarioTipoDespacho('EMBALAJE')
        # EXPORTACIONES
        progreso_despacho_exportaciones = getProgresoDiarioTipoDespacho('EXPORTACIONES')
        # RETIRA CLIENTE
        progreso_despacho_retira = getProgresoDiarioTipoDespacho('RETIRA CLIENTE')
        # Progreso diario de despachos - Tipo de venta
        # 1STOCK_R
        progreso_stock_r = getProgresoDiarioTipoVenta('1STOCK_R')
        # 1STOCK
        progreso_stock =  getProgresoDiarioTipoVenta('1STOCK')
        # 2CALZADO
        progreso_calzado =  getProgresoDiarioTipoVenta('2CALZADO')       
        # 2LIQUIDA
        progreso_liquida =  getProgresoDiarioTipoVenta('2LIQUIDA')
        # 2PROYECT
        progreso_proyect = getProgresoDiarioTipoVenta('2PROYECT')
        # OS
        progreso_os = getProgresoDiarioTipoVenta('OS')
        
            
        # if request.method == 'POST':
        #     try:
        #         stock_r_exists = IndicadorTipoVenta.objects.filter(fecha=date.today()).filter(tipo_venta='1STOCK_R')
        #         if not stock_r_exists:
        #             print('NO EXISTE')
        #             data_stock = {
        #                 'tipo_venta': '1STOCK_R',
        #                 'cantidad_despacho': cant_stock_r,
        #                 'exitos': cant_exitosas_stock_r,
        #                 'estado_final': prc_exitosas_stock_r
        #             }
                    
        #             prog_tipo_venta = IndicadorTipoVentaForm(data=data_stock)
                    
        #             if prog_tipo_venta.is_valid():
        #                 prog_tipo_venta.save()
        #             else:
        #                 data = {
        #                     'error': True,
        #                     'detalles': 'Error al guardar el progreso'
        #                 }
        #                 return render(request,'indicadores/indicadores.html',data)
        #         else:
        #             print('EXISTE')
                
        #         stock_1_exists = IndicadorTipoVenta.objects.filter(fecha=date.today()).filter(tipo_venta='1STOCK')
                
        #         if not stock_1_exists:
        #             data_stock = {
        #                 'tipo_venta': '1STOCK',
        #                 # 'cantidad_despacho': cant_stock,
        #                 'exitos': cant_exitosas_stock,
        #                 'estado_final': prc_exitosas_stock
        #             }
                    
        #             prog_tipo_venta = IndicadorTipoVentaForm(data=data_stock)
                    
        #             if prog_tipo_venta.is_valid():
        #                 prog_tipo_venta.save()
        #             else:
        #                 data = {
        #                     'error': True,
        #                     'detalles': 'Error al guardar el progreso'
        #                 }
        #                 return render(request,'indicadores/indicadores.html',data)
        #         else:
        #             print('EXISTE')

        #     except ObjectDoesNotExist:
        #         data = {
        #             'error': True
        #         }
                
            
        cumplimiento_1stock_r = IndicadorTipoVenta.objects.filter(tipo_venta='1STOCK_R')
        list_cumpl_1stock_r = []
        if cumplimiento_1stock_r:
            for valor in cumplimiento_1stock_r:
                list_cumpl_1stock_r.append(valor.estado_final)
        else:
            list_cumpl_1stock_r = [0]   
                
        cumplimiento_1stock = IndicadorTipoVenta.objects.filter(tipo_venta='1STOCK')
        list_cumpl_1stock = []
        if cumplimiento_1stock:
            for valor in cumplimiento_1stock:
                list_cumpl_1stock.append(valor.estado_final)
        else:
            list_cumpl_1stock = [0]
            
        data = {
            # Estado de carga por tarea
            'datos_no_liberada' : datos_no_liberada,
            'datos_picking' : datos_picking,
            'datos_embalaje' : datos_embalaje,
            'datos_reparto' : datos_reparto,
            'list_no_liberada':list_no_liberada,
            'list_picking':list_picking,
            'list_embalaje':list_embalaje,
            'list_reparto':list_reparto,
            
            # Tipo de despacho
            'datos_despacho_directo' : datos_despacho_directo,
            'datos_despacho_traspaso' : datos_despacho_traspaso,
            'datos_despacho_embalaje' : datos_despacho_embalaje,
            'datos_despacho_exportaciones' : datos_despacho_exportaciones,
            'datos_despacho_retira' : datos_despacho_retira,
            
            # Tipo de venta
            'datos_stock' : datos_stock,
            'datos_stock_r' : datos_stock_r,
            'datos_calzado' : datos_calzado,
            'datos_liquida' : datos_liquida,
            'datos_proyect' : datos_proyect,
            'datos_os' : datos_os,

            # Progreso diario - Tipo de despacho
            'progreso_despacho_directo' : progreso_despacho_directo,
            'progreso_despacho_traspaso' : progreso_despacho_traspaso,
            'progreso_despacho_embalaje' : progreso_despacho_embalaje,
            'progreso_despacho_exportaciones' : progreso_despacho_exportaciones,
            'progreso_despacho_retira' : progreso_despacho_retira,
            
            # Progreso diario - Tipo de venta
            'progreso_total' : progreso_total,
            'progreso_stock_r' : progreso_stock_r,
            'progreso_stock' : progreso_stock,
            'progreso_calzado' : progreso_calzado,
            'progreso_liquida' : progreso_liquida,
            'progreso_proyect' : progreso_proyect,
            'progreso_os' : progreso_os,
            
            # Reportes graficos
            'cumplimiento_1stock_r': json.dumps(list_cumpl_1stock_r),
            'cumplimiento_1stock': json.dumps(list_cumpl_1stock)

        }

        return render(request,'indicadores/indicadores.html',data)
    
    return render(request,'indicadores/indicadores.html')


