from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Especialidade, Medico, Paciente, Consulta

# Especialidade Views
class EspecialidadeListView(ListView):
    model = Especialidade
    template_name = 'especialidade_list.html'

class EspecialidadeDetailView(DetailView):
    model = Especialidade
    template_name = 'especialidade_detail.html'

class EspecialidadeCreateView(CreateView):
    model = Especialidade
    fields = ['nome', 'descricao']
    template_name = 'especialidade_form.html'
    success_url = reverse_lazy('especialidade_list')

class EspecialidadeUpdateView(UpdateView):
    model = Especialidade
    fields = ['nome', 'descricao']
    template_name = 'especialidade_form.html'
    success_url = reverse_lazy('especialidade_list')

class EspecialidadeDeleteView(DeleteView):
    model = Especialidade
    template_name = 'especialidade_confirm_delete.html'
    success_url = reverse_lazy('especialidade_list')

# Medico Views
class MedicoListView(ListView):
    model = Medico
    template_name = 'medico_list.html'

class MedicoDetailView(DetailView):
    model = Medico
    template_name = 'medico_detail.html'

class MedicoCreateView(CreateView):
    model = Medico
    fields = ['nome', 'crm', 'especialidade', 'telefone', 'email']
    template_name = 'medico_form.html'
    success_url = reverse_lazy('medico_list')

class MedicoUpdateView(UpdateView):
    model = Medico
    fields = ['nome', 'crm', 'especialidade', 'telefone', 'email']
    template_name = 'medico_form.html'
    success_url = reverse_lazy('medico_list')

class MedicoDeleteView(DeleteView):
    model = Medico
    template_name = 'medico_confirm_delete.html'
    success_url = reverse_lazy('medico_list')

# Paciente Views
class PacienteListView(ListView):
    model = Paciente
    template_name = 'paciente_list.html'

class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'paciente_detail.html'

class PacienteCreateView(CreateView):
    model = Paciente
    fields = ['nome', 'data_nascimento', 'cpf', 'telefone', 'email']
    template_name = 'paciente_form.html'
    success_url = reverse_lazy('paciente_list')

class PacienteUpdateView(UpdateView):
    model = Paciente
    fields = ['nome', 'data_nascimento', 'cpf', 'telefone', 'email']
    template_name = 'paciente_form.html'
    success_url = reverse_lazy('paciente_list')

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente_list')

# Consulta Views
class ConsultaListView(ListView):
    model = Consulta
    template_name = 'consulta_list.html'

class ConsultaDetailView(DetailView):
    model = Consulta
    template_name = 'consulta_detail.html'

class ConsultaCreateView(CreateView):
    model = Consulta
    fields = ['paciente', 'medico', 'data_hora', 'status', 'observacoes']
    template_name = 'consulta_form.html'
    success_url = reverse_lazy('consulta_list')

class ConsultaUpdateView(UpdateView):
    model = Consulta
    fields = ['paciente', 'medico', 'data_hora', 'status', 'observacoes']
    template_name = 'consulta_form.html'
    success_url = reverse_lazy('consulta_list')

class ConsultaDeleteView(DeleteView):
    model = Consulta
    template_name = 'consulta_confirm_delete.html'
    success_url = reverse_lazy('consulta_list')
