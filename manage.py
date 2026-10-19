#!/usr/bin/env python
"""Utilidad de línea de comandos de Django para tareas administrativas.

Uso:
    python manage.py makemigrations Bases   # genera migraciones
    python manage.py migrate                # aplica migraciones a la BD
    python manage.py createsuperuser        # crea el usuario administrador
    python manage.py runserver              # servidor de desarrollo
"""
import os
import sys


def main():
    """Punto de entrada estándar de Django 4.x."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DiFarma.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado y disponible en la "
            "variable de entorno PYTHONPATH? ¿Olvidaste activar el entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
