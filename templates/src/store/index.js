import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import auth from './auth'
import axios from 'axios'

Vue.use(Vuex)

const userData = new Vuex.Store({
    actions: {
        listBanks({ dispatch }) {
            return axios.get('/api/bank-list')
        },
        listImages({ dispatch }, { bankId }) {
            return axios.get('/api/bank/' + bankId)
        },
        getImage({ dispatch }, { imageId }) {
            return axios.get('api/image/' + imageId)
        },
        nextImage({ dispatch }, { imageId }) {
            return axios.get('api/image/next/' + imageId)
        },
        previousImage({ dispatch }, { imageId }) {
            return axios.get('api/image/previous/' + imageId)
        },
    },
    modules: {auth},
    plugins: [createPersistedState()],
})

export default userData
