from typing import Optional
from django.db import models
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
    # cliente         = models.CharField(max_length=150)
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
        
class Linea(models.Model):
    num_linea   = models.IntegerField()
    cantidad    = models.IntegerField()
    estado      = models.CharField(max_length=40)
    orden_venta = models.ForeignKey(OrdenVenta, on_delete=PROTECT)
    articulo    = models.ForeignKey(Articulo, on_delete=PROTECT)
    
    class Meta:
        verbose_name = 'Linea'
        db_table     = 'LINEA'
        
