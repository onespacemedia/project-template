import { wrapElement } from '../utils'

export function overflowTables () {
  function tableSizer () {
    const tables = [].slice.call(
      document.querySelectorAll('.wys-WYSIWYG table')
    )

    if (tables.length > 0) {
      for (const table of tables) {
        // Don't do anything if we're already in a wrapper - we're called on
        // resize as well as load so this function can be called more than
        // once.
        let tableWrapper
        if (table.parentElement.classList.contains('wys-Table')) {
          tableWrapper = table.parentElement
        } else {
          tableWrapper = document.createElement('div')
          tableWrapper.classList.add('wys-Table')
          wrapElement(tableWrapper, tables)
        }

        // Add a class to indicate that it is overflowing (so that the 'scroll
        // left/right' text is displayed), if it is overflowing.
        if (tableWrapper.scrollWidth > tableWrapper.offsetWidth) {
          tableWrapper.classList.add('wys-Table-overflowing')
        } else {
          tableWrapper.classList.remove('wys-Table-overflowing')
        }
      }
    }
  }

  tableSizer()
  window.addEventListener('resize', tableSizer)
}
