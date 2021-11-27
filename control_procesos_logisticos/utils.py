import requests

from control_procesos_logisticos.forms import ArticuloForm, ClienteForm, DespachoForm, LineaForm, OrdenVentaForm, PlanificacionForm, TransporteForm
from .models import Articulo, OrdenVenta,Cliente, Planificacion, Transporte

def crearPlanificacion(ov,linea):
    response = requests.post('http://webservices.gruposentte.cl/DUOC/planificaciones.php', data={
        'ov': ov,
        'linea' : linea
    })

    if response.json()['resultado'] == 0:
        for value in response.json()['data']:
            existe = Planificacion.objects.filter(llave_busqueda=ov+linea).exists()
            if existe:
                data = {'error': True,
                        'detalles': 'La orden de venta ya existe en la planificación'}
                return data
                
    response = requests.post('http://webservices.gruposentte.cl/DUOC/planificaciones.php', data={
        'ov': ov,
        'linea' : linea
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
            articulo = ''
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
                return data
            
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
                return data
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
                return data
            
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
                return data
            data = {
                'error': False,
                'id_ov':id_ov.pk
            }
            return data

