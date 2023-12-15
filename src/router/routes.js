import axios from 'axios'
import { LocalStorage } from 'quasar'
const routes = [
  {
    path: '/',
    component: () => import('pages/LandingPage'),
  },
  {
    path: '/Register',
    component: () => import('pages/Register'),
  },
  {
    path: '/PostRegister',
    component: () => import('pages/PostRegister'),
  },
  {
    path: '/RequireAuth',
    component: () => import('pages/RequireAuth')
  },
  {
    path: '/Admin',
    component: () => import('src/layouts/AdminLayout.vue'),
    children: [
      { path: 'Default', component: () => import('pages/AdminDefault.vue')},
      { path: 'Listings', component: () => import('src/pages/AdminAddListing.vue')},
      { path: 'Sales', component: () => import('pages/AdminSales.vue')},
      { path: 'Profile', component: () => import('pages/AdminProfile.vue')},
      { name: 'EditItem', path: 'EditItem/:itemId', component: () => import('pages/AdminEditListing.vue'), props: true},
      
    ],
    async beforeEnter(to, from, next) {
      let token = LocalStorage.getItem('token')
      LocalStorage.set('navigatingTo', to.fullPath)
      await axios.get('/admin/check_token', { params: 
        {
          token: token
        }}).then( res => {
        if (res.data == false) {
          next('/RequireAuth')
        } else {
          next()
        }
      })

    }
  },
  {
    path: '/User',
    component: () => import('src/layouts/UserLayout.vue'),
    children: [
      { path: 'Default', component: () => import('pages/UserDefault.vue')},
      { path: 'Profile', component: () => import('pages/UserProfile.vue')},
      { name: 'PostSearch', path: 'PostSearch/:type/:query', component: () => import('src/pages/UserPostSearch.vue'), props: true},
      { path: 'Cart', component: () => import('pages/UserCart.vue')},
      { path: 'PostPurchase', component: () => import('src/pages/UserPostPurchase.vue')},
      { name: 'Item', path: 'Item/:itemId', component: () => import('src/pages/UserItem.vue'), props: true},
    ],
    async beforeEnter(to, from, next) {
      let token = LocalStorage.getItem('token')
      LocalStorage.set('navigatingTo', to.fullPath)
      await axios.get('/user/check_token', { params: {
        token: token
      }}).then( res => {
        if (res.data == false) {
          next('/RequireAuth')
        } else {
          next()
        }
      })
    }
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
