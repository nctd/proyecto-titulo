from typing import Optional
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import PROTECT


class Cliente(models.Model):
    nombre = models.CharField(max_length=50,blank=True,default='')
    direccion = models.CharField(max_length=50,blank=True,default='')
    telefono = models.CharField(max_length=50,blank=True,default='')
    nom_contacto = models.CharField(max_length=50,blank=True,default='')
    correo_contacto = models.CharField(max_length=50,blank=True,default='')
    
    class Meta:
        verbose_name = 'Cliente'
        db_table = 'CLIENTE'
        

class OrdenVenta(models.Model):
    orden_venta     = models.CharField(max_length=20,primary_key=True)
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
    llave_busqueda      = models.CharField(max_length=30)
    fecha_planificacion = models.DateField()
    orden_venta         = models.ForeignKey(OrdenVenta, on_delete=PROTECT)
    
    def __str__(self):
        return self.llave_busqueda
    
    class Meta:
        verbose_name = 'Planificacion'
        db_table     = 'PLANIFICACION'
        
class Articulo(models.Model):
    cod_articulo = models.CharField(max_length=30,primary_key=True)
    descripcion = models.CharField(max_length=50,blank=True,default='')
    
    class Meta:
        verbose_name = 'Articulo'
        db_table = 'ARTICULO'

class Transporte(models.Model):
    ot = models.CharField(max_length=20,blank=True,default='')
    empresa = models.CharField(max_length=30,blank=True,default='')
    eliminado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Transporte'
        db_table     = 'TRANSPORTE'

        
class Despacho(models.Model):
    direccion = models.CharField(max_length=50,blank=True,default='')
    comuna = models.CharField(max_length=40,blank=True,default='')
    tipo_despacho = models.CharField(max_length=30,blank=True,default='')
    guia_despacho = models.CharField(max_length=30,blank=True,default='')
    transporte = models.ForeignKey(Transporte, on_delete=PROTECT)
    eliminado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Despacho'
        db_table     = 'DESPACHO'
    



class Linea(models.Model):
    num_linea   = models.IntegerField()
    cantidad    = models.IntegerField()
    estado      = models.CharField(max_length=40)
    orden_venta = models.ForeignKey(OrdenVenta, on_delete=PROTECT)
    articulo    = models.ForeignKey(Articulo, on_delete=PROTECT)
    despacho    = models.ForeignKey(Despacho,on_delete=PROTECT)
    
    class Meta:
        verbose_name = 'Linea'
        db_table     = 'LINEA'