import Vue from 'vue'
import App from './App'

import externalLinks from './external-links'

new Vue(App).$mount('#app')

document.addEventListener('DOMContentLoaded', () => {
  externalLinks()
})
