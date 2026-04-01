# AgentCopy — Projeto

## Visão

AgentCopy é uma plataforma de geração de copies publicitárias com IA. O objetivo é dar ao usuário um assistente especializado em copywriting que entende o contexto do negócio e produz textos de alta conversão, eliminando a necessidade de contratar redatores ou gastar horas escrevendo copies manualmente.

## Problema

Criar copies eficazes exige domínio de frameworks de copywriting (AIDA, PAS, Hook > Empatia > Solução > CTA), conhecimento do público-alvo e do produto, e muita iteração. A maioria dos empreendedores e times de marketing não tem esse domínio — ou quando têm, o processo é lento e custoso.

## Solução

Uma interface de chat onde o usuário descreve o que precisa e o agente:
1. Faz as perguntas certas (público, dor, oferta, diferencial)
2. Gera copies estruturadas usando frameworks de Direct Response
3. Mantém contexto da empresa via RAG (PDFs de briefing, materiais de marca)
4. Salva o histórico de conversas para refinamentos futuros

## Stack

| Camada | Tecnologia |
|---|---|
| Frontend | React 18 + TypeScript + Vite + Tailwind + shadcn/ui |
| Backend | FastAPI + Python + Uvicorn |
| Banco de dados | MongoDB (dados) + ChromaDB (embeddings) |
| IA | OpenAI API (GPT-4o) + Agents SDK |
| RAG | LangChain + ChromaDB + PyPDF |
| Autenticação | JWT + bcrypt |

## Estado Atual

### Implementado
- Autenticação completa (signup, login, JWT)
- Interface de chat com histórico de conversas
- Agente Copywriter especializado (persona de redator sênior de Direct Response)
- Agente gerador de títulos para conversas
- RAG: upload de PDFs, extração, chunking, embeddings e busca semântica
- Gerenciamento de conversas (criar, arquivar, deletar)
- Suporte a múltiplos modelos OpenAI (GPT-4o, GPT-4 Turbo, GPT-4o Mini)
- WebSocket para chat em tempo real
- Tipos de copy (geral, anúncios, redes sociais, etc.)
- Dados de brief por conversa (público-alvo, dores, oferta)

### Pendente / Backlog
- Autenticação no WebSocket (atualmente sem validação JWT)
- Dashboard de uso e custos da API OpenAI
- Export de copies (PDF, DOCX)
- Templates pré-definidos por segmento/nicho
- Editor de copies com versionamento
- Integração direta com plataformas de anúncio (Meta Ads, Google Ads)
- Deploy em produção (backend + frontend + MongoDB Atlas)

## Arquitetura

```
Frontend (React)
    │
    ├── HTTP REST  →  FastAPI Backend
    └── WebSocket  →  FastAPI Backend
                          │
                  ┌───────┼───────┐
                  ▼       ▼       ▼
               MongoDB  OpenAI  ChromaDB
               (dados)  (IA)   (embeddings)
```

### Fluxo principal
1. Usuário envia mensagem no chat
2. Backend busca contexto relevante no ChromaDB (RAG)
3. Contexto + histórico da conversa + mensagem são enviados ao Agente Copywriter
4. Agente responde com copy estruturada
5. Resposta e mensagem são salvas no MongoDB
6. Título da conversa é gerado automaticamente pelo Agente Título (GPT-4o Mini)

### Isolamento de dados
- Todas as operações são escopadas por `user_id`
- PDFs armazenados em `backend/storage/pdfs/{user_id}/`
- Embeddings isolados por coleção no ChromaDB (`user_{user_id}`)

## Variáveis de Ambiente

### Backend (`backend/.env`)
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=agentcopy_db
SECRET_KEY=<string hex 32 bytes>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=sk-...
FRONTEND_URL=http://localhost:5173
HOST=0.0.0.0
PORT=8000
```

### Frontend (`frontend/ai-copy-creator-main/.env`)
```
VITE_API_URL=http://localhost:8000/api
```

## Como rodar localmente

```bash
# MongoDB
docker run -d -p 27017:27017 --name mongodb mongo

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp env.template .env  # configurar OPENAI_API_KEY
python main.py

# Frontend
cd frontend/ai-copy-creator-main
npm install
npm run dev
```

- Backend: http://localhost:8000
- Docs da API: http://localhost:8000/docs
- Frontend: http://localhost:5173

## Deploy (produção)

| Serviço | Opções sugeridas |
|---|---|
| Backend | Render, Railway, AWS, DigitalOcean |
| Frontend | Vercel, Netlify, Cloudflare Pages |
| MongoDB | MongoDB Atlas (free tier disponível) |
| ChromaDB | Migrar para Pinecone ou Weaviate em produção |

## Custos estimados (OpenAI)

| Ação | Custo aprox. |
|---|---|
| 1 copy completa (GPT-4o) | ~$0.05 |
| 100 copies | ~$5.00 |
| Embedding de 1 PDF (1000 chunks) | ~$0.01 |
| Busca RAG por mensagem | ~$0.001 |
