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

//-----  Endpoints de la API  -----

// Login
export const loginUser = async (credentials: any) => { //Se agrega export
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

// Refrescar token
export const refreshToken = async (refresh: string) => { //Se agrega export
    const response = await api.post('/token/refresh/', { refresh });
    return response.data;
};

// Obtener pedidos del conductor
export const getPedidos = async () => { //Se agrega export
  try {
      const response = await api.get('/transporte/mis_pedidos/');
      return response.data;
  } catch (error) {
      if (axios.isAxiosError(error)) {
          throw error.response?.data || { message: error.message };
      }
      throw error;
  }
}

// Función para iniciar un pedido
export const iniciarPedido = async (pedidoId: number) => { //Se agrega export
  try {
    // Paso 1: Obtener la confirmación. No se envia nada en el body
      const response = await api.patch(`/transporte/pedidos/${pedidoId}/`, {});
      //Si el estado es 200, se espera la confirmación.
      if(response.status === 200){
        return response.data; //Devuelve el mensaje de confirmación
      }
      //En caso de que el servidor responda con otro codigo, diferente de 200
      return Promise.reject(response) //Se rechaza la promesa.

  } catch (error) {
      if (axios.isAxiosError(error)) {
          throw error.response?.data || { message: error.message };
      }
      throw error;
  }
};

// Función para finalizar un pedido
export const finalizarPedido = async (pedidoId: number) => { //Se agrega export
  try {
      // Paso 1: Obtener la confirmación
    const response = await api.patch(`/transporte/pedidos/${pedidoId}/`, {});
    if(response.status === 200){
        return response.data; //Devuelve el mensaje de confirmación.
    }
      return Promise.reject(response)

  } catch (error) {
      if (axios.isAxiosError(error)) {
           throw error.response?.data || { message: error.message };
      }
      throw error;
  }
};

export default api; // Añade esta línea
