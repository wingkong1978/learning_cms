import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    refreshToken: null,
    loading: false,
    error: null
  }),

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null

      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(credentials)
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.message || '登录失败')
        }

        this.user = data.user
        this.token = data.token
        this.refreshToken = data.refreshToken

        // 存储 token
        if (credentials.rememberMe) {
          localStorage.setItem('token', data.token)
          localStorage.setItem('refreshToken', data.refreshToken)
        } else {
          sessionStorage.setItem('token', data.token)
          sessionStorage.setItem('refreshToken', data.refreshToken)
        }

        return { success: true }
      } catch (error) {
        this.error = error.message
        return { error: true, message: error.message }
      } finally {
        this.loading = false
      }
    },

    async logout() {
      this.user = null
      this.token = null
      this.refreshToken = null
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('refreshToken')
    },

    async refreshAccessToken() {
      try {
        const response = await fetch('/api/auth/refresh', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            refreshToken: this.refreshToken
          })
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.message)
        }

        this.token = data.token
        return data.token
      } catch (error) {
        this.logout()
        throw error
      }
    },

    async register(userData) {
      this.loading = true
      this.error = null

      try {
        const response = await fetch('/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(userData)
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.message || '注册失败')
        }

        return { success: true, message: '注册成功' }
      } catch (error) {
        this.error = error.message
        return { error: true, message: error.message }
      } finally {
        this.loading = false
      }
    }
  }
}) 