from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Aluno, Nota, Presenca, Responsavel


class ResponsavelSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Responsavel"""
    
    class Meta:
        model = Responsavel
        fields = [
            'id', 'aluno', 'nome', 'cpf', 'parentesco', 'email', 
            'telefone', 'telefone_secundario', 'profissao', 'ativo'
        ]
        read_only_fields = ['id']


class NotaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Nota"""
    
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    bimestre_display = serializers.CharField(source='get_bimestre_display', read_only=True)
    
    class Meta:
        model = Nota
        fields = [
            'id', 'aluno', 'aluno_nome', 'disciplina', 'bimestre', 
            'bimestre_display', 'valor', 'data_registro', 'observacoes'
        ]
        read_only_fields = ['id', 'data_registro']
    
    def validate_valor(self, value):
        if not 0.0 <= value <= 10.0:
            raise serializers.ValidationError("A nota deve estar entre 0 e 10.")
        return value


class PresencaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Presenca"""
    
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Presenca
        fields = [
            'id', 'aluno', 'aluno_nome', 'disciplina', 'data', 
            'status', 'status_display', 'observacoes'
        ]
        read_only_fields = ['id']


class AlunoListSerializer(serializers.ModelSerializer):
    """Serializer para listar alunos (informações básicas)"""
    
    media_geral = serializers.SerializerMethodField()
    status_aprovacao = serializers.SerializerMethodField()
    
    class Meta:
        model = Aluno
        fields = [
            'id', 'nome', 'matricula', 'email', 'serie', 'turma', 
            'status', 'media_geral', 'status_aprovacao', 'data_matricula'
        ]
    
    def get_media_geral(self, obj):
        return obj.media_geral
    
    def get_status_aprovacao(self, obj):
        return obj.status_aprovacao


class AlunoDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalhes completos do aluno"""
    
    notas = NotaSerializer(many=True, read_only=True)
    presencas = PresencaSerializer(many=True, read_only=True)
    responsaveis = ResponsavelSerializer(many=True, read_only=True)
    media_geral = serializers.SerializerMethodField()
    status_aprovacao = serializers.SerializerMethodField()
    
    class Meta:
        model = Aluno
        fields = [
            'id', 'nome', 'matricula', 'cpf', 'email', 'data_nascimento',
            'genero', 'serie', 'turma', 'status', 'endereco', 'telefone',
            'data_matricula', 'foto', 'media_geral', 'status_aprovacao',
            'notas', 'presencas', 'responsaveis'
        ]
        read_only_fields = ['id', 'data_matricula']
    
    def validate_cpf(self, value):
        if value and Aluno.objects.filter(cpf=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Este CPF já está cadastrado.")
        return value
    
    def get_media_geral(self, obj):
        return obj.media_geral
    
    def get_status_aprovacao(self, obj):
        return obj.status_aprovacao


class AlunoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar um novo aluno"""
    
    class Meta:
        model = Aluno
        fields = [
            'nome', 'matricula', 'cpf', 'email', 'data_nascimento',
            'genero', 'serie', 'turma', 'status', 'endereco', 'telefone', 'foto'
        ]
    
    def validate_email(self, value):
        if Aluno.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está cadastrado.")
        return value
    
    def validate_matricula(self, value):
        if Aluno.objects.filter(matricula=value).exists():
            raise serializers.ValidationError("Esta matrícula já existe.")
        return value
