const state = {
  show: false
}

const mutations = {
  'TOGGLE_MOBILE_NAV' (state) {
    console.log(state.show)
    state.show = !state.show
    console.log(state.show)
  }
}

export default {
  state,
  mutations
}
