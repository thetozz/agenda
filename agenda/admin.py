from django.contrib import admin
from .models import Especialidade, Medico, Paciente, Consulta

admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Consulta)

