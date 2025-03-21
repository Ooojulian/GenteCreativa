import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';  // URL base de tu API de Django

const api = axios.create({
    baseURL: API_URL,
});

// Interceptor para añadir el token a todas las peticiones (si existe)
api.interceptors.
