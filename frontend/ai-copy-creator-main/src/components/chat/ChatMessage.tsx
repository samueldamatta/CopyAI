import { User, Sparkles, Copy, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

const ChatMessage = ({ role, content }: ChatMessageProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isUser = role === "user";

  return (
    <div
      className={`py-6 px-4 md:px-8 animate-fade-in ${
        isUser ? "bg-chat-user" : "bg-chat-assistant"
      }`}
    >
      <div className="max-w-3xl mx-auto flex gap-4">
        {/* Avatar */}
        <div
          className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
            isUser ? "bg-secondary" : "bg-primary"
          }`}
        >
          {isUser ? (
            <User className="w-4 h-4 text-foreground" />
          ) : (
            <Sparkles className="w-4 h-4 text-primary-foreground" />
          )}
        </div>

        {/* Content */}
        <div className="flex-1 space-y-2">
          <p className="text-sm font-medium text-muted-foreground">
            {isUser ? "Você" : "CopyAI"}
          </p>
          <div className="text-foreground whitespace-pre-wrap leading-relaxed">
            {content}
          </div>

          {/* Actions for assistant messages */}
          {!isUser && (
            <div className="flex items-center gap-2 pt-2">
              <Button
                variant="ghost"
                size="icon-sm"
                className="text-muted-foreground hover:text-foreground"
                onClick={handleCopy}
              >
                {copied ? (
                  <Check className="h-4 w-4 text-primary" />
                ) : (
                  <Copy className="h-4 w-4" />
                )}
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
