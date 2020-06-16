import '../css/app.css'
import * as Images from '../img' // eslint-disable-line no-unused-vars

import 'babel-polyfill'

// Browser compatibility shims and helpers
import './compatibility/class-list-polyfill'
import './compatibility/webp-detector'
import './compatibility/ios-device-checking'
import { svg4everybody } from './compatibility/svgforeverybody'

// OSM modules
import { bindCookieConsent } from './notices'
import { bindAnimations } from './viewport-animation'
import { bindDebugOverlay } from './debug-overlay'
import { bindExternalLinks } from './external-links'
import { setUpNavigation } from './navigation'
import { setUpLazyImage } from './lazy-images'
import { setUpFocusRing } from './focus-ring'
import { setUpOverflowTables } from './wysiwyg-js'
import { removePreloadClass } from './utils'
import { setUpModals } from './modals'

document.addEventListener('DOMContentLoaded', () => {
  // Add handlers for cookie consent bar
  bindCookieConsent()

  // Bind the in viewport checking for animations
  bindAnimations()

  // Set up debug grid overlay.
  bindDebugOverlay()

  // Make all external links open in a new tab
  bindExternalLinks()

  // Set up the nav bar and mobile nav menu
  setUpNavigation()

  // Set up lazy loading for images
  setUpLazyImage()

  // Add utility classes for when tabbing is happening
  setUpFocusRing()

  // Handle wrapping of tables in wysiwyg editors
  setUpOverflowTables()

  // Use a sprite sheet for SVG
  svg4everybody()

  // Remove pre loading class, used for fixing some filer/animation issues on load
  removePreloadClass()

  setUpModals()

  if (document.querySelector('.g-recaptcha')) {
    const rcScript = document.createElement('script')
    rcScript.setAttribute(
      'src',
      'https://www.google.com/recaptcha/api.js?hl=en'
    )
    window.addEventListener('DOMContentLoaded', function () {
      document.body.appendChild(rcScript)
    })
  }
})
