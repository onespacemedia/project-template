import axios from 'axios'
import tinymce from 'tinymce/tinymce'
import renderWYSIWYG from './wysiwyg'

class Editable {
  constructor ({ el }) {
    this.el = el
    this.siteURL = '/frontend-edit/'

    this.setupListeners()
  }

  setupListeners () {}

  get editData () {
    return {
      app: this.el.dataset.app,
      model: this.el.dataset.model,
      pk: this.el.dataset.pk,
      field: this.el.dataset.field,
      value: this.el.innerHTML
    }
  }

  sendData () {
    const ajaxOptions = {
      url: this.siteURL,
      method: 'post',
      data: this.editData,
      xsrfCookieName: 'csrftoken',
      xsrfHeaderName: 'X-CSRFToken',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    }

    axios(ajaxOptions)
      .then(response => {
        return response
      })
      .catch(e => {
        const { response } = e
        const { status, data } = response

        // form_invalid return
        if (status === 400) {
          return
        }
        /* eslint-disable no-console */
        console.error(e)
        /* eslint-enable no-console */
      })
  }
}

export class SimpleEditable extends Editable {
  setupListeners () {
    this.el.addEventListener('click', e => {
      e.preventDefault()
    })

    this.el.addEventListener('blur', () => {
      this.sendData()
    })

    this.el.addEventListener('paste', e => {
      e.preventDefault()
      document.execCommand('inserttext', false, e.clipboardData.getData('text/plain'))
    })
  }
}

export class WYSIWYGEditable extends Editable {
  setupListeners () {
    this.el.addEventListener('click', () => {
      this.initialiseWYSIWYG()

      this.saveButton.addEventListener('click', () => {
        tinymce.remove(`#${this.el.getAttribute('id')}`)
        this.saveButtonContainer.parentNode.removeChild(this.saveButtonContainer)

        this.sendData()
      })
    })
  }

  initialiseWYSIWYG () {
    renderWYSIWYG({selector: `#${this.el.getAttribute('id')}`})

    this.saveButtonContainer = document.createElement('div')
    this.saveButton = document.createElement('div')
    this.saveButton.innerHTML = 'Save'
    this.saveButton.classList.add('edt-SaveButton_Button')
    this.saveButtonContainer.classList.add('edt-SaveButton_Container')
    this.el.parentNode.appendChild(this.saveButtonContainer)
    this.saveButtonContainer.appendChild(this.saveButton)
  }
}

export class ImageEditable extends Editable {
  setupListeners () {
    this.el.addEventListener('click', () => {
      if (!this.el.nextElementSibling || this.el.nextElementSibling.nodeName !== 'IFRAME') {
        const iframe = document.createElement('iframe')
        iframe.src = `${this.el.dataset.url}?file__iregex=.(png|gif|jpg|jpeg)$`
        iframe.frameborder = '0'
        iframe.classList.add('edt-Iframe')
        this.el.parentNode.insertBefore(iframe, this.el.nextSibling)
      }
    })
  }

  get editData () {
    return {
      app: this.el.dataset.app,
      model: this.el.dataset.model,
      pk: this.el.dataset.pk,
      field: this.el.dataset.field,
      value: this.el.dataset.value
    }
  }
}
