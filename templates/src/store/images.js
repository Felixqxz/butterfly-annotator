import axios from 'axios'

const actions = {
    listBanks({dispatch}) {
        return axios.get('/api/bank-list')
    },
    listImages({dispatch}, {bankId}) {
        return axios.get('/api/bank/' + bankId)
    },
    listAccesses({dispatch}, {bankId}) {
        return axios.get('/api/bank-list-accesses/' + bankId)
    },
    requestPermission({dispatch}, {targetUser, level, bankId}) {
        return axios.put('/api/bank-access', {targetName: targetUser, level, id: bankId})
    },
    fetchImageData({dispatch}, {imageId}) {
        return axios.get('/api/image/' + imageId)
    },
    sendAnnotations({dispatch}, {data}) {
        return axios.post('/api/image/annotate', data)
    },
    getAvatar({dispatch}) {
        return axios.get('/api/avatar/get')
    },
    getUserInfo({dispatch}) {
        return axios.get('/api/info/get')
    },
}

export default {
    actions,
}