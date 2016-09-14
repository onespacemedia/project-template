import Vue from 'vue'

import components from './components'

Vue.filter('toString', (val) => {
  return String(val)
})

Vue.config.debug = true

export default {
  components,

  events: {
    overflowBody (val) {
      if (val) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }
  }
}
