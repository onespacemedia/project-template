export default function mobileNav (state = { show: false }, action) {
  switch (action.type) {
    case 'TOGGLE_MOBILE_NAV':
      return Object.assign({}, state, {
        show: !state.show
      })
    default:
      return state
  }
}
