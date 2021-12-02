const handleError = (toast, title, message) => {
    toast.toast(message, {
        title,
        variant: 'danger',
        solid: true,
    })
}

export default handleError
