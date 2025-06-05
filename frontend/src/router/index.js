// import Dashboard from '@/views/Dashboard.vue'
import { createRouter, createWebHistory } from 'vue-router'

// Lazy imports
const HomeView = () => import('../views/Home.vue')
const LoginView = () => import('../views/Login.vue')
const RegisterView = () => import('../views/Register.vue')
const IndividualPatientView = () => import('../views/IndividualPatient.vue')
const Dashboard = () => import('../views/Dashboard.vue')
const AdminOverview = () => import('../views/AdminOverview.vue')



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
      path: '/patients/:id',
      name: 'patients',
      component: IndividualPatientView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard
    },
     {
      path: '/adminoverview',
      name: 'adminoverview',
      component: AdminOverview
    }
  ]
})

export default router
