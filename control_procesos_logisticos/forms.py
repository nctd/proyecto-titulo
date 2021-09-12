from django import forms
from django.core.exceptions import ValidationError
# from import_export import widgets


from .models import Articulo, Cliente, Linea, OrdenVenta, Planificacion

class OrdenVentaForm(forms.ModelForm):
    
    # def validate_ov(self):
    #     ov = self.cleaned_data['orden_venta']
    #     exists = OrdenVenta.objects.filter(rut__iexact=ov).exists()
        
    #     if exists:
    #         print('Esta orden de venta ya tiene una planificación registrada')
    #     return ov    
    class Meta:
        model = OrdenVenta
        fields = '__all__'
        
    
class PlanificacionForm(forms.ModelForm):
    class Meta:
        model = Planificacion
        fields = '__all__'
        widgets = {
            'fecha_planificacion':
                forms.TextInput(attrs={
                    'class':'form-control',
                    'type': 'text',
                    'id':'datepicker-icon-prepend',
                    'placeholder': 'Fecha'
                })
        }
        
class LineaForm(forms.ModelForm):
    class Meta:
        model = Linea
        fields = '__all__'
        
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        
class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = '__all__'        