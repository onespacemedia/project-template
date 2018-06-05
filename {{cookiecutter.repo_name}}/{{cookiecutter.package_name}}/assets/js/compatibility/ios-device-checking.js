export default function iosDeviceChecking() {
  const body = document.body || document.documentElement

  // If the device is iOS add a class to the body so we can do specific CSS for it
  if (!!navigator.platform && /iPad|iPhone|iPod/.test(navigator.platform)) {
    body.classList.add('is-iOS')
  }
}
