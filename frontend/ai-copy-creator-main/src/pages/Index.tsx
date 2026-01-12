import { useState, useRef, useEffect } from "react";
import ChatSidebar from "@/components/chat/ChatSidebar";
import ChatMessage from "@/components/chat/ChatMessage";
import ChatInput from "@/components/chat/ChatInput";
import WelcomeScreen from "@/components/chat/WelcomeScreen";
import TypingIndicator from "@/components/chat/TypingIndicator";
import { chatService, conversationService } from "@/services/api";
import { useToast } from "@/hooks/use-toast";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

interface Conversation {
  id: string;
  title: string;
  date: string;
  messages: Message[];
}

const Index = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversation, setActiveConversation] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentCopyType, setCurrentCopyType] = useState<string>("geral");
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Carregar conversas ao montar o componente
  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const convList = await conversationService.getConversations();
      const formattedConversations: Conversation[] = convList.map((conv) => ({
        id: conv.id,
        title: conv.title,
        date: formatDate(conv.updated_at),
        messages: [],
      }));
      setConversations(formattedConversations);
    } catch (error) {
      console.error("Erro ao carregar conversas:", error);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));

    if (diffInDays === 0) return "Hoje";
    if (diffInDays === 1) return "Ontem";
    if (diffInDays < 7) return `${diffInDays} dias atrás`;
    return date.toLocaleDateString("pt-BR");
  };

  const handleSendMessage = async (content: string, copyType?: string, briefData?: any) => {
    // Se o conteúdo estiver vazio mas o copyType existir, apenas abre o modal no ChatInput
    if (!content && copyType) {
      setCurrentCopyType(copyType);
      return;
    }

    // Atualizar o tipo de copy atual
    if (copyType) {
      setCurrentCopyType(copyType);
    }

    // Adicionar o tipo de copy na mensagem se não for "geral"
    const fullContent = copyType && copyType !== "geral" 
      ? `[Tipo de Copy: ${copyType}]\n\n${content}`
      : content;

    const newMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
    };

    setMessages((prev) => [...prev, newMessage]);
    setIsLoading(true);

    try {
      // Enviar mensagem para o backend (ChatGPT) com o tipo de copy e brief
      const response = await chatService.sendMessage(
        fullContent, 
        activeConversation || undefined,
        copyType || currentCopyType,
        briefData
      );

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.content,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Recarregar lista de conversas
      await loadConversations();

      // Se não havia conversa ativa, definir a primeira como ativa
      if (!activeConversation) {
        const convList = await conversationService.getConversations();
        if (convList.length > 0) {
          setActiveConversation(convList[0].id);
        }
      }
    } catch (error: any) {
      console.error("Erro ao enviar mensagem:", error);
      toast({
        title: "Erro ao enviar mensagem",
        description: error.response?.data?.detail || "Não foi possível enviar a mensagem. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setActiveConversation(null);
    setMessages([]);
    setCurrentCopyType("geral");
    setSidebarOpen(false);
  };

  const handleSelectConversation = async (id: string) => {
    setActiveConversation(id);
    setSidebarOpen(false);
    
    try {
      const conversation = await conversationService.getConversation(id);
      
      // Restaurar o tipo de copy da conversa
      setCurrentCopyType(conversation.copy_type || "geral");
      
      const formattedMessages: Message[] = conversation.messages.map((msg, index) => ({
        id: `${id}-${index}`,
        role: msg.role as "user" | "assistant",
        content: msg.content,
      }));
      
      setMessages(formattedMessages);
    } catch (error: any) {
      console.error("Erro ao carregar conversa:", error);
      toast({
        title: "Erro ao carregar conversa",
        description: error.response?.data?.detail || "Não foi possível carregar a conversa. Tente novamente.",
        variant: "destructive",
      });
    }
  };

  const handleDeleteConversation = async (id: string) => {
    try {
      await conversationService.deleteConversation(id);
      
      // Remover da lista local
      setConversations((prev) => prev.filter((conv) => conv.id !== id));
      
      // Se a conversa deletada era a ativa, limpar as mensagens
      if (activeConversation === id) {
        setActiveConversation(null);
        setMessages([]);
        setCurrentCopyType("geral");
      }
      
      toast({
        title: "Conversa excluída",
        description: "A conversa foi excluída com sucesso.",
      });
    } catch (error: any) {
      console.error("Erro ao excluir conversa:", error);
      toast({
        title: "Erro ao excluir conversa",
        description: error.response?.data?.detail || "Não foi possível excluir a conversa. Tente novamente.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <ChatSidebar
        conversations={conversations}
        activeConversation={activeConversation}
        onSelectConversation={handleSelectConversation}
        onNewChat={handleNewChat}
        onDeleteConversation={handleDeleteConversation}
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
      />

      <main className="flex-1 flex flex-col min-w-0">
        {messages.length === 0 ? (
          <WelcomeScreen onSuggestionClick={handleSendMessage} />
        ) : (
          <div className="flex-1 overflow-y-auto">
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                role={message.role}
                content={message.content}
              />
            ))}
            {isLoading && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        )}

        <ChatInput 
          key={activeConversation || "new"}
          onSend={handleSendMessage} 
          isLoading={isLoading}
          initialCopyType={currentCopyType}
          conversationId={activeConversation}
        />
      </main>
    </div>
  );
};

export default Index;
