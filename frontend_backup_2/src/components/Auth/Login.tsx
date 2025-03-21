import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext'; // Importa useAuth
import { loginUser } from '../../services/api';

const Login: React.FC = () => { //Usamos interface en componentes funcionales
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [cedula, setCedula] = useState(''); // Añade estado para la cédula
  const [isConductorCliente, setIsConductorCliente] = useState(false); // Estado para el tipo de usuario.
  const [error, setError] = useState('');
  const { login } = useAuth(); // Obtiene la función login del contexto.
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => { //Usamos el tipo correcto
    e.preventDefault();
    setError(''); //Limpia errores

    try {
        let credentials;
        //Si el checkbox esta marcado, credenciales = cedula
        if (isConductorCliente) {
            if (!cedula) {
                setError('La cédula es obligatoria.');
                return;
            }
            credentials = { cedula };
        } else { //Si no esta marcado
            if (!email || !password) {
                setError('El email y la contraseña son obligatorios.');
                return;
            }
            credentials = { email, password };
        }

        const data = await loginUser(credentials);
        // Guarda el token y la información del usuario (si es necesario)
        login(data.access, { email: credentials.email, rol: '...' });  // Ajusta según la respuesta real de tu API.
        navigate('/dashboard');

    } catch (error:any) { //Usa any
      setError(error.message || 'Error al iniciar sesión');
      console.error("Error en el login:", error);
      console.log(error.response.data) // <-- Imprime la respuesta completa del error.
    }
};

    return (
        <div>
            <h2>Iniciar Sesión</h2>
            <form onSubmit={handleSubmit}>
                <div>
                   <label>
                    <input
                        type="checkbox"
                        checked={isConductorCliente}
                        onChange={() => setIsConductorCliente(!isConductorCliente)}
                    />
                    Soy Conductor/Cliente
                   </label>
                </div>

                {isConductorCliente ? (
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
                ) : (
                    <>
                        <div>
                            <label htmlFor="email">Email:</label>
                            <input
                                type="email"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
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
                    </>
                )}

                <button type="submit">Iniciar Sesión</button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>
        </div>
    );
}

export default Login;
