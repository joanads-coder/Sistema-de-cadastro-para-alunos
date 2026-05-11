from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date
from .models import Aluno, Nota, Presenca, Responsavel


class AlunoModelTest(TestCase):
    """Testes para o modelo Aluno"""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='João da Silva',
            matricula='2024001',
            email='joao@example.com',
            data_nascimento=date(2008, 5, 15),
            genero='M',
            serie='6º Ano',
            turma='A'
        )
    
    def test_criar_aluno(self):
        self.assertEqual(self.aluno.nome, 'João da Silva')
        self.assertEqual(self.aluno.matricula, '2024001')
    
    def test_str_aluno(self):
        esperado = f"{self.aluno.nome} - {self.aluno.matricula}"
        self.assertEqual(str(self.aluno), esperado)
    
    def test_status_aprovacao_sem_notas(self):
        self.assertEqual(self.aluno.status_aprovacao, 'Reprovado')
    
    def test_media_geral_sem_notas(self):
        self.assertEqual(self.aluno.media_geral, 0.0)


class NotaModelTest(TestCase):
    """Testes para o modelo Nota"""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='Maria Silva',
            matricula='2024002',
            email='maria@example.com',
            data_nascimento=date(2008, 3, 20),
            genero='F',
            serie='7º Ano',
            turma='B'
        )
        self.nota = Nota.objects.create(
            aluno=self.aluno,
            disciplina='Matemática',
            bimestre=1,
            valor=8.5
        )
    
    def test_criar_nota(self):
        self.assertEqual(self.nota.valor, 8.5)
        self.assertEqual(self.nota.disciplina, 'Matemática')
    
    def test_str_nota(self):
        esperado = f"{self.aluno.nome} - Matemática: 8.5"
        self.assertEqual(str(self.nota), esperado)


class AlunoAPITest(APITestCase):
    """Testes para a API de Alunos"""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='Ana Santos',
            matricula='2024003',
            email='ana@example.com',
            data_nascimento=date(2008, 8, 10),
            genero='F',
            serie='6º Ano',
            turma='C'
        )
    
    def test_listar_alunos(self):
        url = reverse('aluno-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_criar_aluno_via_api(self):
        url = reverse('aluno-list')
        dados = {
            'nome': 'Paulo Costa',
            'matricula': '2024004',
            'email': 'paulo@example.com',
            'data_nascimento': '2008-12-05',
            'genero': 'M',
            'serie': '7º Ano',
            'turma': 'A'
        }
        response = self.client.post(url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Aluno.objects.count(), 2)
    
    def test_obter_aluno_por_id(self):
        url = reverse('aluno-detail', args=[self.aluno.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Ana Santos')
