import { Sparkles } from "lucide-react";

const TypingIndicator = () => {
  return (
    <div className="py-6 px-4 md:px-8 bg-chat-assistant animate-fade-in">
      <div className="max-w-3xl mx-auto flex gap-4">
        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center flex-shrink-0">
          <Sparkles className="w-4 h-4 text-primary-foreground" />
        </div>
        <div className="flex-1 space-y-2">
          <p className="text-sm font-medium text-muted-foreground">CopyAI</p>
          <div className="flex items-center gap-1">
            <span className="w-2 h-2 bg-muted-foreground rounded-full animate-typing" style={{ animationDelay: "0ms" }} />
            <span className="w-2 h-2 bg-muted-foreground rounded-full animate-typing" style={{ animationDelay: "200ms" }} />
            <span className="w-2 h-2 bg-muted-foreground rounded-full animate-typing" style={{ animationDelay: "400ms" }} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
