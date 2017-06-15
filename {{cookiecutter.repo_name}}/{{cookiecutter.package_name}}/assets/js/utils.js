/*
 External links (defined as all links pointing to a domain that is not the
 same as the one from which the current document is being served)
 will have their 'target' attribute set to '_blank'.

 Social media sharing links will show in a popup.
 */
export function externalLinks () {
  const links = Array.from(document.getElementsByTagName('a'))

  // If the link starts with any of these things, we'll open a 600x300 popup
  // window for them.
  const usePopupPrefixes = [
    'https://twitter.com/intent/tweet?',
    'https://www.facebook.com/sharer.php?',
    'https://www.linkedin.com/shareArticle?'
  ]

  let thisDomain = window.location.hostname

  if (thisDomain.indexOf('www.') === 0) {
    thisDomain = thisDomain.substr(4)
  }

  for (const link of links) {
    const href = link.getAttribute('href')

    if (!href) {
      continue
    }

    if (
      href.indexOf('http://') === 0 ||
      href.indexOf('https://') === 0 ||
      href.indexOf('//') === 0
    ) {
      let domain = link.hostname

      if (domain.indexOf('www.') === 0) {
        domain = domain.substr(4)
      }

      if (domain !== thisDomain) {
        link.setAttribute('target', '_blank')
        // Add noopener and 'noreferrer' to work around this:
        // https://dev.to/ben/the-targetblank-vulnerability-by-example
        let rel = link.getAttribute('rel')

        if (!rel) {
          // will be null if it is not set
          rel = ''
        }

        link.setAttribute('rel', `${rel} noopener noreferrer`)
      }
    }

    // Use a popup for social sharing links.
    for (const prefix of usePopupPrefixes) {
      if (href.indexOf(prefix) === 0) {
        link.addEventListener('click', event => {
          event.preventDefault()
          window.open(
            href,
            '_blank',
            'width=600,height=300,menubar=0,toolbar=0,status=0'
          )
        })

        break
      }
    }
  }
}

/*
 Media breakpoints
 */
export const mediaBreakpoints = {
  sm: 600,
  md: 900,
  lg: 1200,
  xlg: 1800
}

/*
 https://github.com/vuejs/vue/issues/4419

 As per this, since we mount Vue on the `#app` element this breaks iframes in Safari (Safari bug).
 This snippet removes the iframe and re-inserts it so Safari is happy
 */
export function iframeFix () {
  const iframes = document.querySelectorAll('iframe')

  if (iframes.length > 0) {
    for (const iframe of iframes) {
      const iframeCopy = iframe.cloneNode()
      const parent = iframe.parentNode

      parent.insertBefore(iframeCopy, iframe)
      parent.removeChild(iframe)
    }
  }
}

export function getOffsetTop (el, parent = document.body) {
  let offsetTop = 0

  do {
    if (!isNaN(el.offsetTop)) {
      offsetTop += el.offsetTop
    }

    el = el.offsetParent
  } while (el !== parent || el !== document.body)

  return offsetTop
}

export function getOffsetLeft (el, parent = document.body) {
  let offsetLeft = 0

  do {
    if (!isNaN(el.offsetLeft)) {
      offsetLeft += el.offsetLeft
    }

    el = el.offsetParent
  } while (el !== parent || el !== document.body)

  return offsetLeft
}

export function scrollToY (
  scrollTargetY = 0,
  speed = 300,
  easing = 'easeInOutQuint'
) {
  const scrollY = window.scrollY
  let currentTime = 0

  const time = Math.max(
    0.1,
    Math.min(Math.abs(scrollY - scrollTargetY) / speed, 0.8)
  )

  const easingEquations = {
    easeOutSine (pos) {
      return Math.sin(pos * (Math.PI / 2))
    },
    easeInOutSine (pos) {
      return -0.5 * (Math.cos(Math.PI * pos) - 1)
    },
    easeInOutQuint (pos) {
      if ((pos /= 0.5) < 1) {
        return 0.5 * Math.pow(pos, 5)
      }
      return 0.5 * (Math.pow(pos - 2, 5) + 2)
    }
  }

  function tick () {
    currentTime += 1 / 60

    const position = currentTime / time
    const t = easingEquations[easing](position)

    if (position < 1) {
      window.requestAnimationFrame(tick)

      window.scrollTo(0, scrollY + (scrollTargetY - scrollY) * t)
    } else {
      window.scrollTo(0, scrollTargetY)
    }
  }

  tick()
}

export class Cycler {
  constructor (items) {
    this.items = items
    this.currentPosition = 0
  }

  current () {
    return this.items[this.currentPosition]
  }

  set (val) {
    this.currentPosition = val
  }

  prev () {
    const current = this.current()
    this.currentPosition = this.currentPosition - 1

    if (this.currentPosition < 0) this.currentPosition = this.items.length - 1

    return current
  }

  next () {
    const current = this.current()
    this.currentPosition = (this.currentPosition + 1) % this.items.length

    return current
  }
}
