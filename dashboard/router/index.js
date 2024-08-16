import { createRouter, createWebHistory } from 'vue-router'
import HomeBaseView from '@/views/HomeBaseView.vue'

const router = createRouter({
  // history: createWebHistory(import.meta.env.BASE_URL),
  history: createWebHistory('dashboard'),
  routes: [
    {
      path: '/',
      name: 'home-base',
      component: HomeBaseView,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'index',
          component: () => import('@/views/IndexView.vue'),
        },
      ],
    },
    {
      path: '/accounts/login',
      name: 'login',
      component: () => import('@/views/accounts/LoginView.vue'),
    },
    {
      path: '/accounts/register',
      name: 'register',
      component: () => import('@/views/accounts/RegisterView.vue'),
    },
    {
      path: '/accounts/logout',
      name: 'logout',
      component: () => import('@/views/accounts/LogoutView.vue'),
    },
  ],
})

router.beforeEach((to, from) => {
  // instead of having to check every route record with
  const loggedInUserData = localStorage.getItem('loggedInUser')
  const isAuthenticated = !!loggedInUserData

  // to.matched.some(record => record.meta.requiresAuth)
  if (to.meta.requiresAuth && !isAuthenticated) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    return {
      path: '/accounts/login',
      // save the location we were at to come back later
      query: { redirect: to.fullPath },
    }
  }
})

export default router
