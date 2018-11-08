export function bindCookieConsent () {
  const bar = document.querySelector('.js-CookieConsent')
  const accept = document.querySelector('.js-CookieAccept')
  const close = document.querySelector('.js-CookieClose')
  const optIn = document.querySelector('.js-CookieOptIn')
  const optOut = document.querySelector('.js-CookieOptOut')

  if (bar && accept && close) {
    if (!window.localStorage.getItem('cookie_consent') && !window.localStorage.getItem('no_cookie_consent')) {
      bar.classList.add('cc-Bar-show')
      window.addEventListener('beforeunload', () => {
        if (!window.localStorage.getItem('no_cookie_consent')) {
          window.localStorage.setItem('cookie_consent', 'true')
        }
      })
    }

    accept.addEventListener('click', () => {
      bar.parentNode.removeChild(bar)
      window.localStorage.removeItem('no_cookie_consent')
      window.localStorage.setItem('cookie_consent', 'true')
      window.tracking()
    })

    close.addEventListener('click', () => {
      bar.parentNode.removeChild(bar)
      window.localStorage.removeItem('cookie_consent')
      window.localStorage.setItem('no_cookie_consent', 'true')
    })
  }

  // Opt-in/Opt-out buttons to be put somewhere on the privacy
  // policy page with the classes js-CookieOptIn and js-CookieOptOut
  if (optIn && optOut) {
    if (window.localStorage.getItem('no_cookie_consent')) {
      optOut.style.display = 'none'
    }

    if (window.localStorage.getItem('cookie_consent')) {
      optIn.style.display = 'none'
    }

    optIn.addEventListener('click', () => {
      window.localStorage.removeItem('no_cookie_consent')
      window.localStorage.setItem('cookie_consent', 'true')
      window.location.reload()
    })

    optOut.addEventListener('click', () => {
      window.localStorage.removeItem('cookie_consent')
      window.localStorage.setItem('no_cookie_consent', 'true')
      window.location.reload()
    })
  }
}
