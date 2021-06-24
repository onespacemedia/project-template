function initMedia () {
  const videos = document.querySelectorAll('.js-MediaHero')

  for (const video of videos) {
    new HeroVideo(video)
  }
}

class HeroVideo {
  constructor (el) {
    this.el = el
    this.videoContainer = el.querySelector('.vid-Video')
    this.videoParent = el.querySelector('.js-MediaHero_Media')

    if (window.innerWidth < 1025) {
      this.videoContainer.parentNode.remove(this.videoContainer)
      return
    }

    this.rescaleVideos()
    this.setupListeners()
  }

  handleVimeo () {
    this.videoContainer.addEventListener('load', () => {
      window.setTimeout(() => {
        this.el.classList.add('vid-Video-isPlaying')
      }, 500)
    })
  }

  handleYoutube () {
    this.videoContainer.addEventListener('load', () => {
      window.setTimeout(() => {
        this.el.classList.add('vid-Video-isPlaying')
      }, 500)
    })
  }

  handleLocal () {
    this.videoContainer.addEventListener('canplaythrough', () => {
      this.videoContainer.play()
      this.el.classList.add('vid-Video-isPlaying')
    })
  }

  rescaleVideos () {
    this.videoContainer.style.transform = 'none'
    let scaleFactorY = 1
    let scaleFactorX = 1

    if (this.videoContainer.offsetHeight < this.videoParent.offsetHeight) {
      scaleFactorY = this.videoParent.offsetHeight / this.videoContainer.offsetHeight
    }

    if (this.videoContainer.offsetWidth < this.videoParent.offsetWidth) {
      scaleFactorX = this.videoParent.offsetWidth / this.videoContainer.offsetWidth
    }

    // Take the largest of the two.
    const scaleFactor = Math.max(scaleFactorX, scaleFactorY)

    /* Adjust because transform-origin is 50%. */
    const differenceAdjusted = 2 * scaleFactor - 1

    this.videoContainer.style.transformOrigin = '50% 50%'
    this.videoContainer.style.transform = `scale(${differenceAdjusted})`
  }

  setupListeners () {
    if (this.videoContainer.classList.contains('vid-Video-youtube')) {
      window.onYouTubeIframeAPIReady = () => {
        this.handleYoutube()
      }

      const scriptTag = document.createElement('script')
      scriptTag.src = 'https://www.youtube.com/player_api'
      document.body.appendChild(scriptTag)
    }

    if (this.videoContainer.classList.contains('vid-Video-vimeo')) {
      this.handleVimeo()
    }

    if (this.videoContainer.classList.contains('vid-Video-local')) {
      this.handleLocal()
    }

    window.addEventListener('resize', this.rescaleVideos)
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initMedia()
})
