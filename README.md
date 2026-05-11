# Sistema de Cadastro para Alunos 📚

Um sistema completo de gerenciamento de alunos desenvolvido com **Django** e **Django REST Framework**, permitindo cadastro, monitoramento de notas, presença e informações de responsáveis.

## 📋 Funcionalidades

### 👤 Gerenciamento de Alunos
- ✅ Cadastro completo de alunos (dados pessoais e acadêmicos)
- ✅ Atualização e exclusão de registros
- ✅ Filtros por série, turma e status
- ✅ Busca por nome, matrícula ou email

### 📊 Notas e Desempenho
- ✅ Registro de notas por disciplina e bimestre
- ✅ Cálculo automático de médias
- ✅ Relatório de desempenho por aluno
- ✅ Análise de desempenho por disciplina

### ✋ Controle de Presença
- ✅ Registro de presença (presente, ausente, atraso, justificado)
- ✅ Resumo de presença com percentual
- ✅ Filtros por data e disciplina

### 👨‍👩‍👧 Responsáveis
- ✅ Cadastro de responsáveis por aluno
- ✅ Diferentes graus de parentesco
- ✅ Informações de contato

### 📈 Estatísticas
- ✅ Dashboard com estatísticas gerais
- ✅ Alunos por série
- ✅ Média geral de notas
- ✅ Taxa de presença

## 🚀 Instalação

### Pré-requisitos
- Python 3.11+
- pip ou conda
- PostgreSQL (opcional, pode usar SQLite)

### Passos de Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/joanads-coder/Sistema-de-cadastro-para-alunos.git
cd Sistema-de-cadastro-para-alunos
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv

# Ative o ambiente (Windows)
venv\Scripts\activate

# Ative o ambiente (macOS/Linux)
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Crie um superusuário (admin)**
```bash
python manage.py createsuperuser
```

7. **Inicie o servidor**
```bash
python manage.py runserver
```

A aplicação estará disponível em: `http://127.0.0.1:8000`

## 📱 API Endpoints

### Alunos
- `GET /api/alunos/` - Listar todos os alunos
- `POST /api/alunos/` - Criar novo aluno
- `GET /api/alunos/{id}/` - Obter detalhes do aluno
- `PUT /api/alunos/{id}/` - Atualizar aluno
- `DELETE /api/alunos/{id}/` - Deletar aluno
- `GET /api/alunos/{id}/media_disciplinas/` - Média por disciplina
- `GET /api/alunos/{id}/presenca_resumo/` - Resumo de presença
- `GET /api/alunos/{id}/relatorio/` - Relatório completo
- `GET /api/alunos/por_serie/?serie=6º%20Ano` - Alunos por série
- `GET /api/alunos/estatisticas/` - Estatísticas gerais

### Notas
- `GET /api/notas/` - Listar notas
- `POST /api/notas/` - Criar nota
- `GET /api/notas/{id}/` - Detalhes da nota
- `PUT /api/notas/{id}/` - Atualizar nota
- `DELETE /api/notas/{id}/` - Deletar nota

### Presença
- `GET /api/presencas/` - Listar presenças
- `POST /api/presencas/` - Registrar presença
- `GET /api/presencas/{id}/` - Detalhes da presença
- `PUT /api/presencas/{id}/` - Atualizar presença
- `DELETE /api/presencas/{id}/` - Deletar presença

### Responsáveis
- `GET /api/responsaveis/` - Listar responsáveis
- `POST /api/responsaveis/` - Criar responsável
- `GET /api/responsaveis/{id}/` - Detalhes do responsável
- `PUT /api/responsaveis/{id}/` - Atualizar responsável
- `DELETE /api/responsaveis/{id}/` - Deletar responsável

## ��� Variáveis de Ambiente (.env)

```env
# Django
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
# DB_USER=seu_usuario
# DB_PASSWORD=sua_senha
# DB_HOST=localhost
# DB_PORT=5432

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 🧪 Testes

Executar os testes do projeto:
```bash
python manage.py test
```

Com cobertura:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📁 Estrutura do Projeto

```
Sistema-de-cadastro-para-alunos/
├── config/                 # Configurações do Django
│   ├── settings.py        # Settings
│   ├── urls.py            # URLs principais
│   └── wsgi.py            # WSGI config
├── alunos/                 # App principal
│   ├── models.py          # Modelos (Aluno, Nota, Presença, Responsável)
│   ├── views.py           # ViewSets da API
│   ├── serializers.py     # Serializers DRF
│   ├── urls.py            # URLs da app
│   ├── admin.py           # Admin Django
│   └── tests.py           # Testes unitários
├── .github/
│   └── workflows/         # GitHub Actions CI/CD
├── manage.py              # Django manage
├── requirements.txt       # Dependências Python
├── .env.example           # Template de variáveis
└── README.md              # Este arquivo
```

## 🔐 Painel de Administração

Acesse o painel em: `http://127.0.0.1:8000/admin`

Use as credenciais do superusuário criado na instalação.

## 🛠️ Tecnologias Utilizadas

- **Django 4.2** - Framework web
- **Django REST Framework 3.14** - API REST
- **PostgreSQL/SQLite** - Banco de dados
- **Python 3.11+** - Linguagem
- **docker** (opcional) - Containerização
- **GitHub Actions** - CI/CD

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

**Joana DS** - [GitHub](https://github.com/joanads-coder)

## 💬 Suporte

Para dúvidas ou sugestões, abra uma [issue](https://github.com/joanads-coder/Sistema-de-cadastro-para-alunos/issues) no repositório.

---

**Última atualização:** 2026-05-11
