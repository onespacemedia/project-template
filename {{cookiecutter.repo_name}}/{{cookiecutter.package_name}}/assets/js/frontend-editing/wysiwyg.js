import tinymce from 'tinymce/tinymce'
import 'tinymce/themes/modern/theme'
import 'tinymce/plugins/code/plugin'
import 'tinymce/plugins/hr/plugin'
import 'tinymce/plugins/image/plugin'
import 'tinymce/plugins/link/plugin'
import 'tinymce/plugins/lists/plugin'
import 'tinymce/plugins/table/plugin'
import axios from 'axios'

export default function ({ selector }) {
  tinymce.baseURL = '/static/tinymce'
  tinymce.init({
    selector,
    base: '/static/tinymce',
    content_css: '/static/build/css/wysiwyg.css',
    menubar: false,
    branding: false,
    statusbar: false,
    height: 350,
    plugins: 'image lists hr link table code',
    block_formats: 'Paragraph=p;Heading=h2;Subheading=h3;',
    toolbar1:
      'bold italic underline strikethrough removeformat' +
      ' | ' +
      'formatselect numlist bullist blockquote' +
      ' | ' +
      'table image code',
    formats: {
      underline: {
        inline: 'u'
      }
    },
    image_title: true,
    automatic_uploads: true,
    relative_urls: false,
    file_picker_types: 'image',

    // Start custom image picker
    images_upload_handler: (blobInfo, success, failure) => {
      const formData = new FormData()
      formData.append('file', blobInfo.blob(), blobInfo.name())
      const ajaxOptions = {
        url: '/image-upload/',
        method: 'post',
        data: formData,
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      }

      axios(ajaxOptions).then(response => {
        if (response['data']['success']) {
          success(response['data']['location'])
        } else {
          failure(response['data']['fail_message'])
        }
      })
    },

    file_picker_callback: (cb, value, meta) => {
      const input = document.createElement('input')
      input.setAttribute('type', 'file')
      input.setAttribute('accept', 'image/*')
      input.onchange = function () {
        const file = this.files[0]

        const reader = new FileReader()
        reader.onload = function () {
          // Note: Now we need to register the blob in TinyMCEs image blob
          // registry. In the next release this part hopefully won't be
          // necessary, as we are looking to handle it internally.
          const id = `blobid ${new Date().getTime()}`
          const blobCache = tinymce.activeEditor.editorUpload.blobCache
          const base64 = reader.result.split(',')[1]
          const blobInfo = blobCache.create(id, file, base64)
          blobCache.add(blobInfo)

          // call the callback and populate the Title field with the file name
          cb(blobInfo.blobUri(), { title: file.name })
        }
        reader.readAsDataURL(file)
      }

      input.click()
    },
    images_upload_url: '/image-upload/',
    images_upload_base_path: '/media/uploads/message_images/',
    images_upload_credentials: true,

    /* Plugin-specific stuff here */
    table_appearance_options: false,
    table_advtab: false
  })
}
