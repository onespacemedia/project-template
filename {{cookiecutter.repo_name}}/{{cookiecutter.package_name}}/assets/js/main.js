import 'babel-polyfill'
import 'intersection-observer'
import 'utils/class-list-polyfill'
import 'utils/focus-ring'
import 'utils/webp-detector'

import { svg4everybody } from './utils/svgforeverybody'

import LazyImage from './images'
import { Navigation } from './site'
import { externalLinks } from './utils'
import { overflowTables } from './wysiwyg'

document.addEventListener('DOMContentLoaded', () => {
  const body = document.body || document.documentElement
  body.classList.add('util-JSEnabled')

  externalLinks()
  new Navigation()
  overflowTables()

  const lazyImage = document.querySelector('.js-LazyImage')
  if (lazyImage) {
    const lazyImages = document.querySelectorAll('.js-LazyImage')
    const callback = (entries, observer) => {
      Array.from(entries).forEach((entry, index) => {
        if (entry.isIntersecting && !entry.target.dataset.activating) {
          entry.target.dataset.activating = true
          window.setTimeout(() => {
            new LazyImage({ el: entry.target })
            observer.unobserve(entry.target)
          }, 150 * index)
        }
      })
    }
    /* eslint-disable compat/compat */
    const observer = new IntersectionObserver(callback, {
      threshold: 0.4
    })
    Array.from(lazyImages).forEach(image => observer.observe(image))
  }

  // If the device is iOS add a class to the body so we can do specific CSS for it
  if (!!navigator.platform && /iPad|iPhone|iPod/.test(navigator.platform)) {
    const body = document.body || document.documentElement
    body.classList.add('is-iOS')
  }

  svg4everybody()

  // This class is used for making the animation duration on CSS animations 0, initially
  setTimeout(() => {
    document.body.classList.remove('util-Preload')
  }, 500)
})
