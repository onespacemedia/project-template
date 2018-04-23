export default class LazyImage {
  constructor ({ el }) {
    this.el = el
    this.smallImage = this.el.querySelector('.img-Image_Image-small')
    this.image = this.el.querySelector('.img-Image_Image[data-src]')
    this.src = this.image.dataset.src.split(', ')
    this.supportsObjectFit = 'objectFit' in document.documentElement.style
    this.loadedClass = 'img-Image_Image-loaded'

    if (this.supportsObjectFit) {
      this.image.addEventListener('load', () => {
        this.image.classList.add(this.loadedClass)
      })
      this.image.addEventListener('transitionend', evt => {
        if (evt.propertyName === 'opacity') {
          this.smallImage.parentNode.removeChild(this.smallImage)
        }
      })

      this.image.setAttribute('src', this.src.join(', '))
    } else {
      const div = document.createElement('div')
      div.className = `img-Image_Image img-Image_Image-large img-Image_Image-noObjectFit ${
        this.loadedClass
      }`
      const imageUrl = window.devicePixelRatio >= 2 ? this.src[1] : this.src[0]
      div.style.backgroundImage = `url(${imageUrl})`
      this.image.parentNode.replaceChild(div, this.image)
    }
  }
}
