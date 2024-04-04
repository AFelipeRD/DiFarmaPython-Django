from django.urls import path
from . import views

# URLs de Todas las Actividades Diseñadas.

urlpatterns = [

    # URL de las Vistas Principales
    path('', views.Principal_view, name='Principal'),
    path('Index/', views.Index_view, name='Index'),
    path('Base/', views.Base_view, name='Base'),

    # URL Actividades de Inicio
    path('logout/', views.LogOut_view, name='Logout'),
    path('login/', views.Login_view, name='Login'),
    path('Registro/', views.Registro_view, name='Registro'), 

    # URL Actividades de Proveedores
    path('Proveedores/', views.Proveedores_view.as_view(), name='Proveedores'),
    path('Add_Proveedores/', views.Add_Proveedores_view.as_view(), name='AddProveedores'),
    path('Edit_Proveedores/', views.Edit_Proveedores_view.as_view(), name='EditProveedores'),
    path('Delete_Proveedores/', views.Delete_Proveedores_view.as_view(), name='DeleteProveedores'),

    # URL Actividades de Productos
    path('Productos/', views.Productos_view.as_view(), name='Productos'),
    path('Add_Productos/', views.Add_Productos_view.as_view(), name='AddProductos'),
    path('Edit_Productos/', views.Edit_Productos_view.as_view(), name='EditProductos'),
    path('Delete_Productos/', views.Delete_Productos_view.as_view(), name='DeleteProductos'),

    # URL Actividades de ControlTemperaturas
    path('ControlTemperaturas/', views.ControlTemperaturas_view.as_view(), name='ControlTemperaturas'),
    path('Add_ControlTemperaturas/', views.Add_ControlTemperaturas_view.as_view(), name='AddControlTemperaturas'),
    path('Edit_ControlTemperaturas/', views.Edit_ControlTemperaturas_view.as_view(), name='EditControlTemperaturas'),
    path('Delete_ControlTemperaturas/', views.Delete_ControlTemperaturas_view.as_view(), name='DeleteControlTemperaturas'),

    # URL Actividades de Ventas
    path('Ventas/', views.Ventas.as_view(), name='Ventas'),
    path('Export/', views.Ventas.Export_view, name="ExportPDF" ),
    path('Export/<id>/<iva>', views.Ventas.Export_view, name="ExportPDF" ),    
    
]


