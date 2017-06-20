/*
 See `doc/parallax-js.md` for instructions.
 */
export default function () {
  // Don't throw an exception on ancient browsers.
  if (!('classList' in document.body)) {
    return
  }

  const parallaxElementsA = [].slice.call(
    document.getElementsByClassName('js-Parallax')
  )
  let parallaxElements = []

  let transformProperty
  const nullElement = document.createElement('div')
  // Check for unprefixed 'transform', then check for 'webkitTransform'
  // (-webkit-transform). This is to add support for older Webkits (Safari and
  // Android browser) that are still widely used.
  if ('transform' in nullElement.style) {
    transformProperty = 'transform'
  } else if ('webkitTransform' in nullElement.style) {
    transformProperty = 'webkitTransform'
  } else {
    // Don't bother with -moz-transform (old Firefoxes that do not support
    // the unprefixed transform are basically non-existent), -ms-transform
    // (for IE9), etc.
    return
  }

  // Store these, as they don't change with every scroll.
  let windowHeight
  let windowMiddle
  let windowWidth

  function recalculateElementOffsets () {
    /*
     Calculate the top offsets of all of our elements and store them.
     This is to prevent doing it on every scroll; we only need to do it
     on load and on resize. getBoundingClientRect is surprisingly expensive.
     */

    windowWidth = window.innerWidth
    windowHeight = window.innerHeight
    windowMiddle = windowHeight / 2

    parallaxElements = []

    const currentPos =
      window.scrollY || window.pageYOffset || document.documentElement.scrollTop

    for (const element of parallaxElementsA) {
      const elemobj = {
        element,
        top: currentPos + element.getBoundingClientRect().top,
        // Bottom of the element, measured from the top of the document.
        bottom:
        currentPos +
        element.getBoundingClientRect().top +
        element.offsetHeight,
        // Middle of the element, measured from the top of the document.
        middle:
        currentPos +
        element.getBoundingClientRect().top +
        element.offsetHeight / 2,
        // If an element's position is above the half-way mark of the viewport
        // then we'll want to compensate for that - its starting point should
        // be zero.
        compensation: 0,
        // Completely arbitrary 'parallax by' factor.
        moveXBy: 0,
        moveYBy: 10,
        // These will be set if present.
        maxWidth: null,
        minWidth: null,

        // CSS property to change.
        cssProperty: element.dataset.parallaxCssProperty || transformProperty,
        // Template for transform property
        transformTemplate:
        element.dataset.parallaxTransformTemplate ||
        'translate3d([x][unit], [y][unit], 0)',
        unit: element.dataset.parallaxUnit || 'px'
      }

      if (elemobj.middle < window.innerHeight / 2) {
        elemobj.compensation = elemobj.middle - window.innerHeight / 2
      }

      if (element.dataset.parallaxXBy) {
        elemobj.moveXBy = parseFloat(element.dataset.parallaxXBy, 10)
      }

      if (element.dataset.parallaxYBy) {
        elemobj.moveYBy = parseFloat(element.dataset.parallaxYBy, 10)
      }

      let responsiveBreak = false

      if (element.dataset.parallaxMaxWidth) {
        const maxWidth = parseFloat(element.dataset.parallaxMaxWidth, 10)
        if (windowWidth > maxWidth) {
          responsiveBreak = true
        }
      }

      if (element.dataset.parallaxMinWidth) {
        const minWidth = parseInt(element.dataset.parallaxMinWidth, 10)
        if (windowWidth < minWidth) {
          responsiveBreak = true
        }
      }

      if (responsiveBreak) {
        element.style[transformProperty] = elemobj.transformTemplate
          .replace(/\[x\]/g, 0)
          .replace(/\[y\]/g, 0)
          .replace(/\[unit\]/g, elemobj.unit)

        element.style.transform = 'translate3d(0, 0, 0)'
        continue
      }

      parallaxElements.push(elemobj)
    }
  }

  recalculateElementOffsets()
  window.addEventListener('resize', recalculateElementOffsets)

  function scrollHook () {
    const currentPos =
      window.scrollY || window.pageYOffset || document.documentElement.scrollTop

    const scrollBottom = windowHeight + currentPos

    // This is an old-style loop for speed purposes; a ES6 `for (const i of
    // array)` is sometimes transpiled into something much slower.
    for (let i = 0; i < parallaxElements.length; i++) {
      const item = parallaxElements[i]
      // Do nothing if it is not on screen.
      if (scrollBottom < item.top || currentPos > item.bottom) {
        return
      }
      // How far is the middle of the element from the middle of the
      // screen?
      const middleOffset =
        item.middle - currentPos - windowMiddle - item.compensation

      let yOffset = 0
      let xOffset = 0

      if (item.moveXBy) {
        xOffset = middleOffset / 100.0 * item.moveXBy
      }

      if (item.moveYBy) {
        yOffset = middleOffset / 100.0 * item.moveYBy
      }

      if (item.unit === 'px') {
        yOffset = parseFloat(yOffset, 10)
        xOffset = parseFloat(xOffset, 10)
      }
      // Build the transform property.
      const transformString = item.transformTemplate
        .replace(/\[x\]/g, xOffset)
        .replace(/\[y\]/g, yOffset)
        .replace(/\[unit\]/g, item.unit)
      item.element.style[item.cssProperty] = transformString
    }
  }

  scrollHook()
  window.addEventListener('scroll', scrollHook)
}
