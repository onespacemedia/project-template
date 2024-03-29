export const mediaBreakpoints = {
  xs: 450,
  sm: 768,
  md: 900,
  lg: 1200,
  xlg: 1440,
  xxlg: 1600
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

export function debounce (func, wait, immediate) {
  let timeout

  return function () {
    const context = this
    const args = arguments

    const later = function () {
      timeout = null
      if (!immediate) func.apply(context, args)
    }

    const callNow = immediate && !timeout
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
    if (callNow) func.apply(context, args)
  }
}

export function isVisible (el) {
  return el.offsetWidth !== 0 && el.offsetHeight !== 0
}

export function removePreloadClass () {
  const body = document.body || document.documentElement

  // This class is used for making the animation duration on CSS animations 0, initially
  setTimeout(() => {
    body.classList.remove('util-Preload')
  }, 500)
}

// Wrap an HTMLElement around either a single element, or each element in an
// HTMLElement array.
export function wrapElement (toWrap, elements) {
  // Convert `elements` to an array, if necessary.
  if (!elements.length) {
    elements = [elements]
  } else {
    /* Array.from allows it to be used on an HTMLCollection. */
    elements = Array.from(elements)
  }

  // Loops backwards to prevent having to clone the wrapper on the
  // first element (see `child` below).
  for (let i = elements.length - 1; i >= 0; i--) {
    const child = i > 0 ? toWrap.cloneNode(true) : toWrap
    const el = elements[i]

    // Cache the current parent and sibling.
    const parent = el.parentNode
    const sibling = el.nextSibling

    // Wrap the element (is automatically removed from its current
    // parent).
    child.appendChild(el)

    // If the element had a sibling, insert the wrapper before
    // the sibling to maintain the HTML structure; otherwise, just
    // append it to the parent.
    if (sibling) {
      parent.insertBefore(child, sibling)
    } else {
      parent.appendChild(child)
    }
  }
}
