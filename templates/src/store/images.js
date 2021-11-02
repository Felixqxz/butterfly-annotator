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
    }
}

export default {
    actions,
}