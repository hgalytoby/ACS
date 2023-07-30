export const progressbarOptions = {
  color: '#48e3d1',
  failedColor: '#ff0202',
  thickness: '4px',
  transition: {
    speed: '0.2s',
    opacity: '0.6s',
    termination: 300,
  },
  autoRevert: false,
  location: 'top',
  inverse: false,
}
export const toastificationOptions = {
  transition: 'Vue-Toastification__fade',
  maxToasts: 6,
  newestOnTop: true,
  filterBeforeCreate: (toast, toasts) => {
    if (toasts.filter(
      t => t.type === toast.type,
    ).length !== 0) {
      return false
    }

    return toast
    
  },
}
