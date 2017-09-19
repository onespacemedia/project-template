export default class LazyImage {
  constructor ({el}) {
    this.el = el
    this.altText = el.dataset.altText
    this.aspectRatio = el.dataset.aspectRatio
    this.smallImageUrl = el.dataset.smallImageUrl
    this.largeImageUrl = el.dataset.largeImageUrl

    this.supportsObjectFit = 'objectFit' in document.documentElement.style
    this.loadedClass = 'img-Image_Image-loaded'

    const fragment = document.createDocumentFragment()
    const node = this.createNode(this.aspectRatio, this.smallImageUrl, this.largeImageUrl)
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
    return document.createRange().createContextualFragment(`
      <div class="img-Image">
        <div class="img-Image_AspectRatioHolder">
          <div class="img-Image_AspectRatio" style="padding-bottom: ${this.aspectRatio}"></div>

          <div class="img-Image_Media">
            <img alt="" class="img-Image_Image img-Image_Image-small${blurred ? ' img-Image_Image-blurred' : ''}" src="${this.smallImageUrl}">
            <img alt="${this.altText}" class="img-Image_Image img-Image_Image-large" src="${this.largeImageUrl}">
            ${!this.supportsObjectFit ? `<div class="img-Image_Image img-Image_Image-ie" style="background-image: url(${this.largeImageUrl});"></div>` : ''}
          </div>
        </div>
      </div>
    `)
  }
}
