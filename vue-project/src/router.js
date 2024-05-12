import { createRouter, createWebHistory } from 'vue-router';
import axios from 'axios';

import MainPage from './components/main_page.vue';
import CreateTender from './components/create_tender.vue';
import Profile from './components/profile.vue';
import MyTenders from './components/mytenders.vue';
import MyResponse from './components/myresponse.vue';
import Authorization from './components/authorization.vue';
import Registration from './components/registration.vue';
import Tender from './components/tender.vue';
import Forbidden from './components/forbidden.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: MainPage, alias: '/' },
    { path: '/create', component: CreateTender },
    { path: '/forbidden', component: Forbidden },
    { path: '/profile', component: Profile },
    { path: '/mytenders', component: MyTenders },
    { path: '/myresponse', component: MyResponse },
    { path: '/auth', component: Authorization},
    { path: '/regist', component: Registration},
    { path: '/tender/:id', component: Tender, props: true },
  ]
});

router.beforeEach(async (to, from, next) => {
  try {
    const response = await axios.get('/update_tender_status');
    // Обработайте ответ сервера, если необходимо
    next();
  } catch (error) {
    // Обработайте ошибку, если она возникла
    next();
  }
});

export default router;
