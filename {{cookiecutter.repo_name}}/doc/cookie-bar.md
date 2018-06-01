# Documentation for the `Cookie bar`
There are two main parts to the cookie bar: `cookie-bar.js` and `_cookie-notice.html`
## cookie-bar.js
There are two parts to `cookie-bar.js`, the part that deals with the cookie bar and the part that deals with classes that are intended to be put on buttons in the privacy policy. All data is stored in localstorage to avoid using external libraries such as js-Cookie. 

This also calls the global `tracking()` function which is defined in `_analytics.html` and is where all tracking scripts that don't anonymize IP and other identifying markers should go.

The current functionality uses soft consent which is that if the user continues to use the site after being give the option to opt-out, it is assumed that they consent and we can therefore load cookies and other scripts.

For the privacy policy buttons, simply have two buttons with the classes `js-CookieOptIn` and `js-CookieOptOut` and the js will do the rest.

## _cookie-notice.html
To add the cookie bar to a site, simply add `{% include 'base/_cookie-notice.html' %}` and use the two settings, `cookie-bar-text` and `cookie-bar-link` to define it's text and link location.

The cookie bar uses `position:sticky` so that it is always at the top of a page. if this breaks, the most likely cause is an `overflow: hidden` style on some element on the page. By default the close icon opts the user out and the accept will opt them in. In addition moving to another page will also opt them in. 
