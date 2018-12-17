import axios from 'axios'
import tinymce from 'tinymce/tinymce'

import renderWYSIWYG from './wysiwyg'
import LazyImage from '../lazy-images/lazy-image'

const siteURL = '/ch/frontend-edit/'

function sendData (editData) {
  const ajaxOptions = {
    url: siteURL,
    method: 'post',
    data: editData,
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
        console.log('400 returned')
        console.log(data)
        return
      }
      /* eslint-disable no-console */
      console.error(e)
      /* eslint-enable no-console */
    })
}

export function setupEditing () {
  const simpleEditables = document.querySelectorAll('.js-SimpleEditable')
  for (const editable of simpleEditables) {
    editable.addEventListener('click', (e) => {
      e.preventDefault()
    })
    editable.addEventListener('blur', () => {
      const editData = {
        app: editable.dataset.app,
        model: editable.dataset.model,
        pk: editable.dataset.pk,
        field: editable.dataset.field,
        value: editable.innerHTML
      }

      sendData(editData)
    })
  }

  const WYSIWYGEditable = document.querySelectorAll('.js-WYSIWYGEditable')
  for (const editable of WYSIWYGEditable) {
    editable.addEventListener('click', () => {
      renderWYSIWYG({selector: `#${editable.getAttribute('id')}`})
      const saveButtonContainer = document.createElement('div')
      const saveButton = document.createElement('div')
      saveButton.innerHTML = 'Save'
      saveButton.classList.add('edt-SaveButton_Button')
      saveButtonContainer.classList.add('edt-SaveButton_Container')
      editable.parentNode.appendChild(saveButtonContainer)
      saveButtonContainer.appendChild(saveButton)

      saveButton.addEventListener('click', () => {
        tinymce.remove(`#${editable.getAttribute('id')}`)
        saveButtonContainer.parentNode.removeChild(saveButtonContainer)

        const editData = {
          app: editable.dataset.app,
          model: editable.dataset.model,
          pk: editable.dataset.pk,
          field: editable.dataset.field,
          value: editable.innerHTML
        }

        sendData(editData)
      })
    })
  }

  const imageEditable = document.querySelectorAll('.js-ImageEditable')
  for (const editable of imageEditable) {
    editable.addEventListener('click', () => {
      if (!editable.nextElementSibling || editable.nextElementSibling.nodeName !== 'IFRAME') {
        const iframe = document.createElement('iframe')
        iframe.src = `${editable.dataset.url}?file__iregex=.(png|gif|jpg|jpeg)$`
        iframe.frameborder = '0'
        iframe.classList.add('edt-Iframe')
        editable.parentNode.insertBefore(iframe, editable.nextSibling)
      }
    })
  }
  window.addEventListener('message', (e) => {
    if (e.origin === 'http://localhost:3000') {
      const ajaxOptions = {
        url: `${siteURL}?pk=${e.data}`,
        method: 'get',
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      }

      axios(ajaxOptions)
        .then(response => {
          const tempDiv = document.createElement('div')
          tempDiv.innerHTML = response.data.image_html
          const image = tempDiv.firstChild
          const originalImage = e.source.frameElement.previousElementSibling
          originalImage.replaceChild(image, originalImage.firstChild)
          new LazyImage({el: image})
          e.source.frameElement.parentNode.removeChild(e.source.frameElement)

          const editData = {
            app: image.parentNode.dataset.app,
            model: image.parentNode.dataset.model,
            pk: image.parentNode.dataset.pk,
            field: image.parentNode.dataset.field,
            value: e.data
          }

          sendData(editData)
        })
        .catch(e => {
          const { response } = e
          const { status, data } = response

          // form_invalid return
          if (status === 400) {
            console.log('400 returned')
            console.log(data)
            return
          }
          /* eslint-disable no-console */
          console.error(e)
          /* eslint-enable no-console */
        })
    }
  }, false)
}
