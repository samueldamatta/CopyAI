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
  Sparkles,
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
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { conversationService } from "@/services/api";

interface ChatInputProps {
  onSend: (message: string, copyType?: string, briefData?: any) => void;
  isLoading?: boolean;
  initialCopyType?: string;
  conversationId?: string | null;
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

const ChatInput = ({ onSend, isLoading = false, initialCopyType = "geral", conversationId }: ChatInputProps) => {
  const [message, setMessage] = useState("");
  const [copyType, setCopyType] = useState(initialCopyType);
  const [isBriefModalOpen, setIsBriefModalOpen] = useState(false);
  const [briefData, setBriefData] = useState({
    publico: "",
    dor: "",
    oferta: "",
    provaSocial: "",
    tom: "",
  });
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Abrir o modal automaticamente se o componente for montado com um tipo específico (ex: via sugestão)
  // Ou se o tipo inicial mudar via prop do componente pai (Index.tsx)
  useEffect(() => {
    if (initialCopyType !== copyType) {
      setCopyType(initialCopyType);
      if (initialCopyType !== "geral") {
        setIsBriefModalOpen(true);
      }
    }
  }, [initialCopyType]);

  const handleCopyTypeChange = (value: string) => {
    setCopyType(value);
    if (value !== "geral") {
      setIsBriefModalOpen(true);
    }
  };

  const handleSendBrief = async (e: React.FormEvent) => {
    e.preventDefault();

    // Salvar no MongoDB se houver uma conversa ativa
    if (conversationId) {
      try {
        await conversationService.updateBrief(conversationId, briefData);
      } catch (error) {
        console.error("Erro ao salvar brief no banco:", error);
      }
    }

    const briefMessage = `
Brief detalhado:
- Público-alvo: ${briefData.publico}
- Principal dor/problema: ${briefData.dor}
- Oferta final: ${briefData.oferta}
${briefData.provaSocial ? `- Prova Social: ${briefData.provaSocial}` : ""}
- Tom de voz: ${briefData.tom || "Persuasivo e amigável"}

${message ? `Informações adicionais: ${message}` : ""}
`.trim();

    onSend(briefMessage, copyType, briefData);
    setMessage("");
    setBriefData({
      publico: "",
      dor: "",
      oferta: "",
      provaSocial: "",
      tom: "",
    });
    setIsBriefModalOpen(false);
  };

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
          <Select value={copyType} onValueChange={handleCopyTypeChange} disabled={isLoading}>
            <SelectTrigger className="flex-1 bg-secondary border-border">
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

          <Button
            type="button"
            variant="outline"
            size="sm"
            className="gap-2 text-primary border-primary/20 bg-primary/5 hover:bg-primary/10 whitespace-nowrap h-10"
            onClick={() => setIsBriefModalOpen(true)}
          >
            <Sparkles className="h-4 w-4" />
            {copyType === "geral" ? "Preencher Brief" : "Ver Brief"}
          </Button>
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
          CopyAI pode cometer erros. Sempre revise suas copys antes de usar.
        </p>
      </form>

      {/* Mini-form de Brief */}
      <Dialog open={isBriefModalOpen} onOpenChange={setIsBriefModalOpen}>
        <DialogContent className="sm:max-w-[500px] max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              Brief para {COPY_TYPES.find(t => t.value === copyType)?.label}
            </DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSendBrief} className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="publico">Quem é o público-alvo?</Label>
              <Input
                id="publico"
                placeholder="Ex: Empreendedores digitais que faturam +10k"
                value={briefData.publico}
                onChange={e => setBriefData({ ...briefData, publico: e.target.value })}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="dor">Qual o principal problema/dor eles enfrentam?</Label>
              <Textarea
                id="dor"
                placeholder="Ex: Eles têm dificuldade em escalar anúncios sem perder o ROI"
                value={briefData.dor}
                onChange={e => setBriefData({ ...briefData, dor: e.target.value })}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="oferta">Qual a oferta final?</Label>
              <Input
                id="oferta"
                placeholder="Ex: Treinamento Scale-UP com 50% de desconto"
                value={briefData.oferta}
                onChange={e => setBriefData({ ...briefData, oferta: e.target.value })}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="provaSocial">Prova social (opcional)</Label>
              <Input
                id="provaSocial"
                placeholder="Ex: +500 alunos, faturamento de clientes de 1M+"
                value={briefData.provaSocial}
                onChange={e => setBriefData({ ...briefData, provaSocial: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="tom">Tom de voz</Label>
              <Input
                id="tom"
                placeholder="Ex: Autoritário, Amigável, Descontraído..."
                value={briefData.tom}
                onChange={e => setBriefData({ ...briefData, tom: e.target.value })}
              />
            </div>

            <DialogFooter>
              <Button type="button" variant="ghost" onClick={() => setIsBriefModalOpen(false)}>
                Cancelar
              </Button>
              <Button type="submit" className="gap-2">
                <Sparkles className="h-4 w-4" />
                Gerar Copy
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ChatInput;
