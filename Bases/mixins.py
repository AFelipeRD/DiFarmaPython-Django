from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

#--------------------------------------------------------------------------------------------------------------

# Validaciones de Seguridad y Permisos
# Validación de Inicio de Sesión
class ValidarPermisosMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('Login')

#--------------------------------------------------------------------------------------------------------------
# Validación de Permisos para realizar Restricciones
class ValidarRestriccionesMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required, str): 
            perms = (self.permission_required,)
        else: 
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('Index')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return HttpResponseRedirect(self.get_url_redirect())       
