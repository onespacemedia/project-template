import 'intersection-observer'
import { isVisible } from '../utils/index'

export function bindAnimations () {
  const animateCallback = (entries, animateObserver) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        const { target } = entry

        if (entry.target.dataset.animation) {
          entry.target.classList.add(
            `ani-Animation_${entry.target.dataset.animation}`
          )
        }

        animateObserver.unobserve(target)
      }
    })
  }

  const staggerCallback = (entries, staggerObserver) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        let nextTimer = 0
        const { target } = entry
        const children = Array.from(
          target.querySelectorAll('.ani-Animation_Child')
        )

        for (const child of children) {
          setTimeout(() => {
            child.classList.add(
              `ani-Animation_${target.getAttribute('data-animation')}`
            )
          }, nextTimer)

          if (isVisible(child)) {
            nextTimer += parseInt(target.getAttribute('data-time'))
          }
        }

        animateObserver.unobserve(target)
      }
    })
  }

  /* eslint-disable compat/compat */
  const animateObserver = new IntersectionObserver(animateCallback, {
    threshold: 0.1
  })

  const staggerObserver = new IntersectionObserver(staggerCallback, {
    threshold: 0.1
  })

  const animatableElements = Array.from(
    document.querySelectorAll('.ani-Animation_Animate')
  )

  const staggeredElements = Array.from(
    document.querySelectorAll('.ani-Animation_Stagger')
  )

  for (const el of animatableElements) {
    animateObserver.observe(el)
  }

  for (const el of staggeredElements) {
    staggerObserver.observe(el)
  }
}
