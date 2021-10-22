import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const userData = new Vuex.Store({
    state: {
        token: localStorage.getItem('token'),
        loggedIn: false,
        userInfo: JSON.parse(sessionStorage.getItem('userInfo')),
    },
    mutations: {
        SET_TOKEN: (state, token) => {
            state.token = token
            localStorage.setItem('token', token)
        },
        SET_USERINFO: (state, userInfo) => {
            state.userInfo = userInfo
            sessionStorage.setItem('userInfo', JSON.stringify(userInfo))
            state.loggedIn = true
        },
        REMOVE_INFO: (state) => {
            localStorage.removeItem('token')
            sessionStorage.removeItem('userInfo')
            state.userInfo = {}
            state.token = ''
            state.loggedIn = false
        },
    },
    getters: {
        getUser: state => {
            return state.userInfo
        },
    },
    actions: {},
    modules: {},
})

export default userData
