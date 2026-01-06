import { Plus, MessageSquare, Settings, LogOut, Menu, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import Logo from "@/components/Logo";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";

interface Conversation {
  id: string;
  title: string;
  date: string;
}

interface ChatSidebarProps {
  conversations: Conversation[];
  activeConversation: string | null;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  onDeleteConversation: (id: string) => void;
  isOpen: boolean;
  onToggle: () => void;
}

const ChatSidebar = ({
  conversations,
  activeConversation,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  isOpen,
  onToggle,
}: ChatSidebarProps) => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [showLogoutDialog, setShowLogoutDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [conversationToDelete, setConversationToDelete] = useState<string | null>(null);

  const handleLogoutClick = () => {
    setShowLogoutDialog(true);
  };

  const handleConfirmLogout = () => {
    logout();
    setShowLogoutDialog(false);
    navigate("/login");
  };

  const handleDeleteClick = (e: React.MouseEvent, conversationId: string) => {
    e.stopPropagation(); // Evita que clique no botão delete selecione a conversa
    setConversationToDelete(conversationId);
    setShowDeleteDialog(true);
  };

  const handleConfirmDelete = () => {
    if (conversationToDelete) {
      onDeleteConversation(conversationToDelete);
      setConversationToDelete(null);
    }
    setShowDeleteDialog(false);
  };

  return (
    <>
      {/* Mobile toggle button */}
      <Button
        variant="ghost"
        size="icon"
        className="fixed top-4 left-4 z-50 md:hidden"
        onClick={onToggle}
      >
        <Menu className="h-5 w-5" />
      </Button>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={onToggle}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed md:relative left-0 top-0 h-full w-72 bg-sidebar border-r border-sidebar-border flex flex-col z-50 transform transition-transform duration-300 ease-in-out ${
          isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        }`}
      >
        {/* Header */}
        <div className="p-4 border-b border-sidebar-border">
          <div className="flex items-center justify-between mb-4">
            <Logo size="sm" />
          </div>
          <Button
            variant="outline"
            className="w-full justify-start gap-2 bg-transparent border-sidebar-border hover:bg-sidebar-accent"
            onClick={onNewChat}
          >
            <Plus className="h-4 w-4" />
            Nova conversa
          </Button>
        </div>

        {/* Conversations list */}
        <div className="flex-1 overflow-y-auto p-2">
          <p className="text-xs text-muted-foreground px-2 py-2 uppercase tracking-wider">
            Conversas recentes
          </p>
          <div className="space-y-1">
            {conversations.map((conversation) => (
              <div key={conversation.id} className="group relative">
                <Button
                  variant={activeConversation === conversation.id ? "sidebar-active" : "sidebar"}
                  className="w-full text-left h-auto py-3 px-3 pr-10"
                  onClick={() => onSelectConversation(conversation.id)}
                >
                  <MessageSquare className="h-4 w-4 flex-shrink-0" />
                  <div className="flex-1 truncate">
                    <p className="truncate text-sm">{conversation.title}</p>
                    <p className="text-xs text-muted-foreground">{conversation.date}</p>
                  </div>
                </Button>
                <Button
                  variant="ghost"
                  size="icon-sm"
                  className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity h-7 w-7 text-muted-foreground hover:text-destructive"
                  onClick={(e) => handleDeleteClick(e, conversation.id)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="p-2 border-t border-sidebar-border space-y-1">
          <Button variant="sidebar" className="w-full" onClick={handleLogoutClick}>
            <LogOut className="h-4 w-4" />
            Sair
          </Button>
        </div>
      </aside>

      {/* Diálogo de confirmação de logout */}
      <AlertDialog open={showLogoutDialog} onOpenChange={setShowLogoutDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Deseja sair?</AlertDialogTitle>
            <AlertDialogDescription>
              Você será desconectado da sua conta e redirecionado para a tela de login.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction onClick={handleConfirmLogout}>
              Sair
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Diálogo de confirmação de exclusão */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Excluir conversa?</AlertDialogTitle>
            <AlertDialogDescription>
              Esta ação não pode ser desfeita. A conversa e todas as mensagens serão permanentemente excluídas.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction 
              onClick={handleConfirmDelete}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Excluir
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
};

export default ChatSidebar;
