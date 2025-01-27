<template>
  <div class="register-container">
    <div class="register-box">
      <div class="logo">
        <span class="learning-text">LEARNING</span>
        <span class="cms-text">CMS</span>
        <span class="admin-text">ADMIN</span>
      </div>
      <h2 class="subtitle">用户注册</h2>

      <form @submit.prevent="handleSubmit" class="register-form">
        <!-- 用户名输入框 -->
        <div class="form-group" :class="{ 'has-error': errors.username }">
          <input
            type="text"
            v-model="form.username"
            placeholder="用户名"
            class="form-input"
            :disabled="loading"
            @input="validateUsername"
            @blur="checkUsernameAvailability"
          />
          <span class="error-message" v-if="errors.username">{{ errors.username }}</span>
          <span class="success-message" v-if="usernameAvailable">用户名可用</span>
        </div>

        <!-- 邮箱输入框 -->
        <div class="form-group" :class="{ 'has-error': errors.email }">
          <input
            type="email"
            v-model="form.email"
            placeholder="邮箱地址"
            class="form-input"
            :disabled="loading"
            @input="validateEmail"
            @blur="checkEmailAvailability"
          />
          <span class="error-message" v-if="errors.email">{{ errors.email }}</span>
        </div>

        <!-- 密码输入框 -->
        <div class="form-group" :class="{ 'has-error': errors.password }">
          <div class="password-input">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="form.password"
              placeholder="设置密码"
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

        <!-- 确认密码输入框 -->
        <div class="form-group" :class="{ 'has-error': errors.confirmPassword }">
          <div class="password-input">
            <input
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="form.confirmPassword"
              placeholder="确认密码"
              class="form-input"
              :disabled="loading"
              @input="validateConfirmPassword"
            />
            <button
              type="button"
              class="toggle-password"
              @click="showConfirmPassword = !showConfirmPassword"
            >
              <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <span class="error-message" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
        </div>

        <!-- 注册按钮 -->
        <button
          type="submit"
          class="register-button"
          :disabled="loading || !isFormValid"
        >
          <span v-if="!loading">注册</span>
          <i v-else class="fas fa-spinner fa-spin"></i>
        </button>
      </form>

      <!-- 错误提示 -->
      <div v-if="globalError" class="global-error">
        {{ globalError }}
      </div>

      <div class="login-hint">
        已有账号？<a href="#" @click.prevent="goToLogin" class="login-link">去登录</a>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import debounce from 'lodash/debounce'

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const form = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const errors = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const loading = ref(false)
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    const globalError = ref('')
    const usernameAvailable = ref(false)

    // 用户名验证
    const validateUsername = () => {
      if (!form.username) {
        errors.username = '请输入用户名'
      } else if (form.username.length < 3) {
        errors.username = '用户名至少3个字符'
      } else if (!/^[a-zA-Z0-9_]+$/.test(form.username)) {
        errors.username = '用户名只能包含字母、数字和下划线'
      } else {
        errors.username = ''
      }
    }

    // 检查用户名可用性
    const checkUsernameAvailability = debounce(async () => {
      if (!form.username || errors.username) return

      try {
        const response = await fetch(`/api/auth/check-username?username=${form.username}`)
        const data = await response.json()
        usernameAvailable.value = data.available
        if (!data.available) {
          errors.username = '该用户名已被使用'
        }
      } catch (error) {
        console.error('检查用户名失败:', error)
      }
    }, 500)

    // 邮箱验证
    const validateEmail = () => {
      if (!form.email) {
        errors.email = '请输入邮箱地址'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
        errors.email = '请输入有效的邮箱地址'
      } else {
        errors.email = ''
      }
    }

    // 检查邮箱可用性
    const checkEmailAvailability = debounce(async () => {
      if (!form.email || errors.email) return

      try {
        const response = await fetch(`/api/auth/check-email?email=${form.email}`)
        const data = await response.json()
        if (!data.available) {
          errors.email = '该邮箱已被注册'
        }
      } catch (error) {
        console.error('检查邮箱失败:', error)
      }
    }, 500)

    // 密码验证和强度检查
    const validatePassword = () => {
      if (!form.password) {
        errors.password = '请输入密码'
      } else if (form.password.length < 8) {
        errors.password = '密码至少8个字符'
      } else {
        errors.password = ''
      }
      validateConfirmPassword()
    }

    const validateConfirmPassword = () => {
      if (!form.confirmPassword) {
        errors.confirmPassword = '请确认密码'
      } else if (form.confirmPassword !== form.password) {
        errors.confirmPassword = '两次输入的密码不一致'
      } else {
        errors.confirmPassword = ''
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

    const checkPasswordStrength = (password) => {
      const hasLetter = /[a-zA-Z]/.test(password)
      const hasNumber = /\d/.test(password)
      const hasSpecial = /[!@#$%^&*]/.test(password)
      
      if (password.length < 8) return 'weak'
      if (hasLetter && hasNumber && hasSpecial) return 'strong'
      if ((hasLetter && hasNumber) || (hasLetter && hasSpecial) || (hasNumber && hasSpecial)) return 'medium'
      return 'weak'
    }

    // 表单提交
    const handleSubmit = async () => {
      validateUsername()
      validateEmail()
      validatePassword()
      validateConfirmPassword()

      if (!isFormValid.value) return

      loading.value = true
      globalError.value = ''

      try {
        const response = await authStore.register({
          username: form.username,
          email: form.email,
          password: form.password
        })

        if (response.error) {
          globalError.value = response.message
        } else {
          router.push('/login')
        }
      } catch (error) {
        globalError.value = '注册失败，请稍后重试'
        console.error('Register error:', error)
      } finally {
        loading.value = false
      }
    }

    const isFormValid = computed(() => {
      return !errors.username && !errors.email && !errors.password && !errors.confirmPassword &&
             form.username && form.email && form.password && form.confirmPassword
    })

    const goToLogin = () => {
      router.push('/login')
    }

    return {
      form,
      errors,
      loading,
      showPassword,
      showConfirmPassword,
      globalError,
      usernameAvailable,
      passwordStrength,
      passwordStrengthText,
      isFormValid,
      handleSubmit,
      validateUsername,
      validateEmail,
      validatePassword,
      validateConfirmPassword,
      checkUsernameAvailability,
      checkEmailAvailability,
      goToLogin
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  padding: 20px;
}

.register-box {
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* 复用 LoginView 的样式 */
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

.register-button {
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

.register-button:hover {
  background: #1976d2;
}

.register-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #f44336;
  font-size: 12px;
  margin-top: 5px;
}

.success-message {
  color: #4caf50;
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

.login-hint {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #666;
}

.login-link {
  color: #2196f3;
  text-decoration: none;
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

@keyframes spin {
  to { transform: rotate(360deg); }
}

.fa-spinner {
  animation: spin 1s linear infinite;
}
</style> 