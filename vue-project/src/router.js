import { createRouter, createWebHistory } from "vue-router";
import create_tender from "./components/create_tender.vue";
import main_page from "./components/main_page.vue";
import response from "./components/response.vue";
import profile from "./components/profile.vue"
import mytenders from "./components/mytenders.vue";
import myresponse from "./components/myresponse.vue";
import authorization from "./components/authorization.vue";
import registration from "./components/registration.vue";
import participants from "./components/participants.vue";


export default createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: main_page, alias: '/' },
        { path: '/create', component: create_tender },
        { path: '/send', component: response },
        { path: '/profile', component: profile },
        { path: '/mytenders', component: mytenders },
        { path: '/myresponse', component: myresponse },
        { path: '/auth', component: authorization},
        { path: '/regist', component: registration},
        { path: '/participants', component: participants}
    ]
})