import { Modal } from './modal'

export function setUpModals () {
  const eles = document.querySelectorAll('.js-Modal')

  for (const el of eles) {
    new Modal({ el })
  }
}
