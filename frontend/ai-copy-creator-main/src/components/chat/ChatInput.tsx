import { 
  Send, 
  Paperclip, 
  FileText, 
  Megaphone,
  MessageSquare,
  Mail,
  Target,
  ShoppingBag,
  Video,
  Image,
  Globe,
  type LucideIcon
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState, useRef, useEffect } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface ChatInputProps {
  onSend: (message: string, copyType?: string) => void;
  isLoading?: boolean;
  initialCopyType?: string;
}

interface CopyType {
  value: string;
  label: string;
  icon: LucideIcon;
}

const COPY_TYPES: CopyType[] = [
  { value: "geral", label: "Geral / Não especificado", icon: FileText },
  { value: "anuncios", label: "Anúncios (Facebook, Google, Instagram)", icon: Megaphone },
  { value: "redes-sociais", label: "Posts para Redes Sociais", icon: MessageSquare },
  { value: "emails", label: "Emails de Marketing", icon: Mail },
  { value: "landing-pages", label: "Landing Pages", icon: Target },
  { value: "descricoes-produtos", label: "Descrições de Produtos", icon: ShoppingBag },
  { value: "scripts-videos", label: "Scripts para Vídeos", icon: Video },
  { value: "legendas", label: "Legendas e Captions", icon: Image },
  { value: "sites-blogs", label: "Textos para Sites e Blogs", icon: Globe },
];

const ChatInput = ({ onSend, isLoading = false, initialCopyType = "geral" }: ChatInputProps) => {
  const [message, setMessage] = useState("");
  const [copyType, setCopyType] = useState(initialCopyType);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Atualizar copyType quando initialCopyType mudar (ao selecionar uma conversa)
  useEffect(() => {
    setCopyType(initialCopyType);
  }, [initialCopyType]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSend(message.trim(), copyType);
      setMessage("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  }, [message]);

  return (
    <div className="border-t border-border bg-background p-4">
      <form onSubmit={handleSubmit} className="max-w-3xl mx-auto space-y-3">
        {/* Seletor de Tipo de Copy */}
        <div className="flex items-center gap-2">
          <Select value={copyType} onValueChange={setCopyType} disabled={isLoading}>
            <SelectTrigger className="w-full bg-secondary border-border">
              <SelectValue placeholder="Selecione o tipo de copy" />
            </SelectTrigger>
            <SelectContent>
              {COPY_TYPES.map((type) => {
                const IconComponent = type.icon;
                return (
                  <SelectItem key={type.value} value={type.value}>
                    <div className="flex items-center gap-2">
                      <IconComponent className="h-4 w-4 text-primary" />
                      <span>{type.label}</span>
                    </div>
                  </SelectItem>
                );
              })}
            </SelectContent>
          </Select>
        </div>

        {/* Campo de mensagem */}
        <div className="relative flex items-end gap-2 bg-secondary rounded-2xl border border-border p-2 focus-within:border-primary transition-colors">
          <Button
            type="button"
            variant="ghost"
            size="icon-sm"
            className="text-muted-foreground hover:text-foreground flex-shrink-0"
          >
            <Paperclip className="h-5 w-5" />
          </Button>

          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Descreva a copy que você precisa..."
            className="flex-1 bg-transparent border-0 outline-none resize-none text-foreground placeholder:text-muted-foreground min-h-[24px] max-h-[200px] py-1 px-2"
            rows={1}
            disabled={isLoading}
          />

          <Button
            type="submit"
            variant="send"
            size="icon-sm"
            disabled={!message.trim() || isLoading}
            className="flex-shrink-0"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>

        <p className="text-xs text-muted-foreground text-center">
          AgentCopy pode cometer erros. Sempre revise suas copys antes de usar.
        </p>
      </form>
    </div>
  );
};

export default ChatInput;
