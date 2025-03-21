import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Ajusta esto a tu URL base
});

// Interceptor para incluir el token en cada petición
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

export const loginUser = async (credentials: any) => {
  try {
    const response = await api.post('/login/', credentials); //Asegurate de tener esta ruta en tu backend
    return response.data; // Devuelve los tokens (access y refresh)
  } catch (error) {
    console.error("Error en loginUser:", error); // Imprime el error en la consola
    if (axios.isAxiosError(error)) {
      // Accede a la respuesta de error de Axios *si existe*
      throw error.response?.data || { message: error.message };
    }
    throw error; // Si no es un error de Axios, lo relanza tal cual
  }
};

export const getPedidos = async () => {
    const response = await api.get('/pedidos/'); //Protegido, por token
    return response.data;
};

export const iniciarPedido = async (pedidoId: number) => {
  const response = await api.put(`/pedidos/${pedidoId}/iniciar/`); //Protegido
  return response.data;
};

export const finalizarPedido = async (pedidoId: number) => {
  const response = await api.put(`/pedidos/${pedidoId}/finalizar/`);  //Protegido
  return response.data;
};


export default api;