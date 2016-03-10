import Vue from 'vue'
import Vuex from 'vuex'

import modules from './components/modules'

Vue.use(Vuex)

export default new Vuex.Store({ // eslint-disable-line new-cap
  modules
})
