# 🤖 CopyAI - Agente de Copys com ChatGPT

Aplicação completa para criação de copys publicitárias usando inteligência artificial (ChatGPT).

## ✨ Funcionalidades

- 🤖 **ChatGPT integrado** - Respostas reais do GPT-4/GPT-3.5
- 🔐 **Autenticação completa** - Login, signup com JWT
- 💬 **Chat inteligente** - Conversas contextualizadas
- 📚 **Histórico** - Todas as conversas salvas no MongoDB
- 🎨 **Interface moderna** - React + TailwindCSS + shadcn/ui
- ⚡ **API REST rápida** - FastAPI assíncrono

## 🏗️ Arquitetura

```
┌──────────────────┐
│  Frontend React  │  ← Interface do usuário
└────────┬─────────┘
         │ HTTP/WebSocket
         ▼
┌────────────────────┐
│  Backend FastAPI   │  ← API REST + Autenticação
└────────┬───────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────┐
│MongoDB │ │ ChatGPT  │
│        │ │ (OpenAI) │
└────────┘ └──────────┘
```

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8+
- Node.js 16+
- Docker (para MongoDB)
- Conta OpenAI (para ChatGPT)

### 1. Backend

```bash
cd backend

# Ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar
pip install -r requirements.txt

# Configurar
cp env.template .env
# Adicione sua OPENAI_API_KEY no .env

# MongoDB
docker run -d -p 27017:27017 --name mongodb mongo

# Testar
python test_chatgpt.py

# Rodar
python main.py
```

✅ Backend: http://localhost:8000  
✅ Docs: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend/ai-copy-creator-main

# Instalar
npm install

# Rodar
npm run dev
```

✅ Frontend: http://localhost:5173

## 📖 Documentação

- **[QUICKSTART.md](QUICKSTART.md)** - Início rápido em 5 minutos
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Guia completo de integração
- **[backend/README.md](backend/README.md)** - Documentação do backend

## 🎯 Como Usar

1. **Criar conta** em http://localhost:5173/signup
2. **Fazer login** automaticamente
3. **Enviar mensagem:** "Crie uma copy para produto X"
4. **ChatGPT responde** com copy profissional
5. **Histórico salvo** automaticamente

## 📁 Estrutura do Projeto

```
CopyAI/
├── backend/              # FastAPI + ChatGPT + MongoDB
│   ├── routes/          # Endpoints da API
│   ├── services/        # Lógica de negócio
│   │   └── ai_service.py    # Integração ChatGPT ⭐
│   ├── models/          # Modelos MongoDB
│   ├── schemas/         # Validação Pydantic
│   └── middleware/      # Auth JWT
│
├── frontend/            # React + TypeScript
│   └── ai-copy-creator-main/
│       ├── src/
│       │   ├── services/
│       │   │   └── api.ts       # Cliente API ⭐
│       │   ├── contexts/
│       │   │   └── AuthContext.tsx  # Auth ⭐
│       │   └── pages/
│       │       ├── Index.tsx    # Chat principal
│       │       ├── Login.tsx    # Login
│       │       └── Signup.tsx   # Cadastro
│
└── INTEGRATION_GUIDE.md # Guia completo
```

## 🔧 Tecnologias

### Backend
- **FastAPI** - Framework web moderno
- **MongoDB + Motor** - Banco de dados NoSQL assíncrono
- **OpenAI API** - ChatGPT (GPT-4/GPT-3.5)
- **JWT** - Autenticação segura
- **Pydantic** - Validação de dados

### Frontend
- **React** - Library UI
- **TypeScript** - Type safety
- **TailwindCSS** - Estilização
- **shadcn/ui** - Componentes
- **Axios** - Cliente HTTP
- **React Router** - Navegação

## 🤖 ChatGPT

### Modelos Disponíveis

| Modelo | Qualidade | Custo | Uso |
|--------|-----------|-------|-----|
| GPT-3.5 Turbo | ⭐⭐⭐⭐ | $0.002/1K tokens | Testes |
| GPT-4 Turbo | ⭐⭐⭐⭐⭐ | $0.01/1K tokens | Produção |

### Estimativa de Custos

- 1 copy completa: ~$0.05
- 100 copys: ~$5.00
- 1000 copys: ~$50.00

### Configuração

1. Obtenha API Key: https://platform.openai.com/api-keys
2. Adicione no `backend/.env`:
   ```
   OPENAI_API_KEY=sk-sua-chave-aqui
   ```

## 📊 API Endpoints

### Autenticação
- `POST /api/auth/signup` - Criar conta
- `POST /api/auth/login` - Login

### Chat
- `POST /api/chat/message` - Enviar mensagem ao ChatGPT
- `GET /api/chat/models` - Listar modelos disponíveis

### Conversas
- `GET /api/conversations` - Listar conversas
- `GET /api/conversations/{id}` - Ver conversa
- `DELETE /api/conversations/{id}` - Deletar conversa

## 🐛 Solução de Problemas

### Backend não inicia
```bash
# Verificar MongoDB
docker ps

# Se não estiver rodando
docker start mongodb
```

### ChatGPT não responde
```bash
# Testar API Key
cd backend
python test_chatgpt.py

# Verificar créditos
# https://platform.openai.com/usage
```

### Erro 401 no frontend
```
Problema: Token expirado
Solução: Fazer logout e login novamente
```

## 🔐 Segurança

- ✅ Senhas hasheadas (bcrypt)
- ✅ Autenticação JWT
- ✅ Rotas protegidas
- ✅ CORS configurado
- ✅ Validação de inputs
- ✅ Rate limiting (recomendado em produção)

## 🚀 Deploy

### Backend
- Render, Railway, AWS, DigitalOcean
- Variáveis de ambiente:
  - `OPENAI_API_KEY`
  - `MONGODB_URL`
  - `SECRET_KEY`

### Frontend
- Vercel, Netlify, Cloudflare Pages
- Variável de ambiente:
  - `VITE_API_URL`

### MongoDB
- MongoDB Atlas (cloud gratuito)

## 📝 Licença

Este projeto é proprietário e privado.

## 🤝 Contribuindo

Para contribuir:
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

## 🙏 Agradecimentos

- OpenAI pelo ChatGPT
- FastAPI pela excelente framework
- shadcn/ui pelos componentes

---

**Desenvolvido com ❤️ usando FastAPI, React e ChatGPT**

🤖 **Powered by ChatGPT (OpenAI)**

