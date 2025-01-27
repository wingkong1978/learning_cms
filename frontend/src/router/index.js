import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import SearchView from '../views/SearchView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'  // 将根路径重定向到登录页
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/admin',  // 添加管理后台路由
      name: 'admin',
      component: () => import('../views/AdminView.vue'),  // 懒加载管理后台页面
      meta: { requiresAuth: true }  // 需要登录才能访问
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 如果页面需要登录验证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查是否已登录
    const isLoggedIn = localStorage.getItem('token')  // 假设使用 token 存储登录状态
    if (!isLoggedIn) {
      // 未登录则跳转到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }  // 保存原目标路径
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router 