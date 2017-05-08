/*
External links (defined as all links pointing to a domain that is not the
same as the one from which the current document is being served)
will have their 'target' attribute set to '_blank'.

Social media sharing links will show in a popup.
*/
export function externalLinks () {
  const links = Array.from(document.getElementsByTagName('a'))

  // If the link starts with any of these things, we'll open a 600x300 popup
  // window for them.
  const usePopupPrefixes = [
    'https://twitter.com/intent/tweet?',
    'https://www.facebook.com/sharer.php?',
    'https://www.linkedin.com/shareArticle?'
  ]

  let thisDomain = window.location.hostname

  if (thisDomain.indexOf('www.') === 0) {
    thisDomain = thisDomain.substr(4)
  }

  for (const link of links) {
    const href = link.getAttribute('href').trim()

    if (!href) {
      continue
    }

    if (href.indexOf('http://') === 0 || href.indexOf('https://') === 0 || href.indexOf('//') === 0) {
      let domain = link.hostname

      if (domain.indexOf('www.') === 0) {
        domain = domain.substr(4)
      }

      if (domain !== thisDomain) {
        link.setAttribute('target', '_blank')
        // Add noopener and 'noreferrer' to work around this:
        // https://dev.to/ben/the-targetblank-vulnerability-by-example
        let rel = link.getAttribute('rel')

        if (!rel) {
          // will be null if it is not set
          rel = ''
        }

        link.setAttribute('rel', `${rel} noopener noreferrer`)
      }
    }

    // Use a popup for social sharing links.
    for (const prefix of usePopupPrefixes) {
      if (href.indexOf(prefix) === 0) {
        link.addEventListener('click', (event) => {
          event.preventDefault()
          window.open(href, '_blank', 'width=600,height=300,menubar=0,toolbar=0,status=0')
        })

        break
      }
    }
  }
}

/*
 https://github.com/vuejs/vue/issues/4419

 As per this, since we mount Vue on the `#app` element this breaks iframes in Safari (Safari bug).
 This snippet removes the iframe and re-inserts it so Safari is happy
 */
export function iframeFix () {
  const iframes = document.querySelectorAll('iframe')

  if (iframes.length > 0) {
    for (const iframe of iframes) {
      const iframeCopy = iframe.cloneNode()
      const parent = iframe.parentNode

      parent.insertBefore(iframeCopy, iframe)
      parent.removeChild(iframe)
    }
  }
}
