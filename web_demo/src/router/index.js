import Vue from 'vue'
import Router from 'vue-router'
import Main from '../components/main.vue'
Vue.use(Router)

const routes = [
  {
    path:"/",
    redirect:'/chat'
  },
  {
    path:"/chat",
    name:"Main",
    component:Main
  },
  {
    path: '/chat/:talk_id',
    name: 'Main',
    component: Main
  },
]

const router = new Router({
  mode:"history",
  routes
})

export default router