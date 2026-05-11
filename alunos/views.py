from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Q, Count
from .models import Aluno, Nota, Presenca, Responsavel
from .serializers import (
    AlunoListSerializer, AlunoDetailSerializer, AlunoCreateSerializer,
    NotaSerializer, PresencaSerializer, ResponsavelSerializer
)


class AlunoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Alunos"""
    
    queryset = Aluno.objects.prefetch_related('notas', 'presencas', 'responsaveis')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['serie', 'turma', 'status']
    search_fields = ['nome', 'matricula', 'email']
    ordering_fields = ['nome', 'serie', 'data_matricula']
    ordering = ['nome']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AlunoDetailSerializer
        elif self.action == 'create':
            return AlunoCreateSerializer
        elif self.action == 'list':
            return AlunoListSerializer
        return AlunoDetailSerializer
    
    @action(detail=True, methods=['get'])
    def media_disciplinas(self, request, pk=None):
        """Retorna a média do aluno por disciplina"""
        aluno = self.get_object()
        notas = aluno.notas.all()
        
        disciplinas_media = {}
        for nota in notas:
            if nota.disciplina not in disciplinas_media:
                disciplinas_media[nota.disciplina] = []
            disciplinas_media[nota.disciplina].append(nota.valor)
        
        resultado = {
            aluno.nome: {
                disciplina: round(sum(valores) / len(valores), 2)
                for disciplina, valores in disciplinas_media.items()
            }
        }
        
        return Response(resultado)
    
    @action(detail=True, methods=['get'])
    def presenca_resumo(self, request, pk=None):
        """Retorna um resumo de presença do aluno"""
        aluno = self.get_object()
        presencas = aluno.presencas.all()
        
        total = presencas.count()
        if total == 0:
            return Response({'aluno': aluno.nome, 'mensagem': 'Sem registros de presença'})
        
        presente = presencas.filter(status='P').count()
        ausente = presencas.filter(status='A').count()
        atraso = presencas.filter(status='T').count()
        justificado = presencas.filter(status='J').count()
        
        percentual_presenca = round((presente / total) * 100, 2)
        
        return Response({
            'aluno': aluno.nome,
            'total_registros': total,
            'presente': presente,
            'ausente': ausente,
            'atraso': atraso,
            'justificado': justificado,
            'percentual_presenca': percentual_presenca
        })
    
    @action(detail=True, methods=['get'])
    def relatorio(self, request, pk=None):
        """Retorna um relatório completo do aluno"""
        aluno = self.get_object()
        serializer = AlunoDetailSerializer(aluno)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_serie(self, request):
        """Retorna alunos filtrados por série"""
        serie = request.query_params.get('serie')
        if not serie:
            return Response(
                {'erro': 'Parâmetro "serie" é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        alunos = Aluno.objects.filter(serie=serie)
        serializer = AlunoListSerializer(alunos, many=True)
        return Response({
            'serie': serie,
            'total': alunos.count(),
            'alunos': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas gerais dos alunos"""
        total_alunos = Aluno.objects.count()
        alunos_ativos = Aluno.objects.filter(status='ativo').count()
        
        # Alunos por série
        alunos_por_serie = Aluno.objects.values('serie').annotate(
            total=Count('id')
        ).order_by('serie')
        
        # Média geral de notas
        media_geral = Nota.objects.aggregate(media=Avg('valor'))['media'] or 0
        
        # Alunos aprovados/reprovados (baseado em média >= 7)
        aprovados = Aluno.objects.annotate(
            media=Avg('notas__valor')
        ).filter(media__gte=7.0).count()
        
        return Response({
            'total_alunos': total_alunos,
            'alunos_ativos': alunos_ativos,
            'media_geral': round(media_geral, 2),
            'alunos_aprovados': aprovados,
            'alunos_por_serie': list(alunos_por_serie)
        })


class NotaViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Notas"""
    
    queryset = Nota.objects.select_related('aluno')
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aluno', 'disciplina', 'bimestre']
    search_fields = ['aluno__nome', 'disciplina']
    ordering_fields = ['valor', 'data_registro']
    ordering = ['-data_registro']
    
    @action(detail=False, methods=['get'])
    def por_disciplina(self, request):
        """Retorna notas agrupadas por disciplina"""
        disciplina = request.query_params.get('disciplina')
        if not disciplina:
            return Response(
                {'erro': 'Parâmetro "disciplina" é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        notas = Nota.objects.filter(disciplina=disciplina)
        media = notas.aggregate(media=Avg('valor'))['media'] or 0
        serializer = NotaSerializer(notas, many=True)
        
        return Response({
            'disciplina': disciplina,
            'media': round(media, 2),
            'total_notas': notas.count(),
            'notas': serializer.data
        })


class PresencaViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Presenças"""
    
    queryset = Presenca.objects.select_related('aluno')
    serializer_class = PresencaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aluno', 'disciplina', 'status']
    search_fields = ['aluno__nome', 'disciplina']
    ordering_fields = ['data']
    ordering = ['-data']


class ResponsavelViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Responsáveis"""
    
    queryset = Responsavel.objects.select_related('aluno')
    serializer_class = ResponsavelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aluno', 'parentesco', 'ativo']
    search_fields = ['nome', 'aluno__nome', 'email']
    ordering_fields = ['aluno', 'parentesco']
    ordering = ['aluno', 'parentesco']
