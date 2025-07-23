from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Especialidade, Medico, Paciente, Consulta
from .forms import ConsultaForm, MedicoForm

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
    form_class = MedicoForm
    template_name = 'medico_form.html'
    success_url = reverse_lazy('medico_list')

class MedicoUpdateView(UpdateView):
    model = Medico
    form_class = MedicoForm
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
    form_class = ConsultaForm
    template_name = 'consulta_form.html'
    success_url = reverse_lazy('consulta_list')

class ConsultaUpdateView(UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'consulta_form.html'
    success_url = reverse_lazy('consulta_list')

class ConsultaDeleteView(DeleteView):
    model = Consulta
    template_name = 'consulta_confirm_delete.html'
    success_url = reverse_lazy('consulta_list')


@require_http_methods(["GET"])
def get_medico_availability(request, medico_id):
    """API endpoint para obter os dias de trabalho e horários disponíveis de um médico"""
    try:
        from datetime import datetime, timedelta
        from django.utils import timezone
        import pytz
        
        medico = get_object_or_404(Medico, id=medico_id)
        
        # Obter data selecionada do parâmetro de consulta (se fornecida)
        data_selecionada = request.GET.get('data')
        consulta_id = request.GET.get('consulta_id')  # Para edição de consulta existente
        
        # Mapear dias da semana para números (0=domingo, 1=segunda, etc.)
        dias_semana_map = {
            'domingo': 6,
            'segunda': 0,
            'terca': 1,
            'quarta': 2,
            'quinta': 3,
            'sexta': 4,
            'sabado': 5
        }
        
        dias_trabalho = medico.dias_trabalho.split(',')
        dias_disponiveis = [dias_semana_map.get(dia.strip()) for dia in dias_trabalho if dia.strip() in dias_semana_map]
        
        # Gerar horários disponíveis em intervalos de 45 minutos
        horarios_disponiveis = []
        if medico.hora_inicio and medico.hora_fim:
            # Converter hora_inicio para datetime para facilitar cálculos
            inicio = datetime.combine(datetime.today(), medico.hora_inicio)
            fim = datetime.combine(datetime.today(), medico.hora_fim)
            
            # Gerar todos os slots de 45 minutos
            all_slots = []
            current_time = inicio
            while current_time < fim:
                all_slots.append(current_time.time().strftime('%H:%M'))
                current_time += timedelta(minutes=45)
            
            # Se uma data foi fornecida, verificar consultas já agendadas
            horarios_ocupados = set()
            if data_selecionada:
                try:
                    data_obj = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
                    
                    # Obter timezone local do Brasil
                    local_tz = pytz.timezone('America/Sao_Paulo')
                    
                    # Buscar consultas já agendadas para este médico nesta data
                    # Filtrar apenas consultas ativas (não canceladas)
                    consultas_existentes = Consulta.objects.filter(
                        medico=medico,
                        data_hora__date=data_obj,
                        status__in=['agendada', 'realizada']  # Excluir consultas canceladas
                    )
                    
                    # Se estivermos editando uma consulta, excluir ela da verificação
                    if consulta_id:
                        try:
                            consultas_existentes = consultas_existentes.exclude(id=int(consulta_id))
                        except (ValueError, TypeError):
                            pass
                    
                    # Coletar horários já ocupados
                    for consulta in consultas_existentes:
                        # Converter para timezone local antes de extrair o horário
                        if timezone.is_aware(consulta.data_hora):
                            # Se o datetime é timezone-aware, converter para local
                            data_hora_local = consulta.data_hora.astimezone(local_tz)
                        else:
                            # Se não é timezone-aware, tornar timezone-aware primeiro
                            data_hora_naive = timezone.make_aware(consulta.data_hora, local_tz)
                            data_hora_local = data_hora_naive.astimezone(local_tz)
                        
                        horario_consulta = data_hora_local.time().strftime('%H:%M')
                        horarios_ocupados.add(horario_consulta)
                        
                        # Debug: adicionar log para verificar horários ocupados
                        print(f"Horário ocupado encontrado: {horario_consulta} para consulta ID {consulta.id}")
                        print(f"  - Original: {consulta.data_hora} (aware: {timezone.is_aware(consulta.data_hora)})")
                        print(f"  - Local: {data_hora_local}")
                        
                except ValueError:
                    # Data inválida, ignorar filtragem
                    pass
            
            # Filtrar horários disponíveis (remover os ocupados)
            for slot in all_slots:
                if slot not in horarios_ocupados:
                    horarios_disponiveis.append({
                        'value': slot,
                        'display': slot
                    })
            
            # Debug: log dos horários disponíveis após filtragem
            print(f"Horários ocupados: {horarios_ocupados}")
            print(f"Horários disponíveis após filtragem: {[h['value'] for h in horarios_disponiveis]}")
        
        return JsonResponse({
            'success': True,
            'dias_disponiveis': dias_disponiveis,
            'hora_inicio': medico.hora_inicio.strftime('%H:%M'),
            'hora_fim': medico.hora_fim.strftime('%H:%M'),
            'horarios_disponiveis': horarios_disponiveis,
            'dias_trabalho_display': medico.get_dias_trabalho_display()
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
