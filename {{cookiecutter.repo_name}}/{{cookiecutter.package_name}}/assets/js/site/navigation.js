import { debounce, getOffsetTop, mediaBreakpoints } from '../utils/index'

export class Navigation {
  constructor () {
    const el = document.querySelector('.nav-Header')

    this.els = {
      el,
      trigger: el.querySelector('.nav-Header_Trigger'),
      document: document.documentElement || document.body,
      backdrop: el.querySelector('.nav-Header_Backdrop'),
      header: document.querySelector('.hd-Header'),
      tops: document.querySelectorAll(
        '.nav-Header_Items, .nav-Header_Backdrop, .nav-Header_Dropdown'
      )
    }

    this.items = this.constructItems(
      this.els.el.querySelectorAll('.nav-Header_Items > .nav-Header_Item')
    )

    this.isOpen = false

    this.toggleIsOpen = this.toggleIsOpen.bind(this)
    this.setupItems = this.setupItems.bind(this)

    this.setupListeners()
  }

  setupItems () {
    // If we're on mobile we want to track the selected states to control the sub navigation open
    // / closed. aria-selected won't be used on lg++ so we programmatically add it just for sizes
    // below that
    Array.from(
      this.els.el.querySelectorAll(
        '.nav-Header_Item:not(.nav-Header_Item-back)'
      )
    ).forEach(item => {
      window.innerWidth <= mediaBreakpoints.lg
        ? item.setAttribute('aria-selected', 'false')
        : item.removeAttribute('aria-selected')
    })
  }

  setupListeners () {
    this.els.trigger.addEventListener('click', this.toggleIsOpen)
    this.els.backdrop.addEventListener('click', this.toggleIsOpen)

    const resizeFnc = () => {
      if (window.innerWidth > mediaBreakpoints.lg) {
        this.isOpen = false

        Array.from(this.els.tops).forEach(item => {
          item.style.top = ''

          if (item.getAttribute('style') === '') {
            item.removeAttribute('style')
          }
        })
      } else {
        this.setTop()
      }
    }

    window.addEventListener('resize', debounce(resizeFnc, 10))
  }

  toggleIsOpen () {
    this.setIsOpen(!this.isOpen)
  }

  constructItems (elements) {
    return Array.from(elements).map(item => {
      const dropdown = item.querySelector('.nav-Header_Dropdown')
      const hasChildren = item.classList.contains('nav-Header_Item-hasDropdown')
      const link = item.querySelector('.nav-Header_Link')

      const schema = {
        dropdown,
        hasChildren,
        link,
        el: item,
        parent: item.parentNode,
        children: hasChildren
          ? this.constructItems(
            Array.from(dropdown.children).filter(
              child =>
                child.classList.contains('nav-Header_Item-back') === false
            )
          )
          : {},
        back: hasChildren ? item.querySelector('.nav-Header_Item-back') : null,
        _active: false,
        get active () {
          return this._active
        },
        set active (val) {
          this._active = val

          this.el.setAttribute('aria-selected', this._active)
        }
      }

      const className = schema.parent.classList.contains('nav-Header_Items')
        ? 'nav-Header_Items-active'
        : 'nav-Header_Dropdown-active'

      if (schema.hasChildren) {
        schema.link.addEventListener('click', e => {
          if (window.innerWidth <= mediaBreakpoints.lg) {
            e.preventDefault()

            const isActive = !schema.active

            schema.active = isActive
            schema.parent.classList.toggle(className, isActive)
          }
        })
        schema.back.addEventListener('click', () => {
          const isActive = !schema.active

          schema.active = isActive
          schema.parent.classList.toggle(className, isActive)
        })
      }

      return schema
    })
  }

  setTop () {
    Array.from(this.els.tops).forEach(el => {
      const top =
        window.innerWidth <= mediaBreakpoints.xs
          ? this.els.header.offsetHeight
          : getOffsetTop(this.els.header) + this.els.header.offsetHeight

      el.style.top = `${top}px`
    })
  }

  setIsOpen (val) {
    this.isOpen = val

    const inClass = 'nav-IsOpen-in'
    const outClass = 'nav-IsOpen-out'
    const endedClass = 'nav-IsOpen-ended'

    this.els.document.classList.toggle('nav-IsOpen', val)
    this.els.document.classList.toggle(inClass, val)
    this.els.document.classList.toggle(outClass, !val)
    this.els.trigger.setAttribute('aria-selected', val)

    if (!val) {
      this.els.document.classList.remove(endedClass)

      const setAllInactive = item => {
        item.active = false

        if (item.hasChildren) {
          item.children.forEach(child => {
            setAllInactive(child)
          })
        }
      }
      this.items.forEach(item => {
        setAllInactive(item)
      })
    }

    if (val) {
      this.setTop()
    }

    const animationFnc = e => {
      switch (e.animationName) {
        case 'SlideyMcFadeIn':
          this.els.document.classList.remove(inClass)
          this.els.document.classList.add(endedClass)

          break
        case 'SlideyMcFadeOut':
          this.els.document.classList.remove(outClass)

          break
      }
    }

    this.els.document.addEventListener('animationend', animationFnc)
  }
}
