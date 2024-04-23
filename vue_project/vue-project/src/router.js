import { createRouter, createWebHistory } from "vue-router";
import application from "./components/application.vue";
import general from "./components/general.vue";
import application2 from "./components/application2.vue";
import authorization from "./components/authorization.vue";
import registration from "./components/registration.vue";

export default createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: general, alias: '/' },
        { path: '/create', component: application },
        { path: '/send', component: application2 },
        { path: '/auth', component: authorization},
        { path: '/regist', component: registration}
    ]
})




