import axios from 'axios'
import * as Cookies from 'js-cookie'

const state = {
    userInfo: null,
}

const mutations = {
    setUserInfo(state, {userInfo}) {
        state.userInfo = userInfo
    },
    deleteInfo(state) {
        state.userInfo = null
    },
}

const actions = {
    logIn({commit}, {formData}) {
        return axios.post('/login', formData).then(res => {
            const userInfo = res.data
            commit('setUserInfo', {userInfo})
        })
    },
    logOut({commit}) {
        return axios.post('/logout').then(_ => {
            commit('deleteInfo')
        })
    },
    registerAccount({commit}, {registrationForm}) {
        return axios.post('/register', registrationForm).then(res => {
            const userInfo = res.data
            commit('setUserInfo', {userInfo})
        })
    },
}

const getters = {
    currentUser(state) {
        return state.userInfo
    },
    isLoggedIn(state) {
        // IMPORTANT NOTE: do not remove the two following lines, they somehow fix a bug
        // noted on Firefox that forced refreshing the page to be logged in.
        Cookies.get('session')
        state.userInfo
        return !!(Cookies.get('session')) && !!(state.userInfo)
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}
