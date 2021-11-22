import axios from 'axios'

const actions = {
    uploadProfilePicture({dispatch}, {formData}) {
        return axios.post('/api/profile-picture', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
    },
}

export default {
    actions,
}
