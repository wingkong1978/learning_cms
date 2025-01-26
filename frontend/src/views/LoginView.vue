<template>
  <div class="login-container">
    <div class="login-box">
      <div class="logo">
        <span class="learning-text">LEARNING</span>
        <span class="cms-text">CMS</span>
        <span class="admin-text">ADMIN</span>
      </div>
      <h2 class="subtitle">用户登录</h2>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <input
            type="text"
            v-model="username"
            placeholder="用户名/邮箱/手机号"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <input
            type="password"
            v-model="password"
            placeholder="登录密码"
            class="form-input"
          />
        </div>
        <div class="options-row">
          <label class="remember-label">
            <input type="checkbox" v-model="remember" />
            <span>记住登录信息</span>
          </label>
          <a href="#" class="forgot-link">忘记密码?</a>
        </div>
        <button type="submit" class="login-button">登录</button>
      </form>
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
export default {
  data() {
    return {
      username: '',
      password: '',
      remember: false
    }
  },
  methods: {
    async login() {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        })
        const data = await response.json()
        if (response.ok) {
          this.$router.push('/')
        } else {
          alert(data.error || '登录失败')
        }
      } catch (error) {
        alert('连接服务器失败')
      }
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
</style> 