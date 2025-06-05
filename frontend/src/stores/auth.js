import { defineStore } from 'pinia'
import api from '../plugins/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null
  }),

  actions: {
    async login(email, password) {
      try {
        const response = await api.post('/auth/login', { email, password })
        this.user = response.data.user
        this.token = response.data.token

        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))

        return true
      } catch (error) {
        console.error('Login failed:', error.response?.data?.message || error.message)
        return false
      }
    },

    async register(email, password, role = 'doctor') {
      try {
        const res = await api.post('/auth/register', {
          email,
          password,
          role
        })
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
      localStorage.removeItem('user')
    }
  }
})
