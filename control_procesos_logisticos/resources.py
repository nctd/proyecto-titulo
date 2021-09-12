from import_export import resources
from .models import OrdenVenta, Planificacion



class OrdenVentaResource(resources.ModelResource):
    class Meta:
        model = OrdenVenta
        fields = '__all__'
        
 
        
        
        
class PlanificacionResource(resources.ModelResource):
    class Meta:
        model = Planificacion
        