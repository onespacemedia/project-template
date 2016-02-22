import Vue from 'vue'
import Revue from 'revue'
import {createStore} from 'redux'
import reducers from './reducers'

import actions from './actions'

const reduxStore = createStore(reducers)

const store = new Revue(Vue, reduxStore, actions)

export default store
