"""Modelos de datos de DiFarma.

Convenciones aplicadas:
- `created` usa auto_now_add (se fija UNA vez al crear) y `updated` usa
  auto_now (se refresca en cada guardado). Nunca al revés.
- El dinero SIEMPRE es DecimalField; los teléfonos y códigos son CharField
  (los identificadores no son números con los que se calcula).
- Todo __str__ devuelve una cadena segura aunque el campo sea nulo.
"""
from django.db import models
from django.forms import model_to_dict


# ------------------------------------------------------------------------------------------------------------------
# PROVEEDORES
# ------------------------------------------------------------------------------------------------------------------
class Proveedor(models.Model):
    """Proveedor de productos farmacéuticos."""

    nombre = models.CharField(max_length=50, null=True, blank=False)
    numpedido = models.IntegerField(null=True, blank=False)
    fechapedido = models.DateField(null=True, blank=False)
    # Teléfono como texto: conserva ceros iniciales y signos (+57...).
    contacto = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre or ""


# ------------------------------------------------------------------------------------------------------------------
# PRODUCTOS (INVENTARIO)
# ------------------------------------------------------------------------------------------------------------------
class Producto(models.Model):
    """Producto del inventario de la farmacia."""

    # Código como texto: es un identificador, no una cantidad.
    codigo = models.CharField(max_length=20, null=True, blank=False)
    nombre = models.CharField(max_length=50, null=True)
    nproveedor = models.CharField(max_length=50, null=True)
    # Dinero como DecimalField: los enteros pierden los centavos.
    precio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=False, default=0)
    cantidad = models.IntegerField(null=False, blank=False, default=0)
    laboratorio = models.CharField(max_length=50, null=True)
    presentacion = models.CharField(max_length=50, null=True, blank=True)
    ml = models.IntegerField(null=True, blank=True)
    mg = models.IntegerField(null=True, blank=True)
    vencimiento = models.DateField(null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre or ""

    def toJSON(self):
        """Serialización simple para el autocompletado del punto de venta.

        Se excluyen las fechas porque JSON no las serializa directamente.
        """
        return model_to_dict(self, exclude=["created", "updated", "vencimiento"])


# ------------------------------------------------------------------------------------------------------------------
# CONTROL DE TEMPERATURA (cadena de frío)
# ------------------------------------------------------------------------------------------------------------------
class ControlTemperatura(models.Model):
    """Registro de temperatura y humedad para la cadena de frío."""

    fechacontrol = models.DateField(null=True, blank=False)
    horacontrol = models.TimeField(null=True, blank=False)
    humedad = models.IntegerField(null=True, blank=False)
    # Temperatura con decimales: 2,5 °C es un valor válido y frecuente.
    temperatura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ControlTemperatura"
        verbose_name_plural = "ControlTemperaturas"

    def __str__(self):
        return str(self.fechacontrol or "")


# ------------------------------------------------------------------------------------------------------------------
# VENTAS
# ------------------------------------------------------------------------------------------------------------------
class Egreso(models.Model):
    """Venta (egreso) con su fecha, totales y forma de pago."""

    fecha_pedido = models.DateField(null=True, blank=False)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pagado = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    comentarios = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    ticket = models.BooleanField(default=True)
    desglosar = models.BooleanField(default=True)
    # null=True por compatibilidad con filas legadas; auto_now lo rellena al guardar.
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Egreso"
        verbose_name_plural = "Egresos"
        order_with_respect_to = "fecha_pedido"

    def __str__(self):
        return str(self.id)


class ProductosEgreso(models.Model):
    """Línea de producto perteneciente a una venta (Egreso)."""

    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    precio = models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)
    iva = models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)
    created = models.DateTimeField(auto_now_add=True)
    entregado = models.BooleanField(default=True)
    devolucion = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Producto Egreso"
        verbose_name_plural = "Productos Egreso"
        order_with_respect_to = "created"

    def __str__(self):
        return str(self.producto)

    def toJSON(self):
        """Serialización simple de la línea de venta."""
        return model_to_dict(self, exclude=["created"])
