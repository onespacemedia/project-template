export default class LazyImage {
  constructor ({ el }) {
    this.el = el
    this.altText = el.dataset.altText
    this.aspectRatio = el.dataset.aspectRatio
    this.smallImageUrl = el.dataset.smallImageUrl
    this.largeImageUrl = el.dataset.largeImageUrl
    this.largeImage2xUrl = el.dataset['largeImage-2xUrl']

    this.supportsObjectFit = 'objectFit' in document.documentElement.style
    this.loadedClass = 'img-Image_Image-loaded'

    const fragment = document.createDocumentFragment()
    const node = this.createNode(
      this.aspectRatio,
      this.smallImageUrl,
      this.largeImageUrl
    )
    const smallImage = node.querySelector('.img-Image_Image-small')
    const largeImage = node.querySelector('.img-Image_Image-large')
    const ieImage = node.querySelector('.img-Image_Image-ie')

    if (this.supportsObjectFit) {
      smallImage.onload = () => smallImage.classList.add(this.loadedClass)
      largeImage.onload = () => largeImage.classList.add(this.loadedClass)
    } else {
      largeImage.onload = () => ieImage.classList.add(this.loadedClass)
    }

    fragment.appendChild(node)

    this.el.parentNode.replaceChild(fragment, this.el)
  }

  createNode (blurred = true) {
    const fallbackEl = `
      <div class="img-Image_Image img-Image_Image-ie"
           style="background-image: url(${this.largeImageUrl});"></div>`

    let imageClass = 'img-Image_Image img-Image_Image-small'
    imageClass += blurred
      ? ' img-Image_Image-blurred'
      : ''

    return document.createRange().createContextualFragment(`
      <div class="img-Image">
        <div class="img-Image_AspectRatioHolder">
          <div class="img-Image_AspectRatio"
               style="padding-bottom: ${this.aspectRatio}"></div>

          <div class="img-Image_Media">
            <img alt=""
                 class="${imageClass}"
                 src="${this.smallImageUrl}">
            <img alt="${this.altText}"
                 class="img-Image_Image img-Image_Image-large"
                 src="${this.largeImageUrl}"
                 srcset="${this.largeImage2xUrl} 2x">
            ${!this.supportsObjectFit ? fallbackEl : ''}
          </div>
        </div>
      </div>
    `)
  }
}
