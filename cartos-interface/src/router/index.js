import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err);
}

const routes = [
  {
    path: '/',
    redirect : `/home`
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/admin',
    redirect : `/login`
  },
  {
    path: '/registo',
    name: 'Registo',
    component: () => import('../views/Registo.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/resultados',
    name: 'resultados',
    component: () => import('../views/Resultados.vue')
  },
  {
    path: '/users/ver',
    name: 'Perfil',
    component: () => import('../views/Perfil.vue'),
    beforeEnter (to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`)
      } else {
        next()
      }
    }
  },
  {
    path: '/error404',
    name: 'error404',
    component: () => import('../views/NotFound.vue'),
  },
  {
    path: '/error401',
    name: 'error401',
    component: () => import('../views/Unauthorized.vue'),
  },
  {
    path: '/admin',
    component: {
      render(c) { 
        return c('router-view')
      }
    },
    beforeEnter (to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`)
      }
      else if (!store.getters.isAdmin) {
        next(`/error401`)
      }
      else {
        next()
      }
    },
    children:[
      {
        path: 'users',
        name: 'Utilizadores',
        component: () => import('../views/Utilizadores.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'elementos',
        name: 'Elementos',
        component: () => import('../views/Elementos.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'importCSV',
        name: 'importCSV',
       component: () => import('../views/ImportCSV.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'about',
        name: 'Acerca',
        component: () => import('../views/About.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'import',
        name: 'Import',
        component: () => import('../views/Import.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'analise',
        name: 'Analise',
        component: () => import('../views/AnáliseAdmin.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'resultados',
        name: 'AdminResultados',
        component: () => import('../views/ResultadosAdmin.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'homeAdmin',
        name: 'HomeAdmin',
        component: () => import('../views/HomeAdmin.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'histAcesso',
        name: 'HistorialAcesso',
        component: () => import('../views/HistorialAcesso.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'pesquisas',
        name: 'PesquisasRealizadas',
        component: () => import('../views/PesquisasRealizadas.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'uAtivos',
        name: 'UtilizadoresAtivos',
        component: () => import('../views/UtilizadoresAtivos.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
    ]
  },

  /* ---------------------------------------------------------------------- */ 
  /* ------------------------------- LEITOR ------------------------------- */ 
  /* ---------------------------------------------------------------------- */ 

  {
    path: '/leitor',
    component: {
      render(c) { 
        return c('router-view')
      }
    },
    beforeEnter (to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`)
      }
      else if (store.getters.isAdmin) {
        next(`/error401`)
      }
      else {
        next()
      }
    },
    children:[
      {
        path: 'elementos',
        name: 'ElementosLeitor',
        component: () => import('../views/Elementos.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'about',
        name: 'AcercaLeitor',
        component: () => import('../views/About.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'import',
        name: 'ImportLeitor',
        component: () => import('../views/Import.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'analise',
        name: 'AnaliseLeitor',
        component: () => import('../views/AnáliseAdmin.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'resultados',
        name: 'AdminResultadosLeitor',
        component: () => import('../views/ResultadosAdmin.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'pesquisas',
        name: 'PesquisasRealizadasLeitor',
        component: () => import('../views/PesquisasRealizadas.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else {
            next()
          }
        }
      },
    ]
  },
  { 
    path: "*", 
    component: () => import('../views/NotFound.vue'),
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
