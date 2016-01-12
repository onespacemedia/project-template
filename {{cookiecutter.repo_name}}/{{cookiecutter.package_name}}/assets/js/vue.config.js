import FrontendSwitcher from './components/frontend-switcher/FrontendSwitcher.vue'
import MobileNav from './components/mobile-nav/MobileNav.vue'

export default {
  events: {
    overflowBody (val) {
      if (val) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }
  },
  components: {
    FrontendSwitcher,
    MobileNav
  },
  methods: {
    showMobileNav () {
      this.$broadcast('showMobileNav')
    }
  }
}
