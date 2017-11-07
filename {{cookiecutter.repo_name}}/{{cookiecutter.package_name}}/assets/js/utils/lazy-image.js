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

    try {
      const fragment = document.createDocumentFragment()
      const node = document
        .createRange()
        .createContextualFragment(
          this.createNode(
            this.aspectRatio,
            this.smallImageUrl,
            this.largeImageUrl
          )
        )
      const smallImage = node.querySelector('.img-Image_Image-small')
      const largeImage = node.querySelector('.img-Image_Image-large')
      const ieImage = node.querySelector('.img-Image_Image-ie')

      if (this.supportsObjectFit) {
        smallImage.addEventListener('load', () => {
          smallImage.classList.add(this.loadedClass)
        })
        largeImage.addEventListener('load', () => {
          largeImage.classList.add(this.loadedClass)
        })
      } else {
        largeImage.addEventListener('load', () => {
          ieImage.classList.add(this.loadedClass)
        })
      }

      fragment.appendChild(node)

      this.el.parentNode.replaceChild(fragment, this.el)
    } catch (e) {
      const div = document.createElement('div')
      div.innerHTML = this.createNode(
        this.aspectRatio,
        this.smallImageUrl,
        this.largeImageUrl
      )
      const el = div.firstElementChild
      this.el.parentNode.replaceChild(el, this.el)
      const smallImage = el.querySelector('.img-Image_Image-small')
      const largeImage = el.querySelector('.img-Image_Image-large')
      const ieImage = el.querySelector('.img-Image_Image-ie')

      if (this.supportsObjectFit) {
        smallImage.addEventListener('load', () => {
          smallImage.classList.add(this.loadedClass)
        })
        largeImage.addEventListener('load', () => {
          largeImage.classList.add(this.loadedClass)
        })
      } else {
        largeImage.addEventListener('load', () => {
          ieImage.classList.add(this.loadedClass)
        })
      }
    }
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
    // prettier-ignore
    const fallbackEl = `<div class="img-Image_Media">
      <div class="img-Image_Image img-Image_Image-large img-Image_Image-noObjectFit ${this.loadedClass}"
           style="background-image: url(${this.originalLargeImageUrl});"></div>
    </div>`

    return `
      <div class="img-Image${this.blur === false ? ' img-Image-noBlur' : ''}">
        <div class="img-Image_AspectRatioHolder">
          <div class="img-Image_AspectRatio"
               style="padding-bottom: ${this.aspectRatio}"></div>

          ${this.supportsObjectFit ? baseEl : fallbackEl}
      `
  }
}
