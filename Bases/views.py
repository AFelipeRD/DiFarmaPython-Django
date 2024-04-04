from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .models import Proveedor, Producto, ControlTemperatura
from .forms import AddProveedorForm, EditarProveedorForm, AddProductoForm, EditarProductoForm, AddControlTemperaturaForm, EditarControlTemperaturaForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .mixins import ValidarPermisosMixin, ValidarRestriccionesMixin

import time

from .models import Egreso, Producto, Egreso, ProductosEgreso
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os
#from weasyprint.text.fonts import FontConfiguration

#--------------------------------------------------------------------------------------------------------------

# Create your views here.
# Vistas Principales de la Aplicación
def Principal_view(request):
    return render(request, 'Principal.html')

def Index_view(request):
    return render(request, 'Index.html')

def Base_view(request):
    return render(request, 'Base.html')

#--------------------------------------------------------------------------------------------------------------

# Vistas para el Inicio (Login, LogOut, Register)
# Vista Login
def Login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contraseña = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contraseña)
            if user is not None:
                login(request, user)
                messages.info(request, f"Estas Logeado como {usuario}")
                return redirect("Index")
            else:
                messages.error(request, f"Usuario o Contraseña Incorrecto")
        else:
            messages.error(request, f"Usuario o Contraseña Incorrecto")
    form = AuthenticationForm()
    return render(request, "Login.html", {"form": form})

# Vista LogOut
def LogOut_view(request):
    logout(request)
    messages.info(request, f"Saliste Exitosamente")
    return redirect("Principal")

# Vista Register
def Registro_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            nombre_usuario = form.cleaned_data.get('username')
            messages.success(request, f"Nueva Cuenta Creada: {nombre_usuario}")
            login(request, usuario)
            messages.info(request, f"Por Favor Inicia Sesión: {nombre_usuario}")
            return redirect("Login")
        else:
            if form.error_messages:
                messages.error(request, f"Error")
                messages.info(request, f"Tomar las Indicaciones Dadas")
    form = UserCreationForm
    return render(request, "Registro.html", {"form":form})

#--------------------------------------------------------------------------------------------------------------
    
# Vistas para los Proveedores (View, Add, Change, Delete)
# Vista View Proveedores
class Proveedores_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.view_proveedor')
    def get(self, request):
        Proveedores = Proveedor.objects.all()
        form_personal = AddProveedorForm()
        form_editar = EditarProveedorForm()
        context = {
            'Proveedores': Proveedores,
            'form_personal': form_personal,
            'form_editar': form_editar,
        }
        return render(request, 'Proveedores.html', context)

# Vista Add Proveedores
class Add_Proveedores_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.add_proveedor')
    
    def post(self, request):
        if request.method == "POST":
            form = AddProveedorForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                except:
                    messages(request, "Error al Guardar el Proveedor")
                    return redirect('Proveedores')
        return redirect('Proveedores')

# Vista Edit Proveedores
class Edit_Proveedores_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.change_proveedor')
    def post(self, request):
        if request.method == "POST":
            Proveedores = Proveedor.objects.get(pk=request.POST.get('id_personal_editar'))
            form = EditarProveedorForm(request.POST, request.FILES, instance = Proveedores)
            if form.is_valid:
                form.save()
        return redirect('Proveedores')

# Vista Delete Proveedores
class Delete_Proveedores_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.delete_proveedor')
    def post(self, request):
        if request.method == "POST":
            Proveedores = Proveedor.objects.get(pk=request.POST.get('id_personal_eliminar'))
            Proveedores.delete()
        return redirect('Proveedores')

#--------------------------------------------------------------------------------------------------------------

# Vistas para los Productos (View, Add, Change, Delete)
# Vista View Productos
class Productos_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.view_producto')
    def get(self, request):
        Productos = Producto.objects.all()
        form_producto = AddProductoForm()
        form_editar = EditarProductoForm()
        context = {
            'Productos' : Productos,
            'form_producto': form_producto,
            'form_editar': form_editar,
        }
        return render(request, 'Inventario.html', context)

# Vista Add Productos
class Add_Productos_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.add_producto')
    def post(self, request):
        if request.method == "POST":
            form = AddProductoForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                except:
                    messages(request, "Error al Guardar el Producto")
                    return redirect('Productos')
        return redirect('Productos')

# Vista Edit Productos
class Edit_Productos_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.change_producto')
    def post(self, request):
        if request.method == "POST":
            Productos = Producto.objects.get(pk=request.POST.get('id_producto_editar'))
            form = EditarProductoForm(request.POST, request.FILES, instance = Productos)
            if form.is_valid:
                form.save()
        return redirect('Productos')

# Vista Delete Productos
class Delete_Productos_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.delete_producto')
    def post(self, request):
        if request.method == "POST":
            Productos = Producto.objects.get(pk=request.POST.get('id_producto_eliminar'))
            Productos.delete()
        return redirect('Productos')

#--------------------------------------------------------------------------------------------------------------
    
# Vistas para el ControlTemperaturas (View, Add, Change, Delete)
# Vista View ControlTemperaturas
class ControlTemperaturas_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.view_controltemperatura')
    def get(self, request):
        ControlTemperaturas = ControlTemperatura.objects.all()
        form_controltemperatura = AddControlTemperaturaForm()
        form_editar = EditarControlTemperaturaForm()
        context = {
            'ControlTemperaturas': ControlTemperaturas,
            'form_controltemperatura': form_controltemperatura,
            'form_editar': form_editar,
        }
        return render(request, 'ControlTemperaturas.html', context)

# Vista Add ControlTemperaturas
class Add_ControlTemperaturas_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.add_controltemperatura')
    def post(self, request):
        if request.method == "POST":
            form = AddControlTemperaturaForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                except:
                    messages(request, "Error al Guardar el ControlTemperatura")
                    return redirect('ControlTemperaturas')
        return redirect('ControlTemperaturas')

# Vista Edit ControlTemperaturas
class Edit_ControlTemperaturas_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.change_controltemperatura')
    def post(self, request):
        if request.method == "POST":
            ControlTemperaturas = ControlTemperatura.objects.get(pk=request.POST.get('id_personal_editar'))
            form = EditarControlTemperaturaForm(request.POST, request.FILES, instance = ControlTemperaturas)
            if form.is_valid:
                form.save()
        return redirect('ControlTemperaturas')

# Vista Delete ControlTemperaturas
class Delete_ControlTemperaturas_view(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):
    permission_required = ('Bases.delete_controltemperatura')
    def post(self, request):
        if request.method == "POST":
            ControlTemperaturas = ControlTemperatura.objects.get(pk=request.POST.get('id_personal_eliminar'))
            ControlTemperaturas.delete()
        return redirect('ControlTemperaturas')

#--------------------------------------------------------------------------------------------------------------

# Vistas para las Ventas (Caja, Ticket)
# Vista Environment
class Ventas(ValidarPermisosMixin, ValidarRestriccionesMixin, ListView):

    template_name = 'Ventas.html'
    model = Egreso
    permission_required = ('Bases.view_egreso', 'Bases.add_egreso', 'Bases.delete_egreso', 'Bases.change_egreso')

    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
    """
    def get_queryset(self):
        return ProductosPreventivo.objects.filter(
            preventivo=self.kwargs['id']
        )
    """
    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data,safe=False)

    # Vista Ticket
    def Export_view(request, id, iva):
        #print(id)
        template = get_template("Ticket.html")
        #print(id)
        subtotal = 0 
        iva_suma = 0 

        venta = Egreso.objects.get(pk=float(id))
        datos = ProductosEgreso.objects.filter(egreso=venta)
        for i in datos:
            subtotal = subtotal + float(i.subtotal)
            iva_suma = iva_suma + float(i.iva)

        empresa = "DiFarma de C.V"
        context ={
            'num_ticket': id,
            'iva': iva,
            'fecha': venta.fecha_pedido,
            'items': datos, 
            'total': venta.total, 
            'empresa': empresa,
            'comentarios': venta.comentarios,
            'subtotal': subtotal,
            'iva_suma': iva_suma,
        }
        html_template = template.render(context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; Ticket.pdf"
        css_url = os.path.join(settings.BASE_DIR,'index\static\index\css/bootstrap.min.css')
        #HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])
    
        #font_config = FontConfiguration()
        #HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(target=response, font_config=font_config,stylesheets=[CSS(css_url)])
    
#--------------------------------------------------------------------------------------------------------------
