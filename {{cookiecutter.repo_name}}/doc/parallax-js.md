# Documentation for `parallax.js`

`parallax.js` is a small, fast, vanilla JS implementation of parallaxing.

It has been massively optimised for speed. While listening to the `scroll` event is usually considered a no-no, it does so little work in the hook that it has no effect on performance.

Everything that can be precomputed or cached, is precomputed or cached. The only operations that are performed in the `scroll` event are simple mathematical operations, a few object key lookups and three string replacements, all of which are very fast operations. By default it does not change any CSS properties that cause layout recalculations; it uses `transform`, which is hardware-accelerated on nearly all browsers out there.

## Activating it

```javascript
import parallax from './parallax'
document.addEventListener('DOMContentLoaded', () => {
  parallax()
}
```

After that, add the `js-Parallax` class to an element and it will activate with sensible defaults.

## Customisation

Exactly how the parallaxing behaves can be controlled with `data-*` attributes.

### data-parallax-y-by

This specifies a slightly-arbitrary vertical parallaxing factor. A smaller number will increase the parallax factor, and a larger number will increase it. You can specify a negative number to reverse the parallax effect.

```html
<div class="js-Parallax" data-parallax-y-by="2.5"></div>
```

### data-parallax-x-by

This works the same as the above, but affects the horizontal direction. This is zero by default, i.e. there is no X parallaxing.

```html
<div class="js-Parallax" data-parallax-x-by="0.5"></div>
```

### data-parallax-unit

This defines the CSS unit to be used on the `transform`. It defaults to `px`.

```html
<div class="js-Parallax" data-parallax-unit="%"></div>
```

### data-parallax-min-width

This is the minimum screen width, in pixels, at which parallaxing will be used. This is necessary for disabling parallax for smaller devices, usually for layout purposes.

```html
<div class="js-Parallax" data-parallax-min-width="1024"></div>
```

### data-parallax-max-width

This does the opposite of the above; at screen widths larger than this, the parallax effect will be disabled. You can combine it with the above if you nest a `.js-Parallax` element within another. Here's an example that applies a different parallax factor when the display is at least 1024 pixels wide:

```html
<div class="js-Parallax" data-parallax-min-width="1024" data-parallax-move-y-by="10">
  <div class="js-Parallax" data-parallax-max-width="1023" data-move-y-by="5"></div>
</div>
```

### data-transform-template

This allows complete control over the `transform` CSS property used for the parallaxing effect. The strings `[x]`, `[y]` and `[unit]` will be replaced with the X parallax factor, Y parallax factor, and the CSS unit.

```html
<div class="js-Parallax" data-parallax-transform-template="translate3d(0, [y][unit], 0) rotate([x]deg)"></div>
```

### data-parallax-css-property

This defines the CSS property used for the parallax effect. It defaults to `transform`. Changing this will require modifying `data-transform-template`.

**Warning**: be careful what CSS properties you use, and try to think of ways in which you can utilise `transform` rather than other properties. `transform` is guaranteed to not force layout recalculations (which is a speed killer), and it is usually hardware-accelerated. Other properties may not be both or either of these things.

```html
<div class="js-Parallax" data-parallax-css-property='top' data-parallax-transform-template="[y][unit]"></div>
```
