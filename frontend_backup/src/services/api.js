import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';  // URL base de tu API de Django

const api = axios.create({
    baseURL: API_URL,
});

// Interceptor para añadir el token a todas las peticiones (si existe)
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);


// Funciones para interactuar con la API (ejemplos):
export const loginUser = async (credentials) => { // Define un tipo más específico
  try {
    const response = await api.post('/login/', credentials);
    return response.data; // Devuelve los tokens (access y refresh)
  } catch (error) {
     if (axios.isAxiosError(error)) {
      // Accede a la respuesta de error de Axios
      throw error.response?.data || { message: error.message }; //Lanza el error.
    }
    throw error; // Si no es un error de Axios, lo relanza tal cual
  }
};

// Obtiene el listado de pedidos, si es conductor.
export const getPedidos = async () => {
    try {
        const response = await api.get('/transporte/mis_pedidos/');
        return response.data; //Retorna la lista de pedidos.
    } catch (error) {
        if (axios.isAxiosError(error)) {
             throw error.response?.data || { message: error.message };
        }
        throw error;
    }
}

// Función para iniciar un pedido
export const iniciarPedido = async (pedidoId) => {
  try {
      const response = await api.patch(`/transporte/pedidos/${pedidoId}/`, { iniciar: 'confirmado' });
      return response.data;
  } catch (error) {
      if (axios.isAxiosError(error)) {
          throw error.response?.data || { message: error.message };
      }
      throw error;
  }
};

// Función para finalizar un pedido
export const finalizarPedido = async (pedidoId) => {
  try {
      const response = await api.patch(`/transporte/pedidos/${pedidoId}/`, { finalizar: 'confirmado' });
      return response.data;
  } catch (error) {
      if (axios.isAxiosError(error)) {
           throw error.response?.data || { message: error.message };
      }
      throw error;
  }
};

export default api; //Para usar axios en otros lugares, si es necesario.
