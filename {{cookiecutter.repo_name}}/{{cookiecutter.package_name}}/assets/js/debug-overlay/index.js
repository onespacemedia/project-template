import { mediaBreakpoints } from '../utils'

export function bindDebugOverlay () {
  if (
    !document.querySelector('.js-DebugOverlayTrigger') ||
    !document.querySelector('.dbg-Overlay')
  ) {
    return
  }

  const gridOverlay = document.querySelector('.dbg-Overlay')
  const overlayBreakpoint = document.querySelector('.dbg-Overlay_Breakpoint')

  // Put breakpoints into an array and sort by size.
  const keys = Object.keys(mediaBreakpoints)
  const breakpointsArray = []

  for (const key of keys) {
    breakpointsArray.push({
      name: key,
      screenWidth: mediaBreakpoints[key]
    })
  }

  breakpointsArray.sort((a, b) => {
    return a.size > b.size
  })

  for (const trigger of Array.from(
    document.querySelectorAll('.js-DebugOverlayTrigger')
  )) {
    trigger.addEventListener('click', () => {
      gridOverlay.classList.toggle('dbg-Overlay-visible')
    })
  }

  const setBreakpointText = () => {
    // Initial state.
    let breakpointText = `--xxs-viewport (<${
      breakpointsArray[0].screenWidth
    }px)`
    for (const breakpoint of breakpointsArray) {
      if (window.innerWidth >= breakpoint.screenWidth) {
        breakpointText = `--${breakpoint.name} (>= ${breakpoint.screenWidth}px)`
      }
    }
    overlayBreakpoint.innerText = breakpointText
  }
  setBreakpointText()
  window.addEventListener('resize', setBreakpointText)
}
