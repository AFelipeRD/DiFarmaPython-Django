from django.contrib import admin
from Bases.models import Proveedor, Producto, ControlTemperatura

# Register your models here.

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre','numpedido','fechapedido','contacto')
    search_fields = ['nombre']
    readonly_fields = ('created','updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Proveedor, ProveedorAdmin)
                   
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre','nproveedor','precio','cantidad','laboratorio','presentacion','ml','mg','vencimiento')
    search_fields = ['nombre']
    readonly_fields = ('created','updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Producto, ProductoAdmin)

class ControlTemperaturaAdmin(admin.ModelAdmin):
    list_display = ('fechacontrol','horacontrol','humedad','temperatura')
    search_fields = ['fechacontrol']
    readonly_fields = ('created','updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(ControlTemperatura, ControlTemperaturaAdmin)

