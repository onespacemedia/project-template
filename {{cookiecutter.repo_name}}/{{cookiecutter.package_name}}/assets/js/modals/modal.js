export class Modal {
  constructor ({ el }) {
    const doc = document.documentElement || document.body

    this.els = {
      document: doc,
      modal: el,
      openTriggers: doc.querySelectorAll('.js-Modal_Open'),
      closeTriggers: el.querySelectorAll('.js-Modal_Close'),
      copyButton: el.querySelector('.js-Modal_Copy'),
      copyInput: el.querySelector('.js-Modal_CopyInput'),
      copyText: el.querySelector('.js-Modal_CopyText')
    }

    this.closeModal = this.closeModal.bind(this)
    this.openModal = this.openModal.bind(this)

    this.setupListeners()
    this.setupDisplay()
  }

  setupListeners () {
    this.els.openTriggers.forEach(el => {
      el.addEventListener('click', this.openModal)
    })

    this.els.closeTriggers.forEach(el => {
      el.addEventListener('click', this.closeModal)
    })

    this.els.copyButton.addEventListener('click', () => {
      this.els.copyInput.select()
      document.execCommand('copy')
      this.els.copyText.classList.add('mod-Copy_Text-active')

      window.setTimeout(() => {
        this.els.copyText.classList.remove('mod-Copy_Text-active')
      }, 5000)
    })
  }

  setupDisplay () {
    this.els.modal.style.display = 'none'
  }

  closeModal () {
    let opacityDone = false
    let visibilityDone = false

    // So we can fade out the modal but still have it display: none;
    const transitionFnc = evt => {
      if (evt.propertyName === 'opacity') opacityDone = true
      if (evt.propertyName === 'visibility') visibilityDone = true

      if (opacityDone && visibilityDone) {
        this.els.modal.removeEventListener('transitionend', transitionFnc)
        this.els.modal.style.display = 'none'
        this.els.document.classList.remove('lyt-Modal-isOpen')
      }
    }

    this.els.modal.addEventListener('transitionend', transitionFnc)
    this.els.modal.classList.remove('mod-Modal-isOpen')
  }

  openModal () {
    this.els.document.classList.add('lyt-Modal-isOpen')
    this.els.modal.style.display = ''

    window.setTimeout(() => {
      this.els.modal.classList.add('mod-Modal-isOpen')
    }, 1)
  }
}
