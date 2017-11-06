export default class LazyImage {
  constructor ({ el }) {
    this.el = el
    this.altText = el.dataset.altText
    this.blur = el.dataset.blur === 'True'
    this.aspectRatio = el.dataset.aspectRatio
    this.smallImageUrl = el.dataset.smallImageUrl
    this.originalLargeImageUrl = el.dataset.originalLargeImageUrl
    this.originalLargeImage2xUrl = el.dataset['originalLargeImage-2xUrl']
    this.webPUrl = el.dataset.webpUrl
    this.webP2xUrl = el.dataset['webp-2xUrl']

    this.supportsObjectFit = 'objectFit' in document.documentElement.style
    this.loadedClass = 'img-Image_Image-loaded'

    const fragment = document.createDocumentFragment()
    const node = this.createNode()
    const smallImage = node.querySelector('.img-Image_Image-small')
    const largeImage = node.querySelector('.img-Image_Image-large')

    if (this.supportsObjectFit) {
      smallImage.onload = () => smallImage.classList.add(this.loadedClass)
      largeImage.onload = () => {
        largeImage.classList.add(this.loadedClass)

        if (!this.blur) {
          smallImage.classList.add('img-Image_Image-hide')
        }

        const transitionEndFnc = e => {
          smallImage.parentNode.removeChild(smallImage)

          e.target.removeEventListener('transitionend', transitionEndFnc)
        }

        largeImage.addEventListener('transitionend', transitionEndFnc)
      }
    }

    fragment.appendChild(node)

    this.el.parentNode.replaceChild(fragment, this.el)
  }

  createNode () {
    let smallImageClass = 'img-Image_Image img-Image_Image-small'
    smallImageClass += this.blur ? ' img-Image_Image-blurred' : ''

    const baseEl = `<picture class="img-Image_Media">
      <source srcset="${this.webPUrl}, ${this.webP2xUrl} 2x" type="image/webp">
        <img alt=""
             class="${smallImageClass}"
             src="${this.smallImageUrl}">
        <img alt="${this.altText}"
             class="img-Image_Image img-Image_Image-large"
             src="${this.originalLargeImageUrl}"
             srcset="${this.originalLargeImage2xUrl} 2x">
    </picture>`
    const fallbackEl = `<div class="img-Image_Media">
      <div class="img-Image_Image img-Image_Image-large img-Image_Image-noObjectFit ${this
      .loadedClass}"
           style="background-image: url(${this.originalLargeImageUrl});"></div>
    </div>`

    return document.createRange().createContextualFragment(`
      <div class="img-Image${this.blur === false ? ' img-Image-noBlur' : ''}">
        <div class="img-Image_AspectRatioHolder">
          <div class="img-Image_AspectRatio"
               style="padding-bottom: ${this.aspectRatio}"></div>

          ${this.supportsObjectFit ? baseEl : fallbackEl}
      `)
  }
}
