from typing import Optional
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import PROTECT
from datetime import date, datetime


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=70,blank=True,default='')
    direccion = models.CharField(max_length=120,blank=True,default='')
    telefono = models.CharField(max_length=50,blank=True,default='')
    nom_contacto = models.CharField(max_length=50,blank=True,default='')
    correo_contacto = models.CharField(max_length=60,blank=True,default='')
    
    class Meta:
        verbose_name = 'Cliente'
        db_table = 'CLIENTE'
        

class OrdenVenta(models.Model):
    orden_venta     = models.CharField(max_length=25,primary_key=True)
    cliente         = models.ForeignKey(Cliente,on_delete=PROTECT)
    tipo_pago       = models.CharField(max_length=30,verbose_name='Tipo de pago')
    tipo_venta      = models.CharField(max_length=30,verbose_name='Tipo de venta')
    canal_venta     = models.CharField(max_length=20)
    orden_compra    = models.CharField(max_length=50)

    def __str__(self):
        return self.orden_venta
    
    class Meta:
        verbose_name = 'OrdenVenta'
        db_table = 'ORDEN_VENTA'
        
        
        
        
class Planificacion(models.Model):
    id_planificacion    = models.AutoField(primary_key=True)
    llave_busqueda      = models.CharField(max_length=30,blank=True)
    fecha_planificacion = models.DateField()
    orden_venta         = models.ForeignKey(OrdenVenta, on_delete=PROTECT)
    
    
    class Meta:
        verbose_name = 'Planificacion'
        db_table     = 'PLANIFICACION'
        
class Articulo(models.Model):
    cod_articulo = models.CharField(max_length=30,primary_key=True)
    descripcion = models.CharField(max_length=120,blank=True,default='')
    
    class Meta:
        verbose_name = 'Articulo'
        db_table = 'ARTICULO'

class Transporte(models.Model):
    id_transporte    = models.AutoField(primary_key=True)
    ot = models.CharField(max_length=20,blank=True,default='')
    empresa = models.CharField(max_length=30,blank=True,null=True,default='')
    activo = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Transporte'
        db_table     = 'TRANSPORTE'

        
class Despacho(models.Model):
    id_despacho    = models.AutoField(primary_key=True)
    direccion     = models.CharField(max_length=100,blank=True,default='')
    comuna        = models.CharField(max_length=80,blank=True,default='')
    tipo_despacho = models.CharField(max_length=50,blank=True,default='')
    guia_despacho = models.CharField(max_length=50,blank=True,default=None)
    transporte    = models.ForeignKey(Transporte, on_delete=PROTECT)
    activo        = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Despacho'
        db_table     = 'DESPACHO'
    



class Linea(models.Model):
    id_linea    = models.AutoField(primary_key=True)
    num_linea   = models.IntegerField()
    cantidad    = models.IntegerField()
    estado      = models.CharField(max_length=40)
    orden_venta = models.ForeignKey(OrdenVenta, on_delete=PROTECT)
    articulo    = models.ForeignKey(Articulo, on_delete=PROTECT)
    despacho    = models.ForeignKey(Despacho,on_delete=PROTECT)
    activo      = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Linea'
        db_table     = 'LINEA'
        
        
class TemporalLinea(models.Model):
    id_linea    = models.AutoField(primary_key=True)
    num_linea   = models.IntegerField()
    orden_venta = models.CharField(max_length=40,blank='')

    
    class Meta:
        verbose_name = 'Temp_Linea'
        db_table     = 'TMP_LINEA'
        

class Bulto(models.Model):
    id_bulto = models.AutoField(primary_key=True)
    linea = models.ForeignKey(Linea,on_delete=PROTECT)
    activo   = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Bulto'
        db_table     = 'BULTO'

class DetalleBulto(models.Model):
    id_detalle_bulto    = models.AutoField(primary_key=True)
    cantidad   = models.IntegerField()
    largo      = models.IntegerField()
    ancho      = models.DecimalField(max_digits=10, decimal_places=5)
    volumen    = models.DecimalField(max_digits=10, decimal_places=5)
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=5)
    peso_neto  = models.DecimalField(max_digits=10, decimal_places=5)
    bulto      = models.ForeignKey(Bulto, on_delete=PROTECT)
    
    class Meta:
        verbose_name = 'Detalle_Bulto'
        db_table     = 'DETALLE_BULTO'
    
class Retiro(models.Model):
    id_retiro    = models.AutoField(primary_key=True)
    fecha_hora  = models.DateTimeField(default=datetime.now)
    hora_inicio = models.TimeField()
    hora_fin    = models.TimeField()
    cliente     = models.CharField(max_length=40)
    despacho = models.ForeignKey(Despacho,on_delete=PROTECT)
    activo      = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name = 'Retiro'
        db_table     = 'RETIRO'
    
class DetalleRetiro(models.Model):
    id_detalle_retiro    = models.AutoField(primary_key=True)
    orden_venta = models.CharField(max_length=40)
    linea = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=40)
    cantidad = models.IntegerField()
    tipo_embalaje = models.CharField(max_length=40)
    retiro = models.ForeignKey(Retiro,on_delete=PROTECT)
    
    class Meta:
        verbose_name = 'Detalle_Retiro'
        db_table     = 'DETALLE_Retiro'
    
class Cita(models.Model):
    id_cita            = models.AutoField(primary_key=True)
    fecha              = models.DateField()
    hora               = models.TimeField()
    operador_logistico = models.CharField(max_length=40)
    despacho = models.ForeignKey(Despacho,on_delete=PROTECT)
    activo             = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Cita'
        db_table     = 'CITA'

class DetalleCita(models.Model):
    id_detalle_cita    = models.AutoField(primary_key=True)
    orden_venta = models.CharField(max_length=40)
    linea = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=40)
    cantidad = models.IntegerField()
    tipo_embalaje = models.CharField(max_length=40)
    cita = models.ForeignKey(Cita,on_delete=PROTECT)
    
    class Meta:
        verbose_name = 'Detalle_Cita'
        db_table     = 'DETALLE_CITA'
    

class IndicadorDespacho(models.Model):
    id_int_dep = models.AutoField(primary_key=True)
    tipo_venta = models.CharField(max_length=20,blank=True)
    cantidad_despacho = models.IntegerField()
    exitos = models.IntegerField()
    estado_final = models.IntegerField()
    fecha = models.DateField()
    activo = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Indicador_Despacho'
        db_table     = 'INDICADOR_DESPACHO'
    
class IndicadorTipoVenta(models.Model):
    id_int_tp    = models.AutoField(primary_key=True)
    tipo_venta = models.CharField(max_length=20,blank=True)
    cantidad_despacho = models.IntegerField()
    exitos = models.IntegerField()
    estado_final = models.IntegerField()
    fecha = models.DateField()
    activo = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Indicador_Tipo_Venta'
        db_table     = 'INDICADOR_TIPO_VENTA'
        
class LineaNoLiberada(models.Model):
    cod_lnl = models.AutoField(primary_key=True)
    orden_venta = models.CharField(max_length=20)
    cod_articulo = models.CharField(max_length=30)
    linea = models.IntegerField()
    descripcion_articulo = models.CharField(max_length=30)
    cantidad = models.IntegerField()
    activo = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Linea_No_Liberada'
        db_table     = 'LINEA_NO_LIBERADA'
        
class LineaPicking(models.Model):
    cod_lp = models.AutoField(primary_key=True)
    orden_venta = models.CharField(max_length=20)
    cod_articulo = models.CharField(max_length=30)
    linea = models.IntegerField()
    descripcion_articulo = models.CharField(max_length=30)
    cantidad = models.IntegerField()
    activo = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Linea_Picking'
        db_table     = 'LINEA_PICKING'
        
        
class LineaEmbalaje(models.Model):
    cod_le = models.AutoField(primary_key=True)
    orden_venta = models.CharField(max_length=20)
    cod_articulo = models.CharField(max_length=30)
    linea = models.IntegerField()
    descripcion_articulo = models.CharField(max_length=30)
    cantidad = models.IntegerField()
    activo = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Linea_Embalaje'
        db_table     = 'LINEA_EMBALAJE'
        
class LineaReparto(models.Model):
    cod_lr = models.AutoField(primary_key=True)
    orden_venta = models.CharField(max_length=20)
    cod_articulo = models.CharField(max_length=30)
    linea = models.IntegerField()
    descripcion_articulo = models.CharField(max_length=30)
    cantidad = models.IntegerField()
    activo = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Linea_Reparto'
        db_table     = 'LINEA_REPARTO'