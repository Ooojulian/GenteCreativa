import React, { createContext, useState, useEffect, ReactNode, useContext } from 'react';
import  api  from '../services/api';

interface AuthContextProps {
  token: string | null;
  user: any; // Cambia 'any' por un tipo más específico si tienes la interfaz del usuario
  login: (token: string, userData: any) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

// Valor inicial (placeholders) para el contexto.  'navigate' ahora es una función vacía.
const AuthContext = createContext<AuthContextProps>({
  token: null,
  user: null,
  login: () => {},
  logout: () => {},
  isAuthenticated: false,
});

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<any>(null); // Cambia 'any' por un tipo más específico
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }
  }, []);

    useEffect(() => {
    if (token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        setIsAuthenticated(true);

    } else {
        delete api.defaults.headers.common['Authorization'];
         setIsAuthenticated(false);
    }
  }, [token]);


  const login = (newToken: string, userData: any) => {
    setToken(newToken);
    setUser(userData);
    localStorage.setItem('token', newToken);
    localStorage.setItem('user', JSON.stringify(userData));
    // navigate('/dashboard'); // Redirige al dashboard después del login. ¡Ya no aquí!
    setIsAuthenticated(true);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user'); //Limpia user
    // navigate('/login'); // ¡Ya no aquí!
    setIsAuthenticated(false);
  };

  return (
    // Pasa 'navigate' como parte del contexto:
    <AuthContext.Provider value={{ token, user, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};


// Hook personalizado para usar el contexto
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};