import { Sparkles } from "lucide-react";

interface LogoProps {
  size?: "sm" | "md" | "lg";
  showText?: boolean;
}

const Logo = ({ size = "md", showText = true }: LogoProps) => {
  const sizes = {
    sm: "w-6 h-6",
    md: "w-8 h-8",
    lg: "w-12 h-12",
  };

  const textSizes = {
    sm: "text-lg",
    md: "text-xl",
    lg: "text-2xl",
  };

  return (
    <div className="flex items-center gap-2">
      <div className={`${sizes[size]} rounded-lg bg-primary flex items-center justify-center`}>
        <Sparkles className="w-1/2 h-1/2 text-primary-foreground" />
      </div>
      {showText && (
        <span className={`${textSizes[size]} font-semibold text-foreground`}>
          CopyAI
        </span>
      )}
    </div>
  );
};

export default Logo;
