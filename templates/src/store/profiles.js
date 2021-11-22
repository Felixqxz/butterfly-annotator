import axios from 'axios'

const actions = {
    uploadProfilePicture({dispatch}, {formData}) {
        return axios.post('/api/profile-picture', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
    },
    fetchUserData({dispatch}, {username}) {
        return axios.get('/api/user-info/' + username)
    },
}

export default {
    actions,
}
