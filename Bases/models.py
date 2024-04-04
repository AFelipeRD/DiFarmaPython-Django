from django.db import models
from django.forms import model_to_dict

# Create your models here.

# Clases de los Modelos de las Base de Datos
# Clase de los Proveedores
class Proveedor(models.Model):
    nombre = models.CharField(max_length=50, null = True, blank = False)
    numpedido = models.IntegerField(null = True, blank = False)
    fechapedido = models.DateField(max_length=255, null = True, blank = False)
    contacto = models.IntegerField(null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        verbose_name ='Proveedor'
        verbose_name_plural = 'Proveedores'
        
    def __str__(self):
        return self.nombre

#--------------------------------------------------------------------------------------------------------------
# Clase de los Productos
class Producto(models.Model):
    codigo = models.IntegerField(null = True, blank = False)
    nombre = models.CharField(max_length=50, null = True)
    nproveedor = models.CharField(max_length=50, null = True)
    precio = models.IntegerField(null = True, blank = False)
    cantidad = models.IntegerField(null = False, blank = False)
    laboratorio = models.CharField(max_length=50, null = True)
    presentacion = models.CharField(max_length=50, null = True, blank = True)
    ml = models.IntegerField(null = True, blank = True)
    mg = models.IntegerField(null = True, blank = True)
    vencimiento = models.DateField(max_length=255, null = True, blank = False)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        verbose_name ='Producto'
        verbose_name_plural = 'Productos'
  
    def __str__(self):
        return self.nombre

#--------------------------------------------------------------------------------------------------------------
# Clases de los Procedimientos
# Clase del Control de Temperatura
class ControlTemperatura(models.Model):
    fechacontrol = models.DateField(max_length=255, null = True, blank = False)
    horacontrol = models.TimeField(max_length=255, null = True, blank = False)
    humedad = models.IntegerField(null = True, blank = False)
    temperatura = models.IntegerField(null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        verbose_name ='ControlTemperatura'
        verbose_name_plural = 'ControlTemperaturas'
        
    def __str__(self):
        return self.fechacontrol

#--------------------------------------------------------------------------------------------------------------
# Clases de los Modelos de Ventas
# Clase de los Egresos
class Egreso(models.Model):
    fecha_pedido = models.DateField(max_length=255)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pagado = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    comentarios = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    ticket = models.BooleanField(default=True)
    desglosar = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=True , null=True)

    class Meta:
        verbose_name='Egreso'
        verbose_name_plural = 'Egresos'
        order_with_respect_to = 'fecha_pedido'
    
    def __str__(self):
        return str(self.id)

# Clase de los Productos Egreso
class ProductosEgreso(models.Model):
    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2 , null=False)
    precio = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    iva = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    created = models.DateTimeField(auto_now_add=True)
    entregado = models.BooleanField(default=True)
    devolucion = models.BooleanField(default=False)

    class Meta:
        verbose_name='Producto Egreso'
        verbose_name_plural = 'Productos Egreso'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.producto
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['created'])
        return item