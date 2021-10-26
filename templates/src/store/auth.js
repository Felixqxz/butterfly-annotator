import axios from 'axios'

const state = {
    token: '',
    userInfo: null,
}

const mutations = {
    setToken(state, {token}) {
        state.token = token
    },
    setUserInfo(state, {userInfo}) {
        state.userInfo = userInfo
    },
    deleteInfo(state) {
        state.userInfo = null
        state.token = ''
    },
}

const actions = {
    logIn({commit}, {formData}) {
        return axios.post('/login', formData).then(res => {
            const token = res.data.data.username
            const userInfo = res.data.data
            commit('setToken', {token})
            commit('setUserInfo', {userInfo})
        })
    },
    logOut({commit}) {
        return axios.post('/logout').then(_ => {
            commit('deleteInfo')
        })
    },
    uploadImage({dispatch}, {formData}) {
        return axios.post('/api/image/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
    },
    registerAccount({commit}, {registrationForm}) {
        return axios.post('/register', registrationForm).then(res => {
            const token = res.data.data.username
            const userInfo = res.data.data
            commit('setToken', {token})
            commit('setUserInfo', {userInfo})
        })
    },
    readFile({dispatch}, {formData}) {
        return axios.post('/api/description/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
    },
}

const getters = {
    currentUser(state) {
        return state.userInfo
    },
    isLoggedIn(state) {
        return state.userInfo
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}
