<template>
  <div class="login-container">
    <div class="login-box">
      <div class="logo">
        <span class="learning-text">LEARNING</span>
        <span class="cms-text">CMS</span>
        <span class="admin-text">ADMIN</span>
      </div>
      <h2 class="subtitle">用户登录</h2>
      
      <form @submit.prevent="handleSubmit" class="login-form">
        <!-- 用户名/邮箱输入框 -->
        <div class="form-group" :class="{ 'has-error': errors.username }">
          <input
            type="text"
            v-model="form.username"
            placeholder="用户名/邮箱"
            class="form-input"
            :disabled="loading"
            @input="validateUsername"
          />
          <span class="error-message" v-if="errors.username">{{ errors.username }}</span>
        </div>

        <!-- 密码输入框 -->
        <div class="form-group" :class="{ 'has-error': errors.password }">
          <div class="password-input">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="form.password"
              placeholder="登录密码"
              class="form-input"
              :disabled="loading"
              @input="validatePassword"
            />
            <button
              type="button"
              class="toggle-password"
              @click="showPassword = !showPassword"
            >
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <span class="error-message" v-if="errors.password">{{ errors.password }}</span>
          <div class="password-strength" v-if="form.password">
            <div class="strength-bar" :class="passwordStrength"></div>
            <span class="strength-text">{{ passwordStrengthText }}</span>
          </div>
        </div>

        <!-- 记住我和忘记密码 -->
        <div class="form-options">
          <label class="remember-me">
            <input
              type="checkbox"
              v-model="form.rememberMe"
              :disabled="loading"
            />
            <span>记住我</span>
          </label>
          <a href="#" class="forgot-password" @click.prevent="handleForgotPassword">忘记密码？</a>
        </div>

        <!-- 登录按钮 -->
        <button
          type="submit"
          class="login-button"
          :disabled="loading || !isFormValid"
        >
          <span v-if="!loading">登录</span>
          <i v-else class="fas fa-spinner fa-spin"></i>
        </button>
      </form>

      <!-- 错误提示 -->
      <div v-if="globalError" class="global-error">
        {{ globalError }}
      </div>

      <div class="third-party-login">
        <p class="login-divider">使用合作账户登录</p>
        <div class="login-methods">
          <a href="#" class="login-method">
            <i class="iconfont icon-qq"></i>
          </a>
          <a href="#" class="login-method">
            <i class="iconfont icon-wechat"></i>
          </a>
          <a href="#" class="login-method">
            <i class="iconfont icon-alipay"></i>
          </a>
        </div>
      </div>
      <div class="register-hint">
        没有账号？<a href="#" class="register-link">去注册</a>
      </div>
    </div>
    <div class="copyright">
      Copyright © Learning CMS Admin
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const form = reactive({
      username: '',
      password: '',
      rememberMe: false
    })

    const errors = reactive({
      username: '',
      password: ''
    })

    const loading = ref(false)
    const showPassword = ref(false)
    const globalError = ref('')

    // 表单验证
    const validateUsername = () => {
      if (!form.username) {
        errors.username = '请输入用户名或邮箱'
      } else if (form.username.includes('@') && !isValidEmail(form.username)) {
        errors.username = '请输入有效的邮箱地址'
      } else {
        errors.username = ''
      }
    }

    const validatePassword = () => {
      if (!form.password) {
        errors.password = '请输入密码'
      } else if (form.password.length < 6) {
        errors.password = '密码长度至少6位'
      } else {
        errors.password = ''
      }
    }

    // 密码强度检查
    const passwordStrength = computed(() => {
      if (!form.password) return ''
      const strength = checkPasswordStrength(form.password)
      return `strength-${strength}`
    })

    const passwordStrengthText = computed(() => {
      if (!form.password) return ''
      const strengthMap = {
        weak: '弱',
        medium: '中',
        strong: '强'
      }
      return strengthMap[checkPasswordStrength(form.password)]
    })

    // 表单提交
    const handleSubmit = async () => {
      validateUsername()
      validatePassword()

      if (!isFormValid.value) return

      loading.value = true
      globalError.value = ''

      try {
        const response = await authStore.login({
          username: form.username,
          password: form.password,
          rememberMe: form.rememberMe
        })

        if (response.error) {
          globalError.value = response.message
        } else {
          router.push('/admin')
        }
      } catch (error) {
        globalError.value = '登录失败，请稍后重试'
        console.error('Login error:', error)
      } finally {
        loading.value = false
      }
    }

    // 辅助函数
    const isValidEmail = (email) => {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
    }

    const checkPasswordStrength = (password) => {
      const hasLetter = /[a-zA-Z]/.test(password)
      const hasNumber = /\d/.test(password)
      const hasSpecial = /[!@#$%^&*]/.test(password)
      
      if (password.length < 6) return 'weak'
      if (hasLetter && hasNumber && hasSpecial) return 'strong'
      if ((hasLetter && hasNumber) || (hasLetter && hasSpecial) || (hasNumber && hasSpecial)) return 'medium'
      return 'weak'
    }

    const isFormValid = computed(() => {
      return !errors.username && !errors.password && form.username && form.password
    })

    const handleForgotPassword = () => {
      // 实现忘记密码逻辑
      console.log('Forgot password clicked')
    }

    return {
      form,
      errors,
      loading,
      showPassword,
      globalError,
      passwordStrength,
      passwordStrengthText,
      isFormValid,
      handleSubmit,
      validateUsername,
      validatePassword,
      handleForgotPassword
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  padding: 20px;
}

.login-box {
  background: white;
  padding: 30px;
  border-radius: 4px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  gap: 5px;
}

.learning-text {
  color: #2196f3;
}

.cms-text {
  color: #42a5f5;
}

.admin-text {
  color: #ffc107;
}

.subtitle {
  text-align: center;
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #2196f3;
  outline: none;
}

.options-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  font-size: 14px;
}

.remember-label {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #666;
}

.forgot-link {
  color: #2196f3;
  text-decoration: none;
}

.login-button {
  width: 100%;
  padding: 12px;
  background: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background: #1976d2;
}

.third-party-login {
  margin-top: 30px;
  text-align: center;
}

.login-divider {
  color: #999;
  font-size: 14px;
  margin-bottom: 15px;
}

.login-methods {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.login-method {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f5f5f5;
  color: #666;
  text-decoration: none;
  font-size: 12px;
  transition: background-color 0.3s;
}

.login-method:hover {
  background: #e0e0e0;
}

.login-method.qq:hover {
  color: #12B7F5;
}

.login-method.wechat:hover {
  color: #07C160;
}

.login-method.alipay:hover {
  color: #1677FF;
}

.register-hint {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #666;
}

.register-link {
  color: #2196f3;
  text-decoration: none;
}

.copyright {
  margin-top: 20px;
  color: white;
  font-size: 14px;
  text-align: center;
}

.iconfont {
  font-size: 20px;
}

.icon-qq {
  color: #12B7F5;
}

.icon-wechat {
  color: #07C160;
}

.icon-alipay {
  color: #1677FF;
}

.password-input {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
}

.password-strength {
  margin-top: 5px;
}

.strength-bar {
  height: 4px;
  border-radius: 2px;
  margin-bottom: 5px;
}

.strength-weak {
  background: #f44336;
  width: 30%;
}

.strength-medium {
  background: #ffc107;
  width: 60%;
}

.strength-strong {
  background: #4caf50;
  width: 100%;
}

.strength-text {
  font-size: 12px;
  color: #666;
}

.has-error .form-input {
  border-color: #f44336;
}

.error-message {
  color: #f44336;
  font-size: 12px;
  margin-top: 5px;
}

.global-error {
  margin-top: 20px;
  padding: 10px;
  background: #ffebee;
  color: #f44336;
  border-radius: 4px;
  text-align: center;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 15px 0;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #666;
}

.forgot-password {
  color: #2196f3;
  text-decoration: none;
}

.login-button {
  position: relative;
  width: 100%;
}

.login-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.fa-spinner {
  animation: spin 1s linear infinite;
}
</style> 