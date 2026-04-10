# Projeto: My Routine

## Stack

### Backend
- **Linguagem**: Python 3.12+
- **Framework**: FastAPI
- **Banco de dados**: Supabase (PostgreSQL gerenciado)
- **ORM**: SQLAlchemy (async) + Alembic (migrations)
- **Container**: Docker + docker-compose
- **Deploy**: Vercel (Serverless Functions Python)

### Frontend
- **Linguagem**: TypeScript
- **Framework**: React + Vite
- **Estilização**: Tailwind CSS
- **Deploy**: Vercel

## Arquitetura

### Backend (DDD + Hexagonal / Clean Architecture)
- **Padrão**: DDD + Hexagonal (Clean Architecture)
- **Camadas**:
  - `domain/` - Entidades, Value Objects, Domain Events, Repository interfaces (ABC)
  - `application/` - Use Cases, Application Services, DTOs (Pydantic)
  - `infrastructure/` - Adapters, Repository implementations (Supabase/SQLAlchemy), External services
  - `presentation/` - Routers FastAPI, Middlewares, Schemas de request/response

### Frontend (Feature-based)
- **Padrão**: Feature-based structure
- **Camadas**:
  - `components/` - Componentes reutilizáveis (UI Kit)
  - `features/` - Features organizadas por domínio (login, treinos, calendário)
  - `hooks/` - Custom hooks
  - `services/` - Chamadas à API
  - `types/` - Tipos TypeScript compartilhados

## Estrutura do Monorepo

```
my-routine/
├── backend/                # Python FastAPI
│   ├── app/
│   │   ├── main.py         # Entry point FastAPI
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── presentation/
│   ├── tests/
│   ├── alembic/            # Migrations
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/               # React App
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml      # Backend dockerizado
├── vercel.json
└── CLAUDE.md
```

## Convenções

### Código - Backend (Python)
- Nomes de classes: PascalCase
- Nomes de funções/métodos: snake_case
- Nomes de arquivos: snake_case
- Testes: em `tests/` espelhando a estrutura de `app/`, prefixo `test_`
- Type hints obrigatórios em todas as funções
- Pydantic para DTOs e validação

### Código - Frontend (TypeScript/React)
- Nomes de componentes: PascalCase
- Nomes de funções/hooks: camelCase
- Nomes de arquivos: kebab-case para utils, PascalCase para componentes
- Testes: ao lado do arquivo com sufixo `.test.tsx`

### Git
- Commits: conventional commits (feat:, fix:, refactor:, test:, docs:)
- Branch naming: feature/xxx, bugfix/xxx

## Comandos

```bash
# Backend - Docker
docker-compose up backend       # Sobe o backend
docker-compose run backend pytest  # Roda testes

# Backend - Local (sem Docker)
cd backend && pip install -r requirements.txt
cd backend && uvicorn app.main:app --reload --port 8000
cd backend && pytest

# Frontend - Instalar dependências
cd frontend && npm install

# Frontend - Rodar testes
cd frontend && npm test

# Frontend - Rodar lint
cd frontend && npm run lint

# Frontend - Rodar aplicação
cd frontend && npm run dev
```

## Regras Específicas do Projeto

- Interface do app em **português brasileiro**
- Categorias de treino: Musculação, Cardio, Pilates
- Grupos musculares (apenas para Musculação): Peito, Costas, Ombros, Bíceps, Tríceps, Pernas (Quadríceps/Posterior/Panturrilha), Abdômen
- Registro obrigatório: fiz / não fiz
- Registro opcional: tempo gasto (em minutos)
- Autenticação: tela de login visual sem validação (por enquanto)
- Layout: clean e minimalista, inspirado em apps como Hevy e Strong
- Frontend **responsivo (mobile-first)**: deve funcionar bem em celular
- Visualização do histórico: calendário estilo "GitHub contributions"
- Database: Supabase (PostgreSQL)
- Deploy: Vercel (frontend) + Docker (backend)
- Backend **obrigatoriamente dockerizado**
