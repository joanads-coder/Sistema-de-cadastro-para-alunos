from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Aluno(models.Model):
    """Modelo para representar um aluno"""
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('transferido', 'Transferido'),
    ]
    
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=50, unique=True)
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    serie = models.CharField(max_length=20)  # ex: "6º Ano", "7º Ano"
    turma = models.CharField(max_length=10)  # ex: "A", "B", "C"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    endereco = models.TextField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_matricula = models.DateField(auto_now_add=True)
    foto = models.ImageField(upload_to='alunos/', blank=True, null=True)
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        indexes = [
            models.Index(fields=['matricula']),
            models.Index(fields=['serie', 'turma']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.nome} - {self.matricula}"
    
    @property
    def media_geral(self):
        """Calcula a média geral de notas do aluno"""
        notas = self.notas.all()
        if not notas:
            return 0.0
        media = sum([nota.valor for nota in notas]) / len(notas)
        return round(media, 2)
    
    @property
    def status_aprovacao(self):
        """Define o status de aprovação baseado na média"""
        media = self.media_geral
        if media >= 7.0:
            return 'Aprovado'
        elif media >= 5.0:
            return 'Recuperação'
        else:
            return 'Reprovado'


class Nota(models.Model):
    """Modelo para registrar notas de alunos"""
    
    BIMESTRE_CHOICES = [
        (1, '1º Bimestre'),
        (2, '2º Bimestre'),
        (3, '3º Bimestre'),
        (4, '4º Bimestre'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas')
    disciplina = models.CharField(max_length=100)
    bimestre = models.IntegerField(choices=BIMESTRE_CHOICES)
    valor = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    data_registro = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-data_registro']
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = ['aluno', 'disciplina', 'bimestre']
        indexes = [
            models.Index(fields=['aluno', 'disciplina']),
            models.Index(fields=['bimestre']),
        ]
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina}: {self.valor}"


class Presenca(models.Model):
    """Modelo para registrar presença de alunos"""
    
    STATUS_PRESENCA = [
        ('P', 'Presente'),
        ('A', 'Ausente'),
        ('T', 'Atraso'),
        ('J', 'Justificado'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='presencas')
    disciplina = models.CharField(max_length=100)
    data = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_PRESENCA)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-data']
        verbose_name = 'Presença'
        verbose_name_plural = 'Presenças'
        unique_together = ['aluno', 'disciplina', 'data']
        indexes = [
            models.Index(fields=['aluno', 'disciplina']),
            models.Index(fields=['data']),
        ]
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina} ({self.data}): {self.get_status_display()}"


class Responsavel(models.Model):
    """Modelo para representar responsáveis pelos alunos"""
    
    PARENTESCO_CHOICES = [
        ('pai', 'Pai'),
        ('mae', 'Mãe'),
        ('avo', 'Avó/Avô'),
        ('tio', 'Tio/Tia'),
        ('outro', 'Outro'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='responsaveis')
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11, blank=True)
    parentesco = models.CharField(max_length=20, choices=PARENTESCO_CHOICES)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    telefone_secundario = models.CharField(max_length=20, blank=True)
    profissao = models.CharField(max_length=100, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['aluno', 'parentesco']
        verbose_name = 'Responsável'
        verbose_name_plural = 'Responsáveis'
        indexes = [
            models.Index(fields=['aluno', 'ativo']),
        ]
    
    def __str__(self):
        return f"{self.nome} ({self.get_parentesco_display()}) - {self.aluno.nome}"
