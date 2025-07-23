from django import forms
from .models import Especialidade, Medico, Paciente, Consulta

class EspecialidadeForm(forms.ModelForm):
    class Meta:
        model = Especialidade
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da especialidade'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva a especialidade médica (opcional)'
            })
        }

class MedicoForm(forms.ModelForm):
    dias_trabalho = forms.MultipleChoiceField(
        choices=Medico.DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        label="Dias de Trabalho",
        help_text="Selecione os dias da semana em que o médico trabalha"
    )
    
    class Meta:
        model = Medico
        fields = ['nome', 'crm', 'especialidade', 'telefone', 'email', 'dias_trabalho', 'hora_inicio', 'hora_fim']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do médico'
            }),
            'crm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 123456'
            }),
            'especialidade': forms.Select(attrs={
                'class': 'form-select'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'hora_inicio': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'hora_fim': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            })
        }
        labels = {
            'hora_inicio': 'Horário de Início',
            'hora_fim': 'Horário de Fim'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Se estamos editando um médico existente, pré-selecionar os dias
            self.fields['dias_trabalho'].initial = self.instance.dias_trabalho.split(',')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Converter a lista de dias selecionados em string separada por vírgulas
        instance.dias_trabalho = ','.join(self.cleaned_data['dias_trabalho'])
        if commit:
            instance.save()
        return instance

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'cpf', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do paciente'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            })
        }

class ConsultaForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'id_data'
        }),
        label='Data da Consulta',
        help_text='Selecione a data da consulta'
    )
    
    hora = forms.CharField(
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_hora'
        }),
        label='Horário da Consulta',
        help_text='Selecione o horário da consulta'
    )
    
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data', 'hora', 'status', 'observacoes']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'medico': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_medico'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observações sobre a consulta (opcional)'
            })
        }
    
    def _generate_time_slots(self, hora_inicio, hora_fim):
        """Gera slots de horário em intervalos de 45 minutos"""
        from datetime import datetime, timedelta
        
        slots = []
        if hora_inicio and hora_fim:
            # Converter hora_inicio para datetime para facilitar cálculos
            inicio = datetime.combine(datetime.today(), hora_inicio)
            fim = datetime.combine(datetime.today(), hora_fim)
            
            # Gerar slots de 45 minutos
            current_time = inicio
            while current_time < fim:
                time_str = current_time.time().strftime('%H:%M')
                slots.append((time_str, time_str))
                current_time += timedelta(minutes=45)
        
        return slots
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar choices iniciais para o widget Select
        self.fields['hora'].widget.choices = [('', 'Selecione um horário')]
        
        if self.instance.pk and self.instance.data_hora:
            # Se estamos editando uma consulta existente, separar data e hora
            self.fields['data'].initial = self.instance.data_hora.date()
            self.fields['hora'].initial = self.instance.data_hora.time().strftime('%H:%M')
    
    def clean_hora(self):
        """Validação dinâmica do horário baseada no médico selecionado"""
        hora = self.cleaned_data.get('hora')
        medico = self.cleaned_data.get('medico')
        
        if not hora:
            raise forms.ValidationError('Este campo é obrigatório.')
        
        if not medico:
            raise forms.ValidationError('Selecione um médico primeiro.')
        
        # Verificar se o horário está dentro dos horários disponíveis do médico
        if medico.hora_inicio and medico.hora_fim:
            valid_slots = [slot[0] for slot in self._generate_time_slots(medico.hora_inicio, medico.hora_fim)]
            if hora not in valid_slots:
                raise forms.ValidationError(f'Horário inválido. Horários disponíveis: {medico.hora_inicio.strftime("%H:%M")} às {medico.hora_fim.strftime("%H:%M")} em intervalos de 45 minutos.')
        
        return hora
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Combinar data e hora em um único campo datetime
        if self.cleaned_data.get('data') and self.cleaned_data.get('hora'):
            from datetime import datetime, time
            data = self.cleaned_data['data']
            hora_str = self.cleaned_data['hora']
            # Converter string de hora para objeto time
            hora = datetime.strptime(hora_str, '%H:%M').time()
            instance.data_hora = datetime.combine(data, hora)
        
        if commit:
            instance.save()
        return instance
