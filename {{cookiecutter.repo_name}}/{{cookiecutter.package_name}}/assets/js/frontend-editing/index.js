import axios from 'axios'

import LazyImage from '../lazy-images/lazy-image'
import { ImageEditable, SimpleEditable, WYSIWYGEditable } from './editable'

export function setupEditing () {
  const editables = document.querySelectorAll('.js-SimpleEditable')
  for (const el of editables) {
    new SimpleEditable({ el })
  }

  const WYSIWYGs = document.querySelectorAll('.js-WYSIWYGEditable')
  for (const el of WYSIWYGs) {
    new WYSIWYGEditable({ el })
  }

  const images = Array.from(document.querySelectorAll('.js-ImageEditable')).map(el => new ImageEditable({ el }))

  window.addEventListener('message', (e) => {
    if (e.origin === 'http://localhost:3000') {
      const ajaxOptions = {
        url: `/frontend-edit/?pk=${e.data}`,
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

          for (const imageEditable of images) {
            if (image.parentNode === imageEditable.el) {
              imageEditable.sendData()
            }
          }
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
  }, false)
}
