import { debounce, mediaBreakpoints } from '../utils'

export default class Navigation {
  constructor () {
    this.setUpElements()

    this.generateMobileNav()

    this.setUpMobileElements()

    this.items = this.constructItems(
      this.els.document.querySelectorAll('.nav-Mobile_Item')
    )

    this.isOpen = false

    this.toggleIsOpen = this.toggleIsOpen.bind(this)
    this.setupItems = this.setupItems.bind(this)

    this.setupListeners()
  }

  /**
   * Cache any elements we will use multiple times.
   */
  setUpElements () {
    const el = document.querySelector('.nav-Header')

    this.els = {
      el,
      document: document.documentElement || document.body,
      header: document.querySelector('.hd-Header'),
      nav: document.querySelector('.nav-Header_Items'),
      logo: document.querySelector('.hd-Header_Logo')
    }
  }

  /**
   * Cache any elements for the mobile nav that need to be cached after the mobile nav is created.
   */
  setUpMobileElements () {
    this.els.trigger = document.querySelector('.nav-Header_Trigger')

    this.els.backdrop = this.els.document.querySelector('.nav-Header_Backdrop')
  }

  /**
   * If we're on mobile we want to track the selected states to control the sub navigation open
   * / closed. aria-selected won't be used on lg++ so we programmatically add it just for sizes
   * below that.
   */
  setupItems () {
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

    window.addEventListener(
      'resize',
      debounce(this.handleResizeComplete.bind(this), 10)
    )
  }

  /**
   * Copy the desktop version of the nav and change the class names for mobile nav. Also add a
   * couple of mobile only elements.
   */
  generateMobileNav () {
    const backdrop = document.createElement('div')
    backdrop.className = 'nav-Header_Backdrop'

    const mobileNav = document.createElement('nav')
    mobileNav.className = 'nav-Mobile'
    mobileNav.setAttribute('aria-hidden', 'true')

    const mobileNavItems = this.els.nav.cloneNode(true)
    this.replaceClassNames(mobileNavItems, 'nav-Header', 'nav-Mobile')

    const mobileLogo = this.els.logo.cloneNode(true)
    this.replaceClassNames(mobileLogo, 'hd-Header_Logo', 'nav-Mobile_Logo')

    mobileNav.appendChild(mobileLogo)
    mobileNav.appendChild(mobileNavItems)

    this.insertAfter(mobileNav, this.els.header)
    this.insertAfter(backdrop, this.els.header)
  }

  /**
   * For the given elements replace partial or full class names with the given value.
   */
  replaceClassNames (els, origClass, newClass) {
    const allChildren = els.querySelectorAll('nav,div,span,ul,li,a,button')

    const replaceClassName = child => {
      const className = child.className

      if (className) {
        child.className = className.replace(
          new RegExp(origClass, 'g'),
          newClass
        )
      }
    }

    replaceClassName(els)

    Array.from(allChildren).forEach(child => {
      replaceClassName(child)
    })
  }

  /**
   * Close the mobile menu if the window grows too large.
   */
  handleResizeComplete () {
    if (window.innerWidth > mediaBreakpoints.lg) {
      if (this.isOpen) this.setIsOpen(false)
    }
  }

  toggleIsOpen () {
    this.setIsOpen(!this.isOpen)
  }

  /**
   * Add aria selected and active states for items and dropdowns.
   */
  constructItems (elements) {
    return Array.from(elements).map(item => {
      const dropdown = item.querySelector('[data-hasDropdown]')
      const hasChildren = item.classList.contains('nav-Mobile_Item-hasDropdown')
      const link = item.querySelector('.nav-Mobile_Link')

      const schema = {
        dropdown,
        hasChildren,
        link,
        el: item,
        parent: item.parentNode,
        children: hasChildren ? this.constructItems(dropdown.children) : {},
        back: hasChildren
          ? item.querySelector('.nav-Mobile_DropdownItem-back')
          : null,
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
          e.preventDefault()

          const isActive = !schema.active

          schema.active = isActive
          schema.parent.classList.toggle(className, isActive)
        })

        if (schema.back) {
          schema.back.addEventListener('click', () => {
            const isActive = !schema.active

            schema.active = isActive
            schema.parent.classList.toggle(className, isActive)
          })
        }
      }

      return schema
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
    this.els.trigger.classList.toggle('nav-Header_Trigger-open', val)

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

  insertAfter (newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling)
  }
}
