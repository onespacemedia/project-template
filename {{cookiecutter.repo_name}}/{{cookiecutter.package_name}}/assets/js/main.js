import Vue from 'vue'
import App from './App'

import { externalLinks, iframeFix } from './utils'

new Vue(App).$mount('#app')

document.addEventListener('DOMContentLoaded', () => {
  externalLinks()

  // If the browser isn't Safari, don't do anything
  if (document.querySelector('iframe') && window.navigator.userAgent.indexOf("Safari") > -1) {
    iframeFix()
  }
})
