"""Rutas de la aplicación Bases.

Convención: los CRUD usan vistas de clase protegidas por los mixins de
permisos; el punto de venta expone dos rutas de exportación de ticket.
"""
from django.urls import path

from . import views

urlpatterns = [
    # Vistas principales
    path("", views.Principal_view, name="Principal"),
    path("Index/", views.Index_view, name="Index"),
    path("Base/", views.Base_view, name="Base"),

    # Autenticación
    path("login/", views.Login_view, name="Login"),
    path("logout/", views.LogOut_view, name="Logout"),
    path("Registro/", views.Registro_view, name="Registro"),

    # Proveedores (CRUD)
    path("Proveedores/", views.Proveedores_view.as_view(), name="Proveedores"),
    path("Add_Proveedores/", views.Add_Proveedores_view.as_view(), name="AddProveedores"),
    path("Edit_Proveedores/", views.Edit_Proveedores_view.as_view(), name="EditProveedores"),
    path("Delete_Proveedores/", views.Delete_Proveedores_view.as_view(), name="DeleteProveedores"),

    # Productos / Inventario (CRUD)
    path("Productos/", views.Productos_view.as_view(), name="Productos"),
    path("Add_Productos/", views.Add_Productos_view.as_view(), name="AddProductos"),
    path("Edit_Productos/", views.Edit_Productos_view.as_view(), name="EditProductos"),
    path("Delete_Productos/", views.Delete_Productos_view.as_view(), name="DeleteProductos"),

    # Control de temperaturas (CRUD)
    path("ControlTemperaturas/", views.ControlTemperaturas_view.as_view(), name="ControlTemperaturas"),
    path("Add_ControlTemperaturas/", views.Add_ControlTemperaturas_view.as_view(), name="AddControlTemperaturas"),
    path("Edit_ControlTemperaturas/", views.Edit_ControlTemperaturas_view.as_view(), name="EditControlTemperaturas"),
    path("Delete_ControlTemperaturas/", views.Delete_ControlTemperaturas_view.as_view(), name="DeleteControlTemperaturas"),

    # Ventas (caja) y ticket
    path("Ventas/", views.Ventas.as_view(), name="Ventas"),
    # Base para el ticket: el frontend concatena <id>/<iva> manualmente.
    path("Export/", views.Ventas.Export_view, name="ExportPDF"),
    path("Export/<int:id>/<str:iva>", views.Ventas.Export_view, name="ExportTicket"),
]
