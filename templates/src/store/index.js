import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import auth from './auth'
import images from './images'
import profiles from './profiles'

Vue.use(Vuex)

const userData = new Vuex.Store({
    modules: {auth, images, profiles},
    plugins: [createPersistedState()],
})

export default userData
