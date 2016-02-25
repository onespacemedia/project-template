import Vue from 'vue'

import components from './components'

import store from './store'

Vue.filter('toString', (val) => {
  return String(val)
})

Vue.config.debug = true

export default {
  components,

  data () {
    return {
      mobileNav: store.state.mobileNav
    }
  },

  created () {
    this.$subscribe('mobileNav')
  },

  events: {
    overflowBody (val) {
      if (val) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }
  },

  methods: {
    toggleMobileNav () {
      store.dispatch({type: 'TOGGLE_MOBILE_NAV'})

      this.$emit('overflowBody', this.mobileNav.show)
    }
  }
}
