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
        return axios.post('/login', formData)
    },
    logOut({commit}) {
        return axios.post('/logout').then(_ => {
            commit('deleteInfo')
        })
    },
    uploadImage({dispatch}, {formData}) {
        return axios
        .post('/api/image/upload', formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
    },
    registerAccount({commit}, {registrationForm}) {
        return axios.post('/register', registrationForm)
    },
    uploadImages({dispatch}, {formData}) {
        return axios.post('api/upload/multiple/images', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
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
