import axios from 'axios';

// URL base da API do backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Criar instância do Axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token JWT nas requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratar erros de resposta
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token inválido ou expirado
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Tipos
export interface SignupData {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
  created_at: string;
}

export interface Message {
  role: string;
  content: string;
  timestamp: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  copy_type: string;
  messages: Message[];
  created_at: string;
  updated_at: string;
  is_archived: boolean;
}

export interface ConversationListItem {
  id: string;
  title: string;
  copy_type: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

// Serviços de Autenticação
export const authService = {
  signup: async (data: SignupData): Promise<User> => {
    const response = await api.post<User>('/auth/signup', data);
    return response.data;
  },

  login: async (data: LoginData): Promise<TokenResponse> => {
    const response = await api.post<TokenResponse>('/auth/login', data);
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await api.get<User>('/users/me');
    return response.data;
  },
};

// Serviços de Chat
export const chatService = {
  sendMessage: async (content: string, conversationId?: string, copyType?: string, brief?: any): Promise<Message> => {
    const response = await api.post<Message>('/chat/message', {
      content,
      conversation_id: conversationId,
      copy_type: copyType || "geral",
      brief,
    });
    return response.data;
  },

  getModels: async (): Promise<any> => {
    const response = await api.get('/chat/models');
    return response.data;
  },
};

// Serviços de Conversas
export const conversationService = {
  getConversations: async (includeArchived = false): Promise<ConversationListItem[]> => {
    const response = await api.get<ConversationListItem[]>('/conversations', {
      params: { include_archived: includeArchived },
    });
    return response.data;
  },

  getConversation: async (id: string): Promise<Conversation> => {
    const response = await api.get<Conversation>(`/conversations/${id}`);
    return response.data;
  },

  createConversation: async (title?: string): Promise<Conversation> => {
    const response = await api.post<Conversation>('/conversations', { title });
    return response.data;
  },

  deleteConversation: async (id: string): Promise<void> => {
    await api.delete(`/conversations/${id}`);
  },

  archiveConversation: async (id: string): Promise<void> => {
    await api.post(`/conversations/${id}/archive`);
  },

  updateBrief: async (id: string, brief: any): Promise<Conversation> => {
    const response = await api.patch<Conversation>(`/conversations/${id}/brief`, { brief });
    return response.data;
  },
};

export default api;

