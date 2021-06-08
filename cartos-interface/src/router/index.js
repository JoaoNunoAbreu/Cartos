import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'
import * as VueGoogleMaps from 'vue2-google-maps'



Vue.use(VueRouter)

Vue.use(
  VueGoogleMaps, {
    load: {
      key: 'AIzaSyAP-__9IVdlFFWVjAwMAlj91Bg-Aq-hUKQ'
    }
  }
)

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
    redirect : `/admin/login`
  },
  {
    path: '/admin',
    redirect : `/admin/login`
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
    path: '/admin',
    component: {
      render(c) { return c('router-view')}
    },
    children:[
      {
        path: 'login',
        name: 'Login',
        component: () => import('../views/Login.vue')
      },
      {
        path: 'registo',
        name: 'Registo',
        component: () => import('../views/Registo.vue')
      },
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
        path: 'users/ver',
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
        path: 'elementos/indices',
        name: 'Indices',
        component: () => import('../views/Indices.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'elementos/tags',
        name: 'Tags',
        component: () => import('../views/Definitions.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging',
        name: 'ListaElementos',
        component: () => import('../views/tagging/ListaElementos.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/editor',
        name: 'Editor',
        component: () => import('../views/tagging/Editor.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/modernizador',
        name: 'Atualiza',
        component: () => import('../views/tagging/Atualiza.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/elementoAnotado/ver/:id',
        name: 'VerElemento',
        component: () => import('../views/tagging/VerElemento.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/elementoAtualizado/ver/:id',
        name: 'VerAtualizado',
        component: () => import('../views/tagging/VerAtualizado.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/tags/dicionario',
        name: 'DicionarioTags',
        component: () => import('../views/tagging/DicionarioTags.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/anotaBase',
        name: 'AnotaBase',
        component: () => import('../views/tagging/AnotaBase.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/tags/lista',
        name: 'ListaTags',
        component: () => import('../views/tagging/ListaTags.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/regras/lista',
        name: 'ListaRegras',
        component: () => import('../views/tagging/ListaRegras.vue'),
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
        path: 'definitions',
        name: 'Definições',
        component: () => import('../views/Definitions.vue'),
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
        path: 'compElementos',
        name: 'CompElementos',
        component: () => import('../views/CompElementos.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'documentacao',
        name: 'Documentação',
        component: () => import('../views/Documentacao.vue'),
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
      {
        path: 'localidades',
        name: 'Places',
        component: () => import('../views/PlaceList.vue'),
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
      }
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
