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
        // TODO
        return new Promise((resolve, reject) => resolve({
            data: {
                imageUrl: 'https://static.standard.co.uk/2021/07/16/11/urnpublicidap.org8b4bf632ce0a40fa893f1d5c853e5056.jpg?width=968&auto=webp&quality=75&crop=968%3A645%2Csmart',
                width: 968,
                height: 645,
                description: 'Generic description of an image here',
                annotations: [],
            },
        }))
    },
}

export default {
    actions,
}