import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import auth from './auth'
import images from './images'

Vue.use(Vuex)

const userData = new Vuex.Store({
    modules: {auth, images},
    plugins: [createPersistedState()],
})

export default userData
