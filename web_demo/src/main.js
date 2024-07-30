import Vue from 'vue'
import router from './router'
import App from './App.vue'
import ElementUI from 'element-ui';

import 'mavon-editor/dist/css/index.css'
import 'element-ui/lib/theme-chalk/index.css';
import store from './store'

Vue.config.productionTip = false
Vue.use(ElementUI);


new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
