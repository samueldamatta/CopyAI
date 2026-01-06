import Logo from "@/components/Logo";
import { ReactNode } from "react";

interface AuthLayoutProps {
  children: ReactNode;
  title: string;
  subtitle: string;
}

const AuthLayout = ({ children, title, subtitle }: AuthLayoutProps) => {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8 animate-fade-in">
        {/* Logo */}
        <div className="flex justify-center">
          <Logo size="lg" />
        </div>

        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-2xl md:text-3xl font-bold text-foreground">
            {title}
          </h1>
          <p className="text-muted-foreground">{subtitle}</p>
        </div>

        {/* Form container */}
        <div className="bg-card border border-border rounded-2xl p-6 md:p-8 shadow-xl">
          {children}
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
