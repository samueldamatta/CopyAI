import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService, User, LoginData, SignupData } from '@/services/api';
import { useToast } from '@/hooks/use-toast';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (data: LoginData) => Promise<void>;
  signup: (data: SignupData) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const { toast } = useToast();

  // Verificar se há um token salvo ao carregar
  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await authService.getMe();
          setUser(userData);
        } catch (error) {
          console.error('Erro ao carregar usuário:', error);
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        }
      }
      setIsLoading(false);
    };

    loadUser();
  }, []);

  const login = async (data: LoginData) => {
    try {
      const response = await authService.login(data);
      localStorage.setItem('token', response.access_token);

      // Buscar dados do usuário
      const userData = await authService.getMe();
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));

      toast({
        title: 'Login realizado com sucesso!',
        description: `Bem-vindo(a) de volta, ${userData.username}!`,
      });
    } catch (error: any) {
      console.error('Erro no login:', error);
      toast({
        title: 'Erro no login',
        description: error.response?.data?.detail || 'Verifique suas credenciais e tente novamente.',
        variant: 'destructive',
      });
      throw error;
    }
  };

  const signup = async (data: SignupData) => {
    try {
      const newUser = await authService.signup(data);
      
      toast({
        title: 'Conta criada com sucesso!',
        description: 'Faça login para continuar.',
      });

      // Fazer login automático após cadastro
      await login({ email: data.email, password: data.password });
    } catch (error: any) {
      console.error('Erro no cadastro:', error);
      toast({
        title: 'Erro no cadastro',
        description: error.response?.data?.detail || 'Não foi possível criar sua conta. Tente novamente.',
        variant: 'destructive',
      });
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    toast({
      title: 'Logout realizado',
      description: 'Até logo!',
    });
  };

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    signup,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

