import io
import pandas as pd
import requests
import cx_Oracle
import xlsxwriter


from django.http.request import QueryDict
from django.http import FileResponse, JsonResponse,HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required, permission_required


from control_procesos_logisticos.forms import ArticuloForm, ClienteForm, CustomUserCreationForm, DespachoForm, DetallePackingListForm, DetalleRetiroForm,\
                                              LineaForm, OrdenVentaForm, PlanificacionForm, RetiroForm, TransporteForm

from .models import Articulo, Cliente, Despacho, DetalleRetiro, IndicadorDespacho, IndicadorTipoVenta, Linea, OrdenVenta, Planificacion, Retiro,Transporte,TemporalLinea
from datetime import date,datetime,timedelta

from .crearPDF import PDF

from .utils import crearPlanificacion


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
@login_required(login_url='/auth/login_user')
def home(request):
    return render(request,'index.html')

@login_required(login_url='/auth/login_user')
def planificacion(request):
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
                                    'detalles': 'La orden de venta: '+value['ov']+', ya existe en la planificación'}
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

                        ov_exists = OrdenVenta.objects.filter(orden_venta=value['ov']).exists()
                        if ov_exists:
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

@login_required(login_url='/auth/login_user')
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
            guia_despacho = Despacho.objects.filter(id_despacho=despacho.id_despacho).values_list('guia_despacho',flat=True).first()
            if guia_despacho == '':
                guia_despacho = '-'
            
            despacho_existe = Despacho.objects.filter(id_despacho=desp)
            if despacho_existe.exists():
                transporte = Transporte.objects.filter(id_transporte=despacho_existe.values_list('transporte_id',flat=True).first())
                if transporte.exists():
                    ot = transporte.values_list('ot',flat=True).first()
                    if ot == '':
                        ot = '-'
                else:
                    ot = '-'
        
            cita_valida = DetalleRetiro.objects.filter(orden_venta=request.GET['id_ov'])
            if cita_valida.exists():
                cita = Retiro.objects.filter(id_retiro=cita_valida.values_list('retiro_id',flat=True).first())
                cita_pl = cita.values_list('id_retiro',flat=True).first()
            else:
                cita_pl = '-'
            data = {
                'orden_venta': ov,
                'cliente' : ov.cliente.nombre,
                'orden_compra': ov.orden_compra,
                'tipo_venta': ov.tipo_venta,
                'tipo_despacho': ov.tipo_despacho,
                'canal_venta': ov.canal_venta,
                'despacho': despacho,
                'guia_despacho': guia_despacho,
                'lineas': lineas,
                'tipo_despacho': ov.tipo_despacho,
                'cita': cita_pl,
                'ot': ot
            }
            

            data['response'] = 'OV ENCONTRADA'
            data['existe'] = True
            return render(request,'tracking/tracking.html',data)
        except ObjectDoesNotExist:
            data = {
                'error': True
            }
            
            return render(request,'tracking/tracking.html',data)
    else:
        return render(request,'tracking/tracking.html')


@login_required(login_url='/auth/login_user')
def indicadores(request):
    try:
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
                
                # Tipo de venta
                'datos_stock' : datos_stock,
                'datos_stock_r' : datos_stock_r,
                'datos_calzado' : datos_calzado,
                'datos_liquida' : datos_liquida,
                'datos_proyect' : datos_proyect,
                'datos_os' : datos_os,

                # Progreso diario - Tipo de despacho
                'datos_progreso': progreso_despachos,

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
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
            data = {'error': True, 'detalles': e.message}
            return render(request,'planificacion/planificacion.html',data)
        else:
            print(e)        
    
    return render(request,'indicadores/indicadores.html')

@login_required(login_url='/auth/login_user')
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
                # for i in range(delta.days + 1):
                for i in range(delta.days):
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
                'lista_fechas': 'No hay fechas para crear el gráfico',
                },
                status = 200)
            
        if tipo == 'tipo_despacho':
            reportes_despacho = IndicadorDespacho.objects.filter(fecha__range=(fecha_inicio,fecha_fin)).order_by('fecha').values_list()
            list_fecha_despacho = []
            list_cumplimientos = []
            
            if reportes_despacho:
                # for i in range(delta.days + 1):
                for i in range(delta.days):
                    fecha = fecha_inicio + timedelta(days=i)
                    list_fecha_despacho.append(fecha)
                    
                    
                tipos_despacho = OrdenVenta.objects.all().values_list('tipo_despacho',flat=True).distinct()
                for despacho in tipos_despacho:
                    cumplimiento = reportes_despacho.filter(tipo_despacho=despacho)
                    # print(cumplimiento)
                    list_cumplimientos.append(cumplimiento)
                    # print(cumplimiento)
                list_cumpl_despachos = []
                list_total_despachos = []
                for cumplimiento in list_cumplimientos:
                    for fecha in list_fecha_despacho:
                        if cumplimiento:
                            if fecha in cumplimiento.values_list('fecha',flat=True):
                                list_cumpl_despachos.append(cumplimiento.values_list('estado_final',flat=True).filter(fecha=fecha).first())
                            else:
                                list_cumpl_despachos.append(0)

                    data_despachos = {'despacho' : cumplimiento.values_list('tipo_despacho',flat=True).first(),
                                'valores': list_cumpl_despachos}
                    list_total_despachos.append(data_despachos)
                    list_cumpl_despachos = []
                return JsonResponse({
                    'valid':True,
                    'lista_fechas': list_fecha_despacho,
                    'despachos': list_total_despachos,
                }, status=200)
                
            else:
                list_fecha_tipo_venta = [0]
                
            return JsonResponse({
                'valid':False,
                'lista_fechas': 'No hay fechas',
                },
                status = 200)
            
    return JsonResponse({}, status = 400)

@login_required(login_url='/auth/login_user')
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
        
        valido = Retiro.objects.filter(fecha=datetime.strptime(request.POST['fecha-retiro'], "%d/%m/%Y").date(),activo=0)
        if valido.exists():
            for value in valido:
                existe = DetalleRetiro.objects.filter(retiro=value.id_retiro,activo=0,orden_venta=ov.split('-')[0],linea=ov.split('-')[1])
                print(existe)
                if existe.exists():
                    data = {
                        'error': True,
                        'detalles': 'Ya existe un retiro programado para la orden de venta ingresada'
                    }
                    return render(request,'agenda-retiro/agendar.html',data)
        
        retiro = RetiroForm(data=data_retiro)
        if retiro.is_valid():
            id_retiro = retiro.save()
            # file = retiroGenerarPDF(request,data_retiro,data,str(id_retiro.pk))

            for item in data:  
                print(item)
                data_det = {
                    'orden_venta' : item[0],
                    'linea' : item[1],
                    'descripcion' : item[2],
                    'cantidad' : item[3],
                    'tipo_embalaje' : item[4],
                    'retiro' : id_retiro.pk
                }
                det_retiro = DetalleRetiroForm(data=data_det)
                if det_retiro.is_valid():
                    det_retiro.save()
                    
                    orden_venta = crearPlanificacion(item[0],item[1])
                    print(orden_venta)
                    if orden_venta['error']:
                        print('ERRORORORRO')
                        return render(request,'agenda-retiro/agendar.html',orden_venta)
                    else:
                        data_plan = {
                            'llave_busqueda': item[0]+item[1],
                            'fecha_planificacion': datetime.strptime(request.POST['fecha-retiro'], "%d/%m/%Y").date(),
                            # 'orden_venta': item[0]
                            'orden_venta': orden_venta['id_ov']
                        }
                        # print(data_plan)
                        pl = PlanificacionForm(data=data_plan)
                        if pl.is_valid():
                            pl.save()
                        else:
                            data = {
                                'error': True,
                                'detalles': 'Error al crear la planificación'+ str(pl.errors.as_data())
                            }
                            return render(request,'agenda-retiro/agendar.html',data)
                else:
                    data = {
                        'error': True, 
                        'detalles': 'Error al registrar detalles del retiro' + str(det_retiro.errors.as_data())
                    }
                    return render(request,'agenda-retiro/agendar.html',data)
                   
            data = {
                'guardado': True,
                'retiro': str(id_retiro.pk)
            }

            return render(request,'agenda-retiro/agendar.html',data)
            
        else:
            data = {
                'error': True,
                'detalles': 'Error al registrar el retiro' + str(retiro.errors.values())
            }
            return render(request,'agenda-retiro/agendar.html',data)   
    return render(request,'agenda-retiro/agendar.html')   

@login_required(login_url='/auth/login_user')
def retiroGenerarPDF(request,data_retiro,data_detalle,id_retiro):
    pdf = PDF()
    pdf.add_page()
    
    # pdf.set_font("Arial", size = 15)
    
    pdf.titles('CITA NRO '+id_retiro)
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
    
    pdf.output("pdf/CITA"+id_retiro+".pdf",'F')
    return FileResponse(open("pdf/CITA"+id_retiro+".pdf", 'rb'), as_attachment=True, content_type='application/pdf')

@login_required(login_url='/auth/login_user')
def validarOrdenVentaRetiro(request):
    if request.is_ajax and request.method == 'GET':
        orden_venta = request.GET.get('orden_venta',None)
        linea = request.GET.get('linea',None)
        cliente = request.GET.get('cliente',None)
        if cliente == '':
            cliente = None
        validar = ''
        
        response = requests.post('http://webservices.gruposentte.cl/DUOC/planificaciones.php', data={
            'ov': orden_venta,
            'linea' : linea
        })
        
        if response.json()['resultado'] == 1:
            return JsonResponse({'valid':False})
        else:
            for value in response.json()['data']:
                validar = value['cliente']

            if cliente != None:
                if cliente == validar:
                    if response.json()['resultado'] == 0 and response.status_code == 200:
                        return JsonResponse({'valid':True, 'cliente': cliente}, status=200)
                else:
                    return JsonResponse({'valid':False, 'cliente':False,'detalles':'La orden de venta no pertenece al mismo cliente'}, status=400)

            if cliente == None:
                if response.json()['resultado'] == 0 and response.status_code == 200:
                    return JsonResponse({'valid':True, 'cliente': validar}, status=200)
                else:
                    return JsonResponse({'valid':False}, status=400)

@login_required(login_url='/auth/login_user')
def visualizarRetiros(request):
    if request.method == 'GET':
        data = {'res' : ''}
        try:
            if('fecha-desde' and 'fecha-hasta' in request.GET):
                val1 = request.GET['fecha-desde']
                val2 = request.GET['fecha-hasta']
                fec_desde = datetime.strptime(request.GET['fecha-desde'], "%d/%m/%Y").date()
                fec_hasta = datetime.strptime(request.GET['fecha-hasta'], "%d/%m/%Y").date()
                retiros = Retiro.objects.filter(fecha__range=[fec_desde,fec_hasta],activo=0)     

                list_detalles = []
                for retiro in retiros:
                    # detalle = DetalleRetiro.objects.filter(retiro=retiro.id_retiro)
                    if DetalleRetiro.objects.filter(retiro=retiro.id_retiro).exists():
                        detalles = DetalleRetiro.objects.filter(retiro=retiro.id_retiro,activo=0)
                        for detalle in detalles:
                            fila = {
                                'fecha': retiro.fecha,
                                'rango_horario': retiro.hora_inicio +' - '+ retiro.hora_fin,
                                'orden_venta': detalle.orden_venta,
                                'linea' : detalle.linea,
                                'cliente': retiro.cliente,
                                'descripcion': detalle.descripcion,
                                'cantidad': detalle.cantidad,
                                'tipo_embalaje': detalle.tipo_embalaje,
                                'retiro' : retiro.id_retiro
                            }
                            # fila = [retiro.fecha,retiro.hora_inicio +' - '+ retiro.hora_fin,detalle.orden_venta,detalle.linea,retiro.cliente,detalle.descripcion,detalle.cantidad,detalle.tipo_embalaje]
                            list_detalles.append(fila)
                data = {
                    'detalle_retiros' : list_detalles,
                    'fec_inicio': val1,
                    'fec_hasta' : val2
                }
            return render(request,'agenda-retiro/buscar-retiro.html',data) 
        except:
            return render(request,'agenda-retiro/buscar-retiro.html') 
    return render(request,'agenda-retiro/buscar-retiro.html') 

@login_required(login_url='/auth/login_user')
def buscarRetiroPDF(request):
    # if request.is_ajax and request.method == 'POST':
    if request.GET.get('retiro',None):
        # retiro = Retiro.objects.filter(id_retiro=request.POST['retiro'])
        retiro = Retiro.objects.filter(id_retiro=request.GET.get('retiro',None),activo=0)
        data_retiro = {}
        data_detalle = []
        for value in retiro:

            data_retiro = {
                'fecha': datetime.strptime(str(value.fecha), '%Y-%m-%d').strftime('%d/%m/%y'),
                'hora_inicio': value.hora_inicio,
                'hora_fin': value.hora_fin,
                'cliente': value.cliente,
                'direccion': value.direccion,
            }
            
            # detalles = DetalleRetiro.objects.filter(retiro=request.POST['retiro'])
            detalles = DetalleRetiro.objects.filter(retiro=request.GET.get('retiro',None),activo=0)

            for det in detalles:
                detalle = [
                    det.orden_venta,
                    str(det.linea),
                    det.descripcion,
                    str(det.cantidad),
                    det.tipo_embalaje]
                data_detalle.append(detalle)

        # retiroGenerarPDF(request,data_retiro,data_detalle,request.POST['retiro'])
        return retiroGenerarPDF(request,data_retiro,data_detalle,request.GET.get('retiro',None))
        
    #     return JsonResponse({'valid':True},status=200)
    # else:
    #     return JsonResponse({'valid':False},status=400)
    
@login_required(login_url='/auth/login_user')    
def generarReporteRetiros(request):

    # if request.is_ajax and request.method == 'POST':
    # response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # response['Content-Disposition'] = 'attachment; filename="test.xlsx"'

    fec_desde = datetime.strptime(request.GET.get('fecha_desde',None), "%d/%m/%Y").date()
    fec_hasta = datetime.strptime(request.GET.get('fecha_hasta',None), "%d/%m/%Y").date()
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    
    columns = ['FECHA','RANGO HORARIO','ORDEN DE VENTA', 'LÍNEA OV', 'CLIENTE', 'DESCRIPCIÓN', 'CANTIDAD', 'TIPO EMBALAJE']
    row_num = 0
    cell_format = workbook.add_format({'bold': True})
    # Write some test data.
    for col_num in range(len(columns)):
            worksheet.set_column(0,3,20)
            worksheet.set_column(4,5,40)
            worksheet.set_column(6,7,20)
            worksheet.write(row_num, col_num, columns[col_num],cell_format)
            
    filas = Retiro.objects.filter(fecha__range=[fec_desde,fec_hasta],activo=0)   

    list_detalles = []
    for retiro in filas:
        # detalle = DetalleRetiro.objects.filter(retiro=retiro.id_retiro)
        if DetalleRetiro.objects.filter(retiro=retiro.id_retiro).exists():
            detalles = DetalleRetiro.objects.filter(retiro=retiro.id_retiro,activo=0)
            for detalle in detalles:
                fila = [datetime.strptime(str(retiro.fecha), '%Y-%m-%d').strftime('%d-%m-%y'),retiro.hora_inicio +' - '+ retiro.hora_fin,detalle.orden_venta,detalle.linea,retiro.cliente,detalle.descripcion,detalle.cantidad,detalle.tipo_embalaje]
                list_detalles.append(fila)
    for fila in list_detalles:
        row_num += 1
        for col_num in range(len(fila)):
            worksheet.write(row_num, col_num, fila[col_num])

    workbook.close()


    output.seek(0)
    filename = 'reporte_'+str(date.today())+'.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

@login_required(login_url='/auth/login_user')
def anularRetiro(request):
    if request.is_ajax and request.method == 'PUT':
        put = QueryDict(request.body)
        retiro = put.get('retiro')
        linea = put.get('linea')
        # retiro = Retiro.objects.filter(id_retiro=retiro)
        anular = DetalleRetiro.objects.filter(retiro_id=retiro,linea=linea).update(activo=1)
        print(anular)
        if anular > 0:
            return JsonResponse({'valid': True})
        else:
            return JsonResponse({'valid': False})
        
      
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('planificacion')
        else:
            messages.error(request,'Nombre de usuario y/o contraseña incorrectos')
            return redirect('login')
            # return HttpResponse("Invalid login. Please try again.")
    return render(request, 'auth/login_user.html')

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)

        if formulario.is_valid():
            formulario.save()

            return redirect(to='/auth/login_user?register=true')
        data['form'] = formulario
    return render(request,'auth/registro.html',data) 


def packingList(request):
    data = {
        'form_detalle': DetallePackingListForm(),
    }
    return render(request,'packing-list/packing-list.html',data)