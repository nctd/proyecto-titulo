from django.db import models


class OrdenVenta(models.Model):
    orden_venta     = models.CharField(max_length=20,primary_key=True)
    cliente         = models.CharField(max_length=150)
    tipo_pago       = models.CharField(max_length=30,verbose_name='Tipo de pago')
    tipo_venta      = models.CharField(max_length=30,verbose_name='Tipo de venta')
    sol_material    = models.CharField(max_length=50,verbose_name='Solicitud material')
    orden_compra    = models.CharField(max_length=50)
    correo_contacto = models.CharField(max_length=50,verbose_name='Correo contacto cliente')
    canal_venta     = models.CharField(max_length=20)

    def __str__(self):
        return self.orden_venta
    
    class Meta:
        verbose_name = 'OrdenVenta'
        db_table = 'ORDEN_VENTA'