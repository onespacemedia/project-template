const body = document.body || document.documentElement
body.classList.remove('util-IsTabbing')

const handleFirstTab = e => {
  if (e.keyCode === 9) {
    body.classList.add('util-IsTabbing')

    window.removeEventListener('keydown', handleFirstTab)
    window.addEventListener('mousedown', handleMouseDownOnce)
  }
}

window.addEventListener('keydown', handleFirstTab)

const handleMouseDownOnce = () => {
  body.classList.remove('util-IsTabbing')

  window.removeEventListener('mousedown', handleMouseDownOnce)
  window.addEventListener('keydown', handleFirstTab)
}

window.addEventListener('mousedown', handleMouseDownOnce)
