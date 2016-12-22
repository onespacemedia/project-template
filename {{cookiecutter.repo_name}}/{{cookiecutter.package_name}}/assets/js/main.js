import Vue from 'vue'
import App from './App'

import { externalLinks, safariIframeFix } from './utils'

new Vue(App).$mount('#app')

document.addEventListener('DOMContentLoaded', () => {
  externalLinks()

  if (document.querySelector('iframe')) {
    safariIframeFix()
  }
})
