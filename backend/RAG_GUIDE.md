# 📚 Guia RAG (Retrieval-Augmented Generation)

## O que é RAG?

RAG permite que o ChatGPT responda com base em documentos que você fornece, tornando as respostas mais precisas e contextualizadas.

## ⚡ Armazenamento 100% Local

**Tudo fica no seu projeto:**
- ✅ PDFs salvos em: `backend/storage/pdfs/`
- ✅ Embeddings em: `backend/storage/chroma_db/`
- ✅ Metadados no MongoDB
- ✅ Sem dependências de serviços externos (exceto OpenAI para embeddings)

## Fluxo de Funcionamento

```
1. Usuário faz upload de PDF
2. PDF é salvo em backend/storage/pdfs/{user_id}/
3. Sistema extrai texto do PDF
4. Texto é dividido em chunks (pedaços)
5. Cada chunk gera um embedding (vetor via OpenAI)
6. Embeddings são armazenados em backend/storage/chroma_db/ (arquivo local)
7. Quando usuário pergunta algo:
   - Sistema busca chunks mais relevantes no ChromaDB local
   - Chunks são enviados como contexto para ChatGPT
   - ChatGPT responde baseado no contexto do PDF
```

## Como Usar

### 1. Upload de PDF

**Endpoint:** `POST /api/documents/upload`

```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "Authorization: Bearer {seu_token}" \
  -F "file=@documento.pdf" \
  -F "conversation_id=abc123"
```

**Resposta:**
```json
{
  "filename": "documento.pdf",
  "total_pages": 10,
  "total_chunks": 25,
  "collection_name": "user_123_abc123",
  "status": "success"
}
```

### 2. Chat com RAG

O RAG funciona automaticamente! Quando você:
- Faz upload de um PDF em uma conversa
- Faz uma pergunta nessa conversa
- O sistema busca automaticamente contexto relevante no PDF
- ChatGPT responde usando esse contexto

**Exemplo:**

```
1. Upload: "manual_produto.pdf"
2. Pergunta: "Qual a garantia do produto?"
3. Sistema busca no PDF: encontra seção sobre garantia
4. ChatGPT responde: "Segundo o manual, a garantia é de 12 meses..."
```

### 3. Listar Documentos

**Endpoint:** `GET /api/documents/list`

```bash
curl "http://localhost:8000/api/documents/list?conversation_id=abc123" \
  -H "Authorization: Bearer {seu_token}"
```

### 4. Excluir Documento

**Endpoint:** `DELETE /api/documents/{document_id}`

```bash
curl -X DELETE "http://localhost:8000/api/documents/doc123" \
  -H "Authorization: Bearer {seu_token}"
```

## 📁 Estrutura de Armazenamento Local

```
backend/
├── storage/
│   ├── pdfs/                    # PDFs salvos
│   │   ├── user_123/           # Por usuário
│   │   │   ├── abc12345_documento1.pdf
│   │   │   └── def67890_manual.pdf
│   │   └── user_456/
│   │       └── xyz98765_relatorio.pdf
│   └── chroma_db/              # Embeddings (ChromaDB)
│       ├── chroma.sqlite3      # Banco local
│       └── ...                 # Arquivos do ChromaDB
├── .gitignore                  # storage/ está no .gitignore
└── ...
```

**Importante:** A pasta `storage/` é ignorada pelo git para não versionar PDFs e embeddings.

## Configurações

### Parâmetros Ajustáveis

No arquivo `services/rag_service.py`:

```python
# Tamanho dos chunks
chunk_size=1000  # Maior = mais contexto, mas menos preciso
chunk_overlap=200  # Sobreposição entre chunks

# Número de chunks retornados
k=3  # Quantos trechos relevantes usar
```

### Caminhos Locais

Tudo é armazenado em:
```python
backend/storage/pdfs/         # Arquivos PDF
backend/storage/chroma_db/    # Embeddings persistentes
```

## Limitações

- **Tamanho máximo:** 10MB por PDF
- **Formato suportado:** Apenas PDF
- **Idioma:** Funciona melhor em inglês, mas português também funciona
- **Custo:** Cada busca usa embeddings da OpenAI (muito barato ~$0.0001/1K tokens)

## Melhorias Futuras

- [ ] Suporte para DOCX, TXT
- [ ] Upload múltiplo
- [ ] Visualizar trechos usados no chat
- [ ] Cache de embeddings
- [ ] Suporte para imagens em PDFs (OCR)

## Troubleshooting

### "Erro ao processar PDF"
- Verifique se o PDF não está corrompido
- Tente com um PDF mais simples primeiro

### "Sem resultados relevantes"
- Aumente o valor de `k` para buscar mais chunks
- Refine sua pergunta para ser mais específica

### "Resposta não usa o contexto"
- Verifique se o PDF foi processado corretamente
- Confirme que está usando a mesma `conversation_id`

