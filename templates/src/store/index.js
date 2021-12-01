import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import auth from './auth'
import images from './images'
import profiles from './profiles'
import * as Cookies from 'js-cookie'

Vue.use(Vuex)

const userData = new Vuex.Store({
    modules: {auth, images, profiles},
    plugins: [createPersistedState({
        getState: key => Cookies.get(key) ? JSON.parse(Cookies.get(key)) : null,
        setState: (key, state) => Cookies.set(key, JSON.stringify(state)),
    })],
})

export default userData
