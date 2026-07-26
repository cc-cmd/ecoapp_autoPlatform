import React, { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from 'react';
import { login as apiLogin, register as apiRegister } from '@/api/auth';
import type { User, LoginRequest, RegisterRequest } from '@/types';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

interface AuthContextValue extends AuthState {
  /** Authenticate with username & password. Stores token on success. */
  login: (data: LoginRequest) => Promise<void>;
  /** Register a new account. Does NOT auto-login — user must call login() separately. */
  register: (data: RegisterRequest) => Promise<void>;
  /** Clear auth state and remove stored credentials. */
  logout: () => Promise<void>;
}

// ---------------------------------------------------------------------------
// Context
// ---------------------------------------------------------------------------

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

// ---------------------------------------------------------------------------
// Provider
// ---------------------------------------------------------------------------

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Provides authentication state and actions to the component tree.
 * Initializes from localStorage on mount.
 */
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
  });

  // Initialize from localStorage on mount
  useEffect(() => {
    try {
      const token = localStorage.getItem('auth_token');
      const storedUser = localStorage.getItem('auth_user');
      if (token && storedUser) {
        const parsed = JSON.parse(storedUser);
        // Runtime validation: ensure stored user has required fields
        if (
          typeof parsed === 'object' && parsed !== null &&
          typeof parsed.id === 'string' &&
          typeof parsed.username === 'string'
        ) {
          const user: User = { id: parsed.id, username: parsed.username, created_at: parsed.created_at || '' };
          setState({ user, isAuthenticated: true, isLoading: false });
          return;
        }
      }
      setState({ user: null, isAuthenticated: false, isLoading: false });
    } catch {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
      setState({ user: null, isAuthenticated: false, isLoading: false });
    }
  }, []);

  const login = useCallback(async (data: LoginRequest) => {
    const response = await apiLogin(data);
    localStorage.setItem('auth_token', response.token);
    localStorage.setItem('auth_user', JSON.stringify(response.user));
    setState({ user: response.user, isAuthenticated: true, isLoading: false });
  }, []);

  const register = useCallback(async (data: RegisterRequest) => {
    // Register calls the API and returns success without auto-login.
    // User must call login() separately after registration.
    await apiRegister(data);
  }, []);

  const logout = useCallback(async () => {
    // JWT is stateless — just clear local state, no backend call needed
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    setState({ user: null, isAuthenticated: false, isLoading: false });
  }, []);

  return (
    <AuthContext.Provider value={{ ...state, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Hook to access authentication context. Must be used within AuthProvider.
 */
export const useAuthContext = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
};

export { AuthContext };
export default AuthContext;
