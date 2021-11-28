const handleError = (toast, title, message) => {
    toast.toast(message, {
        title,
        autoHideDelay: 5000,
        variant: 'danger',
        solid: true,
    })
}

export default handleError
