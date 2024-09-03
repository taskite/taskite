import { createRouter, createWebHistory } from 'vue-router'
import HomeBaseView from '@/views/HomeBaseView.vue'


const router = createRouter({
  // history: createWebHistory(import.meta.env.BASE_URL),
  history: createWebHistory('dashboard'),
  routes: [
    {
      path: '/boards/:boardId',
      component: () => import('@/views/BoardBaseView.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'boards-detail',
          component: () => import('@/views/boards/IndexView.vue'),
        },
        {
          path: 'members',
          name: 'members',
          component: () => import('@/views/members/IndexView.vue'),
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('@/views/boards/SettingsBaseView.vue'),
          children: [
            {
              path: '',
              name: 'settings-general',
              component: () => import('@/views/boards/settings/IndexView.vue'),
            },
          ],
        },
      ],
    },
    {
      path: '/',
      component: HomeBaseView,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'home-index',
          component: () => import('@/views/HomeView.vue'),
        },
        {
          path: 'workspaces/:workspaceId',
          component: () => import('@/views/WorkspaceBaseView.vue'),
          meta: { requiresAuth: true },
          children: [
            {
              path: 'general',
              name: 'workspace-general',
              component: () => import('@/views/workspaces/GeneralView.vue'),
            },
            {
              path: 'members',
              name: 'workspace-members',
              component: () => import('@/views/workspaces/MembersView.vue'),
            },
            {
              path: 'teams',
              name: 'workspace-teams',
              component: () => import('@/views/workspaces/TeamsView.vue'),
            },
            {
              path: 'notifications',
              name: 'workspace-notifications',
              component: () =>
                import('@/views/workspaces/NotificationsView.vue'),
            },
            {
              path: 'billing',
              name: 'workspace-billing',
              component: () => import('@/views/workspaces/BillingView.vue'),
            },
            {
              path: 'advance',
              name: 'workspace-advance',
              component: () => import('@/views/workspaces/AdvanceView.vue'),
            },
          ],
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
    // {
    //   path: '/accounts/verify',
    //   name: 'account-verify',
    //   component: () => import('@/views/accounts/VerifyView.vue'),
    //   // meta: { requiresAuth: true, allowUnverified: true },
    // },
  ],
})

router.beforeEach((to, from) => {
  // instead of having to check every route record with
  const loggedInUserData = localStorage.getItem('loggedInUser')
  const isAuthenticated = !!loggedInUserData

  // to.matched.some(record => record.meta.requiresAuth)
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      // this route requires auth, check if logged in
      // if not, redirect to login page.
      return {
        path: '/accounts/login',
        // save the location we were at to come back later
        query: { redirect: to.fullPath },
      }
    }
  }
})

export default router
