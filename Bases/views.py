"""Vistas de la aplicación Bases (DiFarma).

Reglas de esta refactorización:
- TODO formulario se valida con form.is_valid() (con paréntesis); sin excepción.
- Los mensajes de usuario usan messages.success/error (el módulo no se invoca).
- Los borrados y ediciones usan get_object_or_404: nunca un 500 por un id inexistente.
- El punto de venta (Ventas) implementa los dos endpoints que el frontend espera:
  'autocomplete' (buscar productos) y 'save' (registrar la venta en una transacción).
"""
import json
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.utils import timezone
from django.views.generic import ListView

from .forms import (
    AddControlTemperaturaForm,
    AddProductoForm,
    AddProveedorForm,
    EditarControlTemperaturaForm,
    EditarProductoForm,
    EditarProveedorForm,
)
from .mixins import ValidarPermisosMixin, ValidarRestriccionesMixin
from .models import ControlTemperatura, Egreso, Producto, ProductosEgreso, Proveedor

# Tasa de IVA aplicada a las ventas (Colombia, 19 %). Ajustar si cambia la norma.
TASA_IVA = Decimal("0.19")


# ------------------------------------------------------------------------------------------------------------------
# VISTAS PRINCIPALES
# ------------------------------------------------------------------------------------------------------------------
def Principal_view(request):
    """Página pública de entrada (landing)."""
    return render(request, "Principal.html")


@login_required(login_url="Login")
def Index_view(request):
    """Panel principal; requiere sesión iniciada."""
    return render(request, "Index.html")


def Base_view(request):
    """Plantilla base de maquetación (solo referencia de desarrollo)."""
    return render(request, "Base.html")


# ------------------------------------------------------------------------------------------------------------------
# INICIO DE SESIÓN: LOGIN / LOGOUT / REGISTRO
# ------------------------------------------------------------------------------------------------------------------
def Login_view(request):
    """Autenticación con el formulario estándar de Django."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            contraseña = form.cleaned_data.get("password")
            user = authenticate(username=usuario, password=contraseña)
            if user is not None:
                login(request, user)
                messages.success(request, f"Estás logeado como {usuario}")
                return redirect("Index")
        messages.error(request, "Usuario o contraseña incorrectos")
    form = AuthenticationForm()
    return render(request, "Login.html", {"form": form})


def LogOut_view(request):
    """Cierra la sesión y regresa a la landing."""
    logout(request)
    messages.info(request, "Saliste exitosamente")
    return redirect("Principal")


def Registro_view(request):
    """Crea la cuenta, inicia sesión y lleva al panel (flujo coherente)."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"Nueva cuenta creada: {usuario.username}")
            return redirect("Index")
        messages.error(request, "Revisa las indicaciones del formulario")
    else:
        form = UserCreationForm()  # Instancia, no la clase
    return render(request, "Registro.html", {"form": form})


# ------------------------------------------------------------------------------------------------------------------
# PROVEEDORES (View, Add, Edit, Delete)
# ------------------------------------------------------------------------------------------------------------------
class Proveedores_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Listado de proveedores con formularios modales de alta y edición."""

    permission_required = ("Bases.view_proveedor",)

    def get(self, request):
        contexto = {
            "Proveedores": Proveedor.objects.all(),
            "form_personal": AddProveedorForm(),
            "form_editar": EditarProveedorForm(),
        }
        return render(request, "Proveedores.html", contexto)


class Add_Proveedores_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Alta de proveedores; la validación del formulario es obligatoria."""

    permission_required = ("Bases.add_proveedor",)

    def post(self, request):
        form = AddProveedorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor guardado correctamente")
        else:
            messages.error(request, "Error al guardar el proveedor: revisa los campos")
        return redirect("Proveedores")


class Edit_Proveedores_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Edición de proveedores por id oculto del modal."""

    permission_required = ("Bases.change_proveedor",)

    def post(self, request):
        proveedor = get_object_or_404(Proveedor, pk=request.POST.get("id_personal_editar"))
        form = EditarProveedorForm(request.POST, request.FILES, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado")
        else:
            messages.error(request, "Error al editar: revisa los campos")
        return redirect("Proveedores")


class Delete_Proveedores_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Eliminación de proveedores por id oculto del modal."""

    permission_required = ("Bases.delete_proveedor",)

    def post(self, request):
        proveedor = get_object_or_404(Proveedor, pk=request.POST.get("id_personal_eliminar"))
        proveedor.delete()
        messages.success(request, "Proveedor eliminado")
        return redirect("Proveedores")


# ------------------------------------------------------------------------------------------------------------------
# PRODUCTOS (View, Add, Edit, Delete)
# ------------------------------------------------------------------------------------------------------------------
class Productos_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Inventario de productos con formularios modales."""

    permission_required = ("Bases.view_producto",)

    def get(self, request):
        contexto = {
            "Productos": Producto.objects.all(),
            "form_producto": AddProductoForm(),
            "form_editar": EditarProductoForm(),
        }
        return render(request, "Inventario.html", contexto)


class Add_Productos_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Alta de productos; validación obligatoria."""

    permission_required = ("Bases.add_producto",)

    def post(self, request):
        form = AddProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto guardado correctamente")
        else:
            messages.error(request, "Error al guardar el producto: revisa los campos")
        return redirect("Productos")


class Edit_Productos_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Edición de productos por id oculto del modal."""

    permission_required = ("Bases.change_producto",)

    def post(self, request):
        producto = get_object_or_404(Producto, pk=request.POST.get("id_producto_editar"))
        form = EditarProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado")
        else:
            messages.error(request, "Error al editar: revisa los campos")
        return redirect("Productos")


class Delete_Productos_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Eliminación de productos por id oculto del modal."""

    permission_required = ("Bases.delete_producto",)

    def post(self, request):
        producto = get_object_or_404(Producto, pk=request.POST.get("id_producto_eliminar"))
        producto.delete()
        messages.success(request, "Producto eliminado")
        return redirect("Productos")


# ------------------------------------------------------------------------------------------------------------------
# CONTROL DE TEMPERATURAS (View, Add, Edit, Delete)
# ------------------------------------------------------------------------------------------------------------------
class ControlTemperaturas_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Registros de cadena de frío con formularios modales."""

    permission_required = ("Bases.view_controltemperatura",)

    def get(self, request):
        contexto = {
            "ControlTemperaturas": ControlTemperatura.objects.all(),
            "form_controltemperatura": AddControlTemperaturaForm(),
            "form_editar": EditarControlTemperaturaForm(),
        }
        return render(request, "ControlTemperaturas.html", contexto)


class Add_ControlTemperaturas_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Alta de registros de temperatura; validación obligatoria."""

    permission_required = ("Bases.add_controltemperatura",)

    def post(self, request):
        form = AddControlTemperaturaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro guardado correctamente")
        else:
            messages.error(request, "Error al guardar el registro: revisa los campos")
        return redirect("ControlTemperaturas")


class Edit_ControlTemperaturas_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Edición de registros por id propio (id_control_editar)."""

    permission_required = ("Bases.change_controltemperatura",)

    def post(self, request):
        registro = get_object_or_404(ControlTemperatura, pk=request.POST.get("id_control_editar"))
        form = EditarControlTemperaturaForm(request.POST, request.FILES, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro actualizado")
        else:
            messages.error(request, "Error al editar: revisa los campos")
        return redirect("ControlTemperaturas")


class Delete_ControlTemperaturas_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Eliminación de registros por id propio (id_control_eliminar)."""

    permission_required = ("Bases.delete_controltemperatura",)

    def post(self, request):
        registro = get_object_or_404(ControlTemperatura, pk=request.POST.get("id_control_eliminar"))
        registro.delete()
        messages.success(request, "Registro eliminado")
        return redirect("ControlTemperaturas")


# ------------------------------------------------------------------------------------------------------------------
# VENTAS (CAJA): autocompletado, guardado y ticket
# ------------------------------------------------------------------------------------------------------------------
class Ventas(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    """Punto de venta: búsqueda de productos, carrito y registro de la venta."""

    template_name = "Ventas.html"
    model = Egreso
    permission_required = (
        "Bases.view_egreso",
        "Bases.add_egreso",
        "Bases.delete_egreso",
        "Bases.change_egreso",
    )

    def get_context_data(self, **kwargs):
        """Añade al contexto la lista de productos y la fecha de hoy ({{HOY}})."""
        contexto = super().get_context_data(**kwargs)
        contexto["productos_lista"] = Producto.objects.all()
        contexto["HOY"] = timezone.localdate()
        contexto["moneda"] = "$"
        return contexto

    def post(self, request, *args, **kwargs):
        """Endpoint AJAX del punto de venta: 'autocomplete' y 'save'."""
        data = {}
        try:
            action = request.POST["action"]
            if action == "autocomplete":
                data = []
                termino = request.POST.get("term", "")
                for producto in Producto.objects.filter(nombre__icontains=termino)[:10]:
                    item = producto.toJSON()
                    # El frontend espera «descripcion»; el modelo usa «nombre».
                    item["descripcion"] = producto.nombre
                    item["value"] = producto.nombre
                    data.append(item)
            elif action == "save":
                data = self._guardar_venta(request)
            else:
                data = {"error": "Acción no soportada"}
        except Exception as exc:  # El frontend muestra el error con Swal
            data = {"error": str(exc)}
        return JsonResponse(data, safe=False)

    @staticmethod
    def _decimal(valor, defecto="0"):
        """Convierte a Decimal de forma segura (carrito y pagos vienen como texto)."""
        try:
            return Decimal(str(valor))
        except (InvalidOperation, TypeError):
            return Decimal(defecto)

    def _guardar_venta(self, request):
        """Crea el Egreso y sus ProductosEgreso dentro de una transacción atómica."""
        carrito = json.loads(request.POST.get("verts", "{}"))
        productos = carrito.get("products", carrito) if isinstance(carrito, dict) else carrito
        if not productos:
            raise ValueError("El carrito está vacío")

        with transaction.atomic():
            egreso = Egreso.objects.create(
                fecha_pedido=request.POST.get("fecha") or timezone.localdate(),
                comentarios=request.POST.get("comentarios", ""),
                ticket=request.POST.get("ticket", "").lower() in ("1", "si", "sí", "true"),
                desglosar=request.POST.get("desglosar", "0") == "1",
            )
            total_venta = Decimal("0")
            for linea in productos:
                producto = Producto.objects.get(pk=linea["id"])
                cantidad = self._decimal(linea.get("cantidad", 1))
                precio = self._decimal(linea.get("precio", 0))
                subtotal = (cantidad * precio).quantize(Decimal("0.01"))
                iva = (subtotal * TASA_IVA).quantize(Decimal("0.01"))
                total = subtotal + iva
                ProductosEgreso.objects.create(
                    egreso=egreso,
                    producto=producto,
                    cantidad=cantidad,
                    precio=precio,
                    subtotal=subtotal,
                    iva=iva,
                    total=total,
                )
                total_venta += total
            pagado = sum(
                (self._decimal(request.POST.get(medio, "0"))
                 for medio in ("efectivo", "tarjeta", "transferencia", "vales", "otro")),
                Decimal("0"),
            )
            egreso.total = total_venta
            egreso.pagado = pagado
            egreso.save()

        # Contrato con el frontend: [id_egreso, éxito, desglosar_iva]
        return [egreso.id, True, "true" if egreso.desglosar else "false"]

    @staticmethod
    def Export_view(request, id=None, iva="false"):
        """Genera el ticket de la venta como HTML imprimible (Ctrl+P → PDF).

        Nota: si se desea PDF directo del servidor, instala weasyprint y
        descomenta el bloque correspondiente; por ahora se evita esa
        dependencia pesada y se imprime desde el navegador.
        """
        if id is None:
            return redirect("Ventas")
        venta = get_object_or_404(Egreso, pk=id)
        datos = ProductosEgreso.objects.filter(egreso=venta)
        subtotal = sum((linea.subtotal for linea in datos), Decimal("0"))
        iva_suma = sum((linea.iva for linea in datos), Decimal("0"))
        contexto = {
            "num_ticket": venta.id,
            "iva": iva,
            "fecha": venta.fecha_pedido,
            "items": datos,
            "total": venta.total,
            "comentarios": venta.comentarios,
            "subtotal": subtotal,
            "iva_suma": iva_suma,
            "empresa": {
                "nombre": "DiFarma de C.V.",
                "domicilio": "Calle 123 #45-67, Bogotá D.C.",
                "telefono": "+57 601 000 0000",
                "moneda": "$",
                "imagen": None,  # Sin logo por ahora; la plantilla lo omite
            },
        }
        html = get_template("Ticket.html").render(contexto)
        respuesta = HttpResponse(html)
        respuesta["Content-Disposition"] = f'inline; filename="ticket_{venta.id}.html"'
        return respuesta
