import { createRouter, createWebHistory } from 'vue-router'

// Lazy imports
const HomeView = () => import('../views/Home.vue')
const LoginView = () => import('../views/Login.vue')
const RegisterView = () => import('../views/Register.vue')
const DashboardView = () => import('../views/Dashboard.vue')


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
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
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    }
  ]
})

export default router
