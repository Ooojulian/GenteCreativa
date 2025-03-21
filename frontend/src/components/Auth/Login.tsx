import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Importa useNavigate
import { useAuth } from '../../context/AuthContext';
import { loginUser } from '../../services/api';

const Login: React.FC = () => {
  const [password, setPassword] = useState('');
  const [cedula, setCedula] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      setError('');

      try {
          let credentials = { cedula, password };

          const data = await loginUser(credentials);
          login(data.access, data.user);
          navigate('/dashboard');
      } catch (error: any) {
            setError(error.message || 'Error al iniciar sesión');
            console.error("Error en el login:", error);
      }
  };

  return (
      <div>
          <h2>Iniciar Sesión</h2>
          <form onSubmit={handleSubmit}>
              <div>
                    <label htmlFor="cedula">Cédula:</label>
                    <input
                        type="text"
                        id="cedula"
                        value={cedula}
                        onChange={(e) => setCedula(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Contraseña:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
              <button type="submit">Iniciar Sesión</button>
              {error && <p style={{ color: 'red' }}>{error}</p>}
          </form>
      </div>
  );
}

export default Login;