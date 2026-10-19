# DiFarma — Sistema de Gestión de Farmacia (Python + Django)

Aplicación web de escritorio para la operación de una farmacia: **inventario de
productos, proveedores, control de temperatura de la cadena de frío, punto de
venta (caja) con ticket imprimible y autenticación de usuarios con permisos por
vista**. Interfaz construida sobre AdminLTE + Bootstrap 4.

## Stack

| Componente | Tecnología |
|---|---|
| Backend | Python 3.10+ · Django 4.2 LTS |
| Base de datos | SQLite (desarrollo) — lista para PostgreSQL/MySQL en producción |
| Frontend | Django Templates · AdminLTE · Bootstrap 4 · jQuery · DataTables |
| Formularios | django-widget-tweaks |

## Estructura del proyecto

```
DiFarmaPython-Django/
├── manage.py               # Utilidad de administración de Django
├── requirements.txt        # Dependencias del proyecto
├── .env.example            # Plantilla de variables de entorno
├── DiFarma/                # Configuración del proyecto (settings, urls, wsgi)
└── Bases/                  # App principal
    ├── models.py           # Proveedor, Producto, ControlTemperatura, Egreso, ProductosEgreso
    ├── views.py            # Vistas CRUD + punto de venta + ticket
    ├── forms.py            # Formularios por entidad
    ├── mixins.py           # Protección de sesión y permisos
    ├── migrations/         # Esquema de base de datos versionado
    ├── templates/          # Plantillas (AdminLTE)
    └── static/             # Librerías de frontend (AdminLTE, jQuery, ...)
```

## Instalación y ejecución

```bash
# 1 · Clonar y entrar
git clone https://github.com/AFelipeRD/DiFarmaPython-Django.git
cd DiFarmaPython-Django

# 2 · Entorno virtual + dependencias
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS
pip install -r requirements.txt

# 3 · Base de datos y superusuario
python manage.py migrate
python manage.py createsuperuser

# 4 · Servidor de desarrollo
python manage.py runserver
# → http://127.0.0.1:8000
```

## Variables de entorno

Copia `.env.example` a `.env` y expórtalo antes de ejecutar en producción:

| Variable | Descripción |
|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta (obligatoria en producción) |
| `DJANGO_DEBUG` | `True` solo en desarrollo |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos separados por coma |

Con `DJANGO_DEBUG=False` se activan automáticamente HSTS, cookies seguras y
redirección a HTTPS.

## Seguridad

- La clave secreta y la configuración sensible se leen de variables de entorno.
- Todas las vistas CRUD exigen sesión iniciada **y** permisos específicos
  (`ValidarPermisosMixin` + `ValidarRestriccionesMixin`).
- Los formularios se validan siempre (`form.is_valid()`) antes de tocar la BD.
- Protección CSRF activa en todos los formularios.
- Dependabot vigila las dependencias semanalmente.

## Problemas conocidos

- Las plantillas referencian algunos assets propios (`static/index/*`) que no
  están incluidos en el repositorio (logo, `b4.css`, iconos de editar/eliminar).
  El AdminLTE completo sí está en `Bases/static/lib/adminlite/`.
- El ticket se genera como HTML imprimible (Ctrl+P → PDF). Para PDF directo
  desde el servidor, instala `weasyprint` y descomenta el bloque en `views.py`.

## Licencia

Uso académico/personal — proyecto de portafolio.
