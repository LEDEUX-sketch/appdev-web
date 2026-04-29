import { defineStore } from 'pinia';
import axios from '../axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')) || null,
        token: localStorage.getItem('access_token') || null,
        refreshToken: localStorage.getItem('refresh_token') || null,
        loading: false,
        error: null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
    },
    actions: {
        async login(username, password) {
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.post('auth/login/', { username, password });
                
                this.token = response.data.access;
                this.refreshToken = response.data.refresh;
                this.user = { username }; 
                
                localStorage.setItem('access_token', this.token);
                localStorage.setItem('refresh_token', this.refreshToken);
                localStorage.setItem('user', JSON.stringify(this.user));
                
                return true;
            } catch (err) {
                this.error = err.response?.data?.detail || 'Login failed. Please check your credentials.';
                return false;
            } finally {
                this.loading = false;
            }
        },
        
        async refreshAccessToken() {
            if (!this.refreshToken) return null;
            
            try {
                const response = await axios.post('auth/token/refresh/', {
                    refresh: this.refreshToken
                }, { _retry: true }); // Prevent infinite loop
                
                this.token = response.data.access;
                localStorage.setItem('access_token', this.token);
                return this.token;
            } catch (err) {
                this.logout();
                return null;
            }
        },

        logout() {
            this.token = null;
            this.refreshToken = null;
            this.user = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }
    }
});
