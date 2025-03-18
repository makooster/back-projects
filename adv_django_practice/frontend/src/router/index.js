import Vue from 'vue';
import VueRouter from 'vue-router';
import UserLogin from '../views/UserLogin.vue';
import AdminPage from '../views/AdminPage.vue';
import UserRegister from '../views/UserRegister.vue';
import store from '../store';

Vue.use(VueRouter);

const routes = [
    { path: '/', component: UserLogin },
    { 
        path: '/admin',
        component: AdminPage,
        meta: { requiresAdmin: true },
    },
    { path: '/register', component: UserRegister },
];

const router = new VueRouter({ 
    mode: 'history', // Equivalent to createWebHistory()
    routes 
});

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAdmin) {
        await store.dispatch('fetchUser');
        if (store.state.user?.role === 'admin') {
            next();
        } else {
            next('/');
        }
    } else {
        next();
    }
});

export default router;
