from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet, NotaViewSet, PresencaViewSet, ResponsavelViewSet

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'notas', NotaViewSet, basename='nota')
router.register(r'presencas', PresencaViewSet, basename='presenca')
router.register(r'responsaveis', ResponsavelViewSet, basename='responsavel')

urlpatterns = [
    path('', include(router.urls)),
]
