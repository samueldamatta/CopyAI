# 🎨 Exemplo de Implementação RAG no Frontend

## 1. Adicionar ao API Service

```typescript
// src/services/api.ts

export const documentService = {
  uploadPdf: async (file: File, conversationId?: string): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    if (conversationId) {
      formData.append('conversation_id', conversationId);
    }

    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  listDocuments: async (conversationId?: string): Promise<any[]> => {
    const params = conversationId ? { conversation_id: conversationId } : {};
    const response = await api.get('/documents/list', { params });
    return response.data;
  },

  deleteDocument: async (documentId: string): Promise<void> => {
    await api.delete(`/documents/${documentId}`);
  },
};
```

## 2. Componente de Upload de PDF

```typescript
// src/components/chat/PdfUpload.tsx

import { useState } from 'react';
import { Upload, File, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';
import { documentService } from '@/services/api';

interface PdfUploadProps {
  conversationId?: string;
  onUploadComplete?: () => void;
}

export const PdfUpload = ({ conversationId, onUploadComplete }: PdfUploadProps) => {
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { toast } = useToast();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        toast({
          title: 'Erro',
          description: 'Apenas arquivos PDF são suportados',
          variant: 'destructive',
        });
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        toast({
          title: 'Arquivo muito grande',
          description: 'O tamanho máximo é 10MB',
          variant: 'destructive',
        });
        return;
      }

      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    try {
      const result = await documentService.uploadPdf(selectedFile, conversationId);
      
      toast({
        title: 'PDF enviado!',
        description: `${result.total_chunks} trechos processados. Agora você pode fazer perguntas sobre o documento.`,
      });

      setSelectedFile(null);
      onUploadComplete?.();
    } catch (error: any) {
      toast({
        title: 'Erro ao enviar PDF',
        description: error.response?.data?.detail || 'Tente novamente',
        variant: 'destructive',
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-4 border border-border rounded-lg bg-secondary">
      <div className="flex items-center gap-2 mb-2">
        <Upload className="h-4 w-4 text-primary" />
        <span className="text-sm font-medium">Adicionar Documento (RAG)</span>
      </div>
      
      {selectedFile ? (
        <div className="flex items-center justify-between p-2 bg-background rounded">
          <div className="flex items-center gap-2">
            <File className="h-4 w-4" />
            <span className="text-sm truncate">{selectedFile.name}</span>
          </div>
          <div className="flex gap-2">
            <Button
              size="sm"
              onClick={handleUpload}
              disabled={uploading}
            >
              {uploading ? 'Processando...' : 'Enviar'}
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setSelectedFile(null)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      ) : (
        <label className="cursor-pointer">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            className="hidden"
          />
          <div className="border-2 border-dashed border-border rounded p-4 text-center hover:border-primary transition-colors">
            <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
            <p className="text-sm text-muted-foreground">
              Clique para selecionar um PDF
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              Máximo 10MB
            </p>
          </div>
        </label>
      )}
    </div>
  );
};
```

## 3. Integrar no ChatInput ou Index

```typescript
// Em Index.tsx, adicione o componente:

import { PdfUpload } from '@/components/chat/PdfUpload';

// Dentro do render:
<div className="p-4 space-y-4">
  <PdfUpload 
    conversationId={activeConversation || undefined}
    onUploadComplete={loadDocuments}
  />
  <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
</div>
```

## 4. Mostrar Documentos Anexados

```typescript
// src/components/chat/DocumentList.tsx

import { File, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface Document {
  id: string;
  filename: string;
  file_size: number;
  total_pages: number;
}

interface DocumentListProps {
  documents: Document[];
  onDelete: (id: string) => void;
}

export const DocumentList = ({ documents, onDelete }: DocumentListProps) => {
  if (documents.length === 0) return null;

  return (
    <div className="p-4 border border-border rounded-lg bg-secondary">
      <p className="text-sm font-medium mb-2">Documentos anexados:</p>
      <div className="space-y-2">
        {documents.map((doc) => (
          <div key={doc.id} className="flex items-center justify-between p-2 bg-background rounded text-sm">
            <div className="flex items-center gap-2">
              <File className="h-4 w-4 text-primary" />
              <div>
                <p className="font-medium">{doc.filename}</p>
                <p className="text-xs text-muted-foreground">
                  {doc.total_pages} páginas • {(doc.file_size / 1024).toFixed(0)}KB
                </p>
              </div>
            </div>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => onDelete(doc.id)}
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
};
```

## 🎯 Fluxo de Uso

1. **Usuário abre uma conversa**
2. **Clica em "Adicionar Documento"**
3. **Seleciona um PDF**
4. **Sistema processa (pode demorar 10-30s)**
5. **Toast confirma sucesso**
6. **Usuário faz perguntas** → ChatGPT usa contexto do PDF automaticamente!

## 💡 Dicas

- Mostre um badge "📄 Com RAG" quando há documentos
- Adicione loading state durante upload
- Mostre preview dos trechos usados (opcional)
- Permita upload múltiplo

