from django.db.backends.base.base import NO_DB_ALIAS
from django.http import response, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from pandas.io import json

from control_procesos_logisticos.forms import ArticuloForm, ClienteForm, DespachoForm, DetalleRetiroForm, IndicadorTipoVentaForm, LineaForm, OrdenVentaForm, PlanificacionForm, RetiroForm, TemporalLineaForm, TransporteForm

from .models import Articulo, Cliente, Despacho, DetalleRetiro, IndicadorTipoVenta, Linea, OrdenVenta, Planificacion, Retiro,Transporte,TemporalLinea
from datetime import date,datetime,timedelta

from .crearPDF import PDF

import pandas as pd
import requests
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
        'tipo': tipo_despacho,
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
        'tipo': tipo_despacho,
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
                            'tipo_despacho':row[18],
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
                        'tipo_despacho':row[18],
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
        tipos_despacho = OrdenVenta.objects.all().values_list('tipo_despacho',flat=True).distinct()
        # Lineas a despachar segun tipo de despacho
        # Despacho directo
        despachos = []
        progreso_despachos = []
        for val in tipos_despacho:
            despach = getLineaTipoDespacho(val)
            progreso = getProgresoDiarioTipoDespacho(val)
            despachos.append(despach)
            progreso_despachos.append(progreso)
        print(despachos)
        # datos_despacho_directo = getLineaTipoDespacho('DESPACHO DIRECTO')
        # # Traspaso entre sucursales
        # datos_despacho_traspaso = getLineaTipoDespacho('TRASPASO ENTRE SUCURSALES')
        # # Embalaje
        # datos_despacho_embalaje = getLineaTipoDespacho('EMBALAJE')
        # # Exportaciones
        # datos_despacho_exportaciones = getLineaTipoDespacho('EXPORTACIONES')
        # # Retira cliente
        # datos_despacho_retira = getLineaTipoDespacho('RETIRA CLIENTE')        
        
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
        # Lineas a despachar segun tipo de despacho
        # Despacho directo
        # progreso_despacho_directo = getProgresoDiarioTipoDespacho('DESPACHO DIRECTO')
        # # TRASPASO ENTRE SUCURSALES
        # progreso_despacho_traspaso = getProgresoDiarioTipoDespacho('TRASPASO ENTRE SUCURSALES')
        # # EMBALAJE
        # progreso_despacho_embalaje = getProgresoDiarioTipoDespacho('EMBALAJE')
        # # EXPORTACIONES
        # progreso_despacho_exportaciones = getProgresoDiarioTipoDespacho('EXPORTACIONES')
        # # RETIRA CLIENTE
        # progreso_despacho_retira = getProgresoDiarioTipoDespacho('RETIRA CLIENTE')
        
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
            'datos_despacho': despachos,
            # 'datos_despacho_directo' : datos_despacho_directo,
            # 'datos_despacho_traspaso' : datos_despacho_traspaso,
            # 'datos_despacho_embalaje' : datos_despacho_embalaje,
            # 'datos_despacho_exportaciones' : datos_despacho_exportaciones,
            # 'datos_despacho_retira' : datos_despacho_retira,
            
            # Tipo de venta
            'datos_stock' : datos_stock,
            'datos_stock_r' : datos_stock_r,
            'datos_calzado' : datos_calzado,
            'datos_liquida' : datos_liquida,
            'datos_proyect' : datos_proyect,
            'datos_os' : datos_os,

            # Progreso diario - Tipo de despacho
            'datos_progreso': progreso_despachos,
            # 'progreso_despacho_directo' : progreso_despacho_directo,
            # 'progreso_despacho_traspaso' : progreso_despacho_traspaso,
            # 'progreso_despacho_embalaje' : progreso_despacho_embalaje,
            # 'progreso_despacho_exportaciones' : progreso_despacho_exportaciones,
            # 'progreso_despacho_retira' : progreso_despacho_retira,
            
            # Progreso diario - Tipo de venta
            'progreso_total' : progreso_total,
            'progreso_stock_r' : progreso_stock_r,
            'progreso_stock' : progreso_stock,
            'progreso_calzado' : progreso_calzado,
            'progreso_liquida' : progreso_liquida,
            'progreso_proyect' : progreso_proyect,
            'progreso_os' : progreso_os,
        }

        return render(request,'indicadores/indicadores.html',data)
    
    return render(request,'indicadores/indicadores.html')


def reporteGrafico(request):
    if request.is_ajax and request.method == 'GET':
        tipo = request.GET.get('tipo',None)
        horizonte = request.GET.get('horizonte',None)
        
        rango = 0
        if horizonte == 'semanal':
            rango = 7
        if horizonte == 'quincenal':
            rango = 15
        if horizonte == 'mensual':
            rango = 30
            
        fecha_inicio = (date.today()) - timedelta(days=rango) 
        fecha_fin = date.today() + timedelta(days=1)
        delta = fecha_fin - fecha_inicio
        
        if tipo == 'tipo_venta':
            # reportes_tipo_venta =  IndicadorTipoVenta.objects.all().order_by('fecha').values_list('fecha',flat=True).distinct()
            # reportes_tipo_venta = IndicadorTipoVenta.objects.filter(fecha__range=((date.today()) - timedelta(days=rango),date.today() + timedelta(days=1))).order_by('fecha').values_list('fecha',flat=True).distinct()
            reportes_tipo_venta = IndicadorTipoVenta.objects.filter(fecha__range=(fecha_inicio,fecha_fin)).order_by('fecha').values_list()
            list_fecha_tipo_venta = []
                
            if reportes_tipo_venta:
                for i in range(delta.days + 1):
                    fecha = fecha_inicio + timedelta(days=i)
                    list_fecha_tipo_venta.append(fecha)
                    
                cumplimiento_1stock_r = reportes_tipo_venta.filter(tipo_venta='1STOCK_R')
                list_cumpl_1stock_r = []
                
                cumplimiento_1stock = reportes_tipo_venta.filter(tipo_venta='1STOCK')
                list_cumpl_1stock = []
                
                cumplimiento_calzado = reportes_tipo_venta.filter(tipo_venta='2CALZADO')
                list_cumpl_calzado = []
                
                cumplimiento_calzado = reportes_tipo_venta.filter(tipo_venta='2CALZADO')
                list_cumpl_calzado = []
                
                cumplimiento_liquid = reportes_tipo_venta.filter(tipo_venta='2LIQUID')
                list_cumpl_liquid = []
                
                cumplimiento_proyect = reportes_tipo_venta.filter(tipo_venta='2PROYECTO')
                list_cumpl_proyect = []
                
                
                cumplimiento_os = reportes_tipo_venta.filter(tipo_venta='OS')
                list_cumpl_os = []

                for fecha in list_fecha_tipo_venta:
                    if cumplimiento_1stock_r:
                        if fecha in cumplimiento_1stock_r.values_list('fecha',flat=True):
                            list_cumpl_1stock_r.append(cumplimiento_1stock_r.values_list('estado_final',flat=True).filter(fecha=fecha).first())
                        else:
                            list_cumpl_1stock_r.append(0)
                    else:
                        list_cumpl_1stock_r = [0]
                    
                    if cumplimiento_1stock:
                        if fecha in cumplimiento_1stock.values_list('fecha',flat=True):
                            list_cumpl_1stock.append(cumplimiento_1stock.values_list('estado_final',flat=True).filter(fecha=fecha).first())
                        else:
                            list_cumpl_1stock.append(0)
                    else:
                        list_cumpl_1stock = [0]
                        
                    if cumplimiento_calzado:
                        if fecha in cumplimiento_calzado.values_list('fecha',flat=True):
                            list_cumpl_calzado.append(cumplimiento_calzado.values_list('estado_final',flat=True).filter(fecha=fecha).first())
                        else:
                            list_cumpl_calzado.append(0)
                    else:
                        list_cumpl_calzado = [0]
                        
                    if cumplimiento_liquid:
                        if fecha in cumplimiento_liquid.values_list('fecha',flat=True):
                            list_cumpl_liquid.append(cumplimiento_liquid.values_list('estado_final',flat=True).filter(fecha=fecha).first())
                        else:
                            list_cumpl_liquid.append(0)
                    else:
                        list_cumpl_liquid = [0]
                        
                    if cumplimiento_proyect:
                        if fecha in cumplimiento_proyect.values_list('fecha',flat=True):
                            list_cumpl_proyect.append(cumplimiento_proyect.values_list('estado_final',flat=True).filter(fecha=fecha).first())
                        else:
                            list_cumpl_proyect.append(0)
                    else:
                        list_cumpl_proyect = [0]
                        
                    if cumplimiento_os:
                        if fecha in cumplimiento_os.values_list('fecha',flat=True):
                            list_cumpl_os.append(cumplimiento_os.values_list('estado_final',flat=True).filter(fecha=fecha).first())
                        else:
                            list_cumpl_os.append(0)
                    else:
                        list_cumpl_os = [0]

                return JsonResponse({
                    'valid':True,
                    'lista_fechas': list_fecha_tipo_venta,
                    'stock_r': list_cumpl_1stock_r,
                    'stock': list_cumpl_1stock,
                    'calzado': list_cumpl_calzado,
                    'liquid': list_cumpl_liquid,
                    'proyect': list_cumpl_proyect,
                    'os': list_cumpl_os,
                }, status=200)
            else:
                list_fecha_tipo_venta = [0]
            return JsonResponse({
                'valid':False,
                'lista_fechas': 'No hay fechas',
                },
                status = 200)
        if tipo == 'tipo_despacho':
            pass
    return JsonResponse({}, status = 400)

def agendarRetiro(request):
    if request.method == 'POST':
        list_ov = []
        for value in request.POST:
            if value.startswith('OV'):
                list_ov.append(value)
                
        data = []   
        data_retiro = {}
        data_detalle = []
        for ov in list_ov:
            response = requests.post('http://webservices.gruposentte.cl/DUOC/planificaciones.php', data={
                'ov': ov.split('-')[0],
                'linea' : ov.split('-')[1]
            })
            if response.json()['resultado'] == 0 and response.status_code == 200:
                for value in response.json()['data']:
                    data_retiro = {
                        'fecha': request.POST['fecha-retiro'],
                        'hora_inicio': request.POST['rango-horario'].split('-')[0],
                        'hora_fin': request.POST['rango-horario'].split('-')[1],
                        'cliente': value['cliente'],
                        'direccion': value['direccion'],
                    }
                    data_detalle = [value['ov'],
                                    value['linea'],
                                    value['descripcion'],
                                    value['cantidad'],
                                    value['solicitud_material']]
                    data.append(data_detalle)
            else:
                data = {
                    'error': True
                }
                return render(request,'agenda-retiro/agendar.html',data)   
        
        retiro = RetiroForm(data=data_retiro)
        if retiro.is_valid():
            id_retiro = retiro.save()
            retiroGenerarPDF(request,data_retiro,data)
            
            for item in data:
                print(item)
                print(item[3])         
                data_det = {
                    'orden_venta' : item[0],
                    'linea' : item[1],
                    'descripcion' : item[2],
                    'cantidad' : item[3],
                    'tipo_embalaje' : item[4],
                    'retiro' : id_retiro.pk
                }
                print(data_det)
                det_retiro = DetalleRetiroForm(data=data_det)
                if det_retiro.is_valid():
                    det_retiro.save()
                else:
                    data = {
                        'error': True, 
                        'detalles': 'Error al registrar detalles del retiro' + str(det_retiro.errors.as_data())
                    }
                    return render(request,'agenda-retiro/agendar.html',data)
                   
            data = {
                'guardado': True
            }
            return render(request,'agenda-retiro/agendar.html',data)
            
        else:
            data = {
                'error': True,
                'detalles': 'Error al registrar el retiro' + str(retiro.errors.values())
            }
            return render(request,'agenda-retiro/agendar.html',data)   
    return render(request,'agenda-retiro/agendar.html')   


def retiroGenerarPDF(request,data_retiro,data_detalle):
    pdf = PDF()
    pdf.add_page()
    
    # pdf.set_font("Arial", size = 15)
    
    pdf.titles('CITA NRO 12312')
    pdf.linea()
    pdf.texto('Fecha: ',14,10)
    pdf.texto(data_retiro['fecha'],45,10)
    
    pdf.texto('Hora inicio: ',14,20)
    pdf.texto(data_retiro['hora_inicio'],45,20)
    
    pdf.texto('Hora fin: ',14,30)
    pdf.texto(data_retiro['hora_fin'],45,30)
    
    pdf.texto('Cliente: ',14,40)
    pdf.texto(data_retiro['cliente'],45,40)
    
    pdf.texto('Dirección de retiro: ',14,50)
    pdf.texto(data_retiro['direccion'],45,50)    

    headers = ['Orden de venta','Línea OV','Descripción','Cantidad','Tipo Embalaje']

    pdf.tabla(headers,data_detalle)

    pdf.output("retiro.pdf")   
    return JsonResponse({'valid':'CREADO'})

def validarOrdenVentaRetiro(request):
    if request.is_ajax and request.method == 'GET':
        orden_venta = request.GET.get('orden_venta',None)
        linea = request.GET.get('linea',None)
        
        response = requests.post('http://webservices.gruposentte.cl/DUOC/planificaciones.php', data={
            'ov': orden_venta,
            'linea' : linea
        })

        
        if response.json()['resultado'] == 0 and response.status_code == 200:
            return JsonResponse({'valid':True})
        else:
            return JsonResponse({'valid':False})
        # return JsonResponse({'response':response.status_code})
        # ov_exists = OrdenVenta.objects.filter(orden_venta=orden_venta).exists()
        # linea_exists = Linea.objects.filter(orden_venta=orden_venta,num_linea=linea).exists()
        
        # if ov_exists and linea_exists:

def visualizarRetiros(request):
    return render(request,'agenda-retiro/buscar-retiro.html') 

def obtenerRetiros(request):
    if request.is_ajax and request.method == 'GET':
        try:
            if('fecha_desde' and 'fecha_hasta' in request.GET):
                fec_desde = datetime.strptime(request.GET.get('fecha_desde',None), "%d/%m/%Y").date()
                fec_hasta = datetime.strptime(request.GET.get('fecha_hasta',None), "%d/%m/%Y").date()
                retiros = Retiro.objects.filter(fecha__range=[fec_desde,fec_hasta])     
                print(retiros)
                list_detalles = []
                for retiro in retiros:
                    print(retiro)
                    # detalle = DetalleRetiro.objects.filter(retiro=retiro.id_retiro)
                    if DetalleRetiro.objects.filter(retiro=retiro.id_retiro).exists():
                        detalles = DetalleRetiro.objects.filter(retiro=retiro.id_retiro)
                        for detalle in detalles:
                            fila = [retiro.fecha,retiro.hora_inicio +' - '+ retiro.hora_fin,detalle.orden_venta,detalle.linea,retiro.cliente,detalle.descripcion,detalle.cantidad,detalle.tipo_embalaje]
                            list_detalles.append(fila)
                        
                    
                    
                return JsonResponse({'valid': True, 'detalle_retiros' : list_detalles}, safe=False, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'valid': False, 'error': True},status=400)