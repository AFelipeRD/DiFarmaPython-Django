from django import forms
from Bases.models import Proveedor, Producto, ControlTemperatura

#--------------------------------------------------------------------------------------------------------------

# Clases de los Formularios de las Bases de Datos (Proveedores, Productos)
# Formulario para Agregar Proveedores
class AddProveedorForm (forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ('nombre','numpedido','fechapedido','contacto')
        labels = {
            'nombre': 'Nombre Proveedor',
            'numpedido': 'Pedido Número',
            'fechapedido': 'Fecha',
            'contacto': 'Teléfono (Contacto)'
        }
        
# Formulario para Editar Proveedores
class EditarProveedorForm (forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ('nombre','numpedido','fechapedido','contacto')
        labels = {
            'nombre': 'Nombre Proveedor',
            'numpedido': 'Pedido Número',
            'fechapedido': 'Fecha',
            'contacto': 'Teléfono (Contacto)'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar'}),
            'numpedido': forms.NumberInput(attrs={'id': 'numpedido_editar'}),
            'fechapedido': forms.DateInput(attrs={'id': 'fechapedido_editar'}),
            'contacto': forms.NumberInput(attrs={'id': 'contacto_editar'})
        }

#--------------------------------------------------------------------------------------------------------------
# Formulario para Agregar Productos
class AddProductoForm (forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('codigo','nombre','nproveedor','precio','cantidad','laboratorio','presentacion','ml','mg','vencimiento')
        labels = {
            'codigo': 'Codigo',
            'nombre': 'Nombre Producto',
            'nproveedor': 'Proveedor',
            'precio': 'Precio (Costo)',
            'cantidad': 'Cantidad',
            'laboratorio': 'Laboratorio',
            'presentacion': 'Presentación',
            'ml':'Mililitros',
            'mg':'Miligramos',
            'vencimiento': 'Fecha de Vencimiento'
        }

# Formulario para Editar Productos
class EditarProductoForm (forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('codigo','nombre','nproveedor','precio','cantidad','laboratorio','presentacion','ml','mg','vencimiento')
        labels = {
            'codigo': 'Codigo',
            'nombre': 'Nombre Producto',
            'nproveedor': 'Proveedor',
            'precio': 'Precio (Costo)',
            'cantidad': 'Cantidad',
            'laboratorio': 'Laboratorio',
            'presentacion': 'Presentación',
            'ml':'Mililitros',
            'mg':'Miligramos',
            'vencimiento': 'Fecha de Vencimiento'
        }
        widgets = {
            'codigo': forms.NumberInput(attrs={'id': 'codigo_editar'}),
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar'}),
            'nproveedor': forms.TextInput(attrs={'id': 'nproveedor_editar'}),
            'precio': forms.NumberInput(attrs={'id': 'precio_editar'}),
            'cantidad': forms.NumberInput(attrs={'id': 'cantidad_editar'}),
            'laboratorio': forms.TextInput(attrs={'id': 'laboratorio_editar'}),
            'presentacion': forms.TextInput(attrs={'id': 'presentacion_editar'}),
            'ml': forms.NumberInput(attrs={'id': 'ml_editar'}),
            'mg': forms.NumberInput(attrs={'id': 'mg_editar'}),
            'vencimiento': forms.DateInput(attrs={'id': 'vencimiento_editar'})
        }

#--------------------------------------------------------------------------------------------------------------

# Clases de los Formularios de las Bases de Datos (ControlTemperaturaes, Productos)
# Formulario para Agregar ControlTemperaturaes
class AddControlTemperaturaForm (forms.ModelForm):
    class Meta:
        model = ControlTemperatura
        fields = ('fechacontrol','horacontrol','humedad','temperatura')
        labels = {
            'fechacontrol': 'Fecha del Control',
            'horacontrol': 'Hora',
            'humedad': 'Humedad',
            'temperatura': 'Temperatura (Grados)'
        }
        
# Formulario para Editar ControlTemperaturaes
class EditarControlTemperaturaForm (forms.ModelForm):
    class Meta:
        model = ControlTemperatura
        fields = ('fechacontrol','horacontrol','humedad','temperatura')
        labels = {
            'fechacontrol': 'Fecha del Control',
            'horacontrol': 'Hora',
            'humedad': 'Humedad',
            'temperatura': 'Temperatura (Grados)'
        }
        widgets = {
            'fechacontrol': forms.DateInput(attrs={'id': 'fechacontrol_editar'}),
            'horacontrol': forms.TimeInput(attrs={'id': 'horacontrol_editar'}),
            'humedad': forms.NumberInput(attrs={'id': 'humedad_editar'}),
            'temperatura': forms.NumberInput(attrs={'id': 'temperatura_editar'})
        }