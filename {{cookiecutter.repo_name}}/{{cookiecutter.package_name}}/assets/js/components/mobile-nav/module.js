const state = {
  show: false
}

const mutations = {
  'TOGGLE_MOBILE_NAV' (state) {
    state.show = !state.show
  }
}

export default {
  state,
  mutations
}
