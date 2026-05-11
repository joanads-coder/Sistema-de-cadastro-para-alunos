from django.contrib import admin
from .models import Aluno, Nota, Presenca, Responsavel


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'serie', 'turma', 'status', 'email')
    list_filter = ('status', 'serie', 'turma', 'data_matricula')
    search_fields = ('nome', 'matricula', 'email', 'cpf')
    readonly_fields = ('data_matricula',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'matricula', 'cpf', 'email', 'data_nascimento', 'genero')
        }),
        ('Informações Acadêmicas', {
            'fields': ('serie', 'turma', 'status', 'data_matricula')
        }),
        ('Informações de Contato', {
            'fields': ('endereco', 'telefone')
        }),
        ('Foto', {
            'fields': ('foto',)
        }),
    )


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'disciplina', 'bimestre', 'valor', 'data_registro')
    list_filter = ('bimestre', 'disciplina', 'data_registro')
    search_fields = ('aluno__nome', 'disciplina')
    readonly_fields = ('data_registro',)
    fieldsets = (
        ('Informações da Nota', {
            'fields': ('aluno', 'disciplina', 'bimestre', 'valor')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Data', {
            'fields': ('data_registro',)
        }),
    )


@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'disciplina', 'data', 'status')
    list_filter = ('status', 'disciplina', 'data')
    search_fields = ('aluno__nome', 'disciplina')
    date_hierarchy = 'data'
    fieldsets = (
        ('Informações de Presença', {
            'fields': ('aluno', 'disciplina', 'data', 'status')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
    )


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'aluno', 'parentesco', 'email', 'telefone', 'ativo')
    list_filter = ('parentesco', 'ativo')
    search_fields = ('nome', 'aluno__nome', 'email', 'cpf')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('aluno', 'nome', 'cpf', 'parentesco')
        }),
        ('Informações de Contato', {
            'fields': ('email', 'telefone', 'telefone_secundario')
        }),
        ('Informações Profissionais', {
            'fields': ('profissao',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )
