import Vue from 'vue';
import Router from 'vue-router';
import home from '@/components/home';
import login from '@/components/login';
import register from '@/components/register';

Vue.use(Router);
export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
    },
    {
      path: '/register',
      name: 'register',
      component: register
    },
    {
      path: '/login',
      name: 'login',
      component: login
    }
  ]
});
