from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Especialidade(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    DIAS_SEMANA = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=20, unique=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE, related_name='medicos')
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Campos para horário de trabalho
    dias_trabalho = models.CharField(
        max_length=200,
        help_text="Dias da semana que o médico trabalha (separados por vírgula)",
        default="segunda,terca,quarta,quinta,sexta"
    )
    hora_inicio = models.TimeField(
        default="09:00",
        help_text="Horário de início do expediente"
    )
    hora_fim = models.TimeField(
        default="18:00",
        help_text="Horário de fim do expediente"
    )
    
    def __str__(self):
        return f"{self.nome} ({self.especialidade})"
    
    def get_dias_trabalho_display(self):
        """Retorna os dias de trabalho em formato legível"""
        dias_dict = dict(self.DIAS_SEMANA)
        dias_lista = self.dias_trabalho.split(',')
        return ', '.join([dias_dict.get(dia.strip(), dia.strip()) for dia in dias_lista if dia.strip()])
    
    def trabalha_no_dia(self, dia_semana):
        """Verifica se o médico trabalha em um determinado dia da semana"""
        return dia_semana in self.dias_trabalho.split(',')
    
    def esta_disponivel(self, data_hora):
        """Verifica se o médico está disponível em uma data/hora específica"""
        dias_semana_map = {
            0: 'segunda',
            1: 'terca', 
            2: 'quarta',
            3: 'quinta',
            4: 'sexta',
            5: 'sabado',
            6: 'domingo'
        }
        
        dia_semana = dias_semana_map.get(data_hora.weekday())
        if not self.trabalha_no_dia(dia_semana):
            return False
            
        hora = data_hora.time()
        return self.hora_inicio <= hora <= self.hora_fim

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='consultas')
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('agendada', 'Agendada'), ('realizada', 'Realizada'), ('cancelada', 'Cancelada')], default='agendada')
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.paciente} - {self.medico} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
