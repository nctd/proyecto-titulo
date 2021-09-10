from django import forms


from .models import OrdenVenta, Planificacion

class planificacionRegistro(forms.ModelForm):
    class Meta:
        model = OrdenVenta
        fields = '__all__'