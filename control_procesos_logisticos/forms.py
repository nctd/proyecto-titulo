from django import forms
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Articulo, Bulto, Cita, Cliente, Despacho, DetalleBulto, DetalleCita, DetalleRetiro, IndicadorTipoVenta, Linea, OrdenVenta, Planificacion, Transporte ,TemporalLinea, Retiro

class OrdenVentaForm(forms.ModelForm):
    
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
                    'placeholder': 'Fecha',
                    'autocomplete': 'off' 
                },)
        }
        
class DespachoForm(forms.ModelForm):
    class Meta:
        model = Despacho
        fields = '__all__'
     
class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = '__all__' 
        
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
        
class TemporalLineaForm(forms.ModelForm):
    class Meta:
        model = TemporalLinea
        fields = '__all__'
        
class IndicadorTipoVentaForm(forms.ModelForm):
    class Meta:
        model = IndicadorTipoVenta
        fields = '__all__'
        
class RetiroForm(forms.ModelForm):
    class Meta:
        model = Retiro
        fields = '__all__'

class DetalleRetiroForm(forms.ModelForm):
    class Meta:
        model = DetalleRetiro
        fields = '__all__'
        
class DetalleBultoForm(forms.ModelForm):
    class Meta:
        model = DetalleBulto
        fields = '__all__'
        
        
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password','id':'password1'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password','id':'password2'}),
    )
    first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','type': 'text','id':'first_name'}))
    last_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','type': 'text','id':'last_name'})) 


    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password1',
            'password2'
        ]
        widgets = {
            'username':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id':'username'
                },),
            'email':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'email',
                    'id':'email',
                },),
                            
        }

        
class BultoPackingListForm(forms.ModelForm):
    class Meta:
        model = Bulto
        fields = ['orden_venta','tipo_bulto','largo','ancho','alto','volumen','peso_bruto','peso_neto','activo']
        # fields = ['orden_venta','tipo_bulto','largo','ancho','volumen','peso_bruto','peso_neto']
        widgets = {
            'orden_venta':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id':'bulto_ov',
                    # 'name': 'bulto_ov'
                },),
            'tipo_bulto':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id':'tipo_bulto'
                },),
            'largo':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id':'bulto_largo',
                },),
            'ancho':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id':'bulto_ancho',
                },),
            'alto':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id':'bulto_alto',
                },),
            'volumen':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id':'bulto_volumen',
                },),
            'peso_bruto':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id':'bulto_peso_bruto',
                },),
            'peso_neto':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id':'bulto_peso_neto',
                },),          
        }

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
            'operador_logistico':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id':'operador_logistico',
                },),      
            'fecha_cita':
                forms.TextInput(attrs={
                    'class':'form-control',
                    'type': 'text',
                    'id':'fecha_cita',
                    'placeholder': 'Fecha',
                    'autocomplete': 'off' 
                },),
            'hora_cita':
                forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'time',
                    'id':'hora_cita',
                },),     

        }
        
class DetalleCitaForm(forms.ModelForm):
    class Meta:
        model = DetalleCita
        fields = '__all__'