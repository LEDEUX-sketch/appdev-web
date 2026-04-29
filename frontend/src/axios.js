import axios from 'axios';

const getBaseURL = () => {
    let url = import.meta.env.VITE_API_URL || 'https://soavs-backend.onrender.com/api/';
    if (!url.endsWith('/')) url += '/';
    if (!url.includes('/api/')) url += 'api/';
    return url;
};

const instance = axios.create({
    baseURL: getBaseURL(),
    timeout: 10000,
});

// Add a request interceptor to include the JWT token
instance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token && !config._retry) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add a response interceptor to handle token expiration and auto-refresh
instance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If error is 401 and we haven't retried yet
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            
            // If it's already the login or refresh endpoint, just logout
            if (originalRequest.url.includes('auth/login/') || originalRequest.url.includes('auth/token/refresh/')) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
                if (window.location.pathname !== '/login') {
                    window.location.href = '/login';
                }
                return Promise.reject(error);
            }

            originalRequest._retry = true;
            const refreshToken = localStorage.getItem('refresh_token');

            if (refreshToken) {
                try {
                    // Try to get a new access token
                    const response = await axios.post(`${instance.defaults.baseURL}auth/token/refresh/`, {
                        refresh: refreshToken
                    });

                    const newToken = response.data.access;
                    localStorage.setItem('access_token', newToken);

                    // Retry the original request with the new token
                    originalRequest.headers.Authorization = `Bearer ${newToken}`;
                    return instance(originalRequest);
                } catch (refreshError) {
                    // Refresh token is also invalid
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    localStorage.removeItem('user');
                    window.location.href = '/login';
                    return Promise.reject(refreshError);
                }
            }
        }

        return Promise.reject(error);
    }
);

export default instance;
