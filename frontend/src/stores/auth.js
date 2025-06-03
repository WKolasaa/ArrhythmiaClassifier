import { defineStore } from 'pinia'
import api from '../plugins/axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null
  }),
  actions: {
    async login(email, password) {
      try {
        const response = await api.post('/auth/login', { email, password })
        this.user = response.data.user
        this.token = response.data.token
        localStorage.setItem('token', this.token)
        return true
      } catch (error) {
        console.error('Login failed:', error.response?.data?.message || error.message)
        return false
      }
    },

    async register(email, password, role = 'doctor') {
      try {
        const res = await api.post('/auth/register', { 
            email: email, 
            password: password, role: role })
        console.log('Register response:', res.data)
        return true
      } catch (error) {
        console.error('Register failed:', error.response?.data?.message || error.message)
        return false
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})
