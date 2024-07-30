import Vue from 'vue'
import Router from 'vue-router'
import Main from '../components/main.vue'
import Picture from "../components/picture.vue"
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
   {
    path:'/kg',
    name:'Picture',
    component: Picture
  },
]

const router = new Router({
  mode:"history",
  routes
})

export default router