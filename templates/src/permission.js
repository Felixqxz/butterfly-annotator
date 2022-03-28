import router from './router'
import userData from './store'

// guard for authentication
router.beforeEach((to, from, next) => {
    if (to.meta.noAuth) {
        next()
    } else {
        // requires logging in
        if (userData.getters.isLoggedIn) {
            next() // is logged in; proceed
        } else {
            next({ path: '/login' }) // not logged in
        }
    }
})
