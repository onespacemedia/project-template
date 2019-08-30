function initDraggables () {
  function createHandle() {
    var handle = document.createElement('span')
    var handleText = document.createTextNode('☰')
    handle.appendChild(handleText)
    handle.classList.add('drag-handle')
    return handle
  }

  var sortableItems = document.querySelectorAll('.inline-navigation-item')
  for (var i = 0; i < sortableItems.length; i++) {
    sortableItems[i].insertAdjacentElement('afterbegin', createHandle())
  }

  Sortable.create(document.querySelector('.inline-navigation-items'), {
    handle: '.drag-handle',
    animation: 100,
    onStart: function (evt, originalEvent) {
      document.querySelector('.inline-navigation-content').classList.add('dragging')
    },
    onEnd: function (evt, originalEvent) {
      document.querySelector('.inline-navigation-content').classList.remove('dragging')
      var sections = document.querySelectorAll('.inline-navigation-item:not(.empty)')
      for (var i = 0; i < sections.length; i++) {
        var relatedSection = sections[i].dataset.inlineRelatedId
        document.querySelector('#' + relatedSection + ' .field-order input').value = i
      }
    }
  })
}

document.addEventListener('DOMContentLoaded', function () {
  initDraggables()
  document.querySelector('.add-row a').addEventListener('click', function () {
    initDraggables()
  })
})
