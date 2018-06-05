import 'intersection-observer'
import LazyImage from './lazyimage'

export function setUpLazyImage () {
  const lazyImage = document.querySelector('.js-LazyImage')

  if (lazyImage) {
    const lazyImages = document.querySelectorAll('.js-LazyImage')
    const callback = (entries, observer) => {
      Array.from(entries).forEach((entry, index) => {
        if (entry.isIntersecting && !entry.target.dataset.activating) {
          entry.target.dataset.activating = true
          window.setTimeout(() => {
            /* eslint-disable no-new */
            new LazyImage({el: entry.target})
            observer.unobserve(entry.target)
          }, 150 * index)
        }
      })
    }

    /* eslint-disable compat/compat */
    const observer = new IntersectionObserver(callback, {
      threshold: 0,
      rootMargin: `${window.innerHeight}px`
    })
    Array.from(lazyImages).forEach(image => observer.observe(image))
  }
}
