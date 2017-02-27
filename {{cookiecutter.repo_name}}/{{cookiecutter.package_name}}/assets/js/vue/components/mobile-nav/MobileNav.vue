<template>
  <div class="mbn-MobileNav_Container">
    <div class="mbn-Trigger" @click="open = !open" :aria-selected="String(open)">
      <span class="mbn-Trigger_Line mbn-Trigger_Line-top"></span>
      <span class="mbn-Trigger_Line mbn-Trigger_Line-middle"></span>
      <span class="mbn-Trigger_Line mbn-Trigger_Line-bottom"></span>
    </div>

    <transition name="trn-Fade">
      <nav class="mbn-MobileNav"
           v-show="open"
           @click="open = !open">
        <ul class="mbn-Items" @click.stop>
          <li class="mbn-Item">
            <a href="/" class="mbn-Item_Link">Home</a>
          </li>

          <li class="mbn-Item"
              v-for="(item, index) in items"
              :class="{ 'mbn-Item-children': item.children.length }"
              :aria-selected="String(activeChild == index)">
            <a class="mbn-Item_Link"
               :href="item.children.length ? null : item.url"
               @click.stop="handleParentLink('activeChild', item, index)">{{ item.title }}
            </a>

            <transition name="trn-SlideIn">
              <ul :class="{ 'mbn-Children': true, 'mbn-Children-disableOverflow': activeChildChild !== undefined }"
                  v-show="item.children.length !== 0 && activeChild === index"
                  :aria-selected="String(activeChild == index)">
                <li class="mbn-Item mbn-Item-back">
                  <a class="mbn-Item_Link" @click="activeChild = undefined">Back</a>
                </li>

                <li class="mbn-Item">
                  <a class="mbn-Item_Link" :href="item.url">{{ item.title }}</a>
                </li>

                <li class="mbn-Item"
                    v-for="(child, childIndex) in item.children"
                    :class="{ 'mbn-Item-children': child.children.length }">
                  <a class="mbn-Item_Link"
                     :href="child.children.length ? null : child.url"
                     @click.stop="handleParentLink('activeChildChild', child, childIndex)">{{ child.title }}
                  </a>

                  <transition name="trn-SlideIn">
                    <ul class="mbn-Children"
                        v-show="child.children.length !== 0 && activeChildChild === childIndex"
                        :aria-selected="String(activeChildChild == childIndex)">
                      <li class="mbn-Item mbn-Item-back">
                        <a class="mbn-Item_Link" @click="activeChildChild = undefined">
                          <span>Back</span>
                        </a>
                      </li>

                      <li class="mbn-Item">
                        <a class="mbn-Item_Link" :href="child.url">{{ child.title }}</a>
                      </li>

                      <li class="mbn-Item" v-for="child in child.children">
                        <a class="mbn-Item_Link" :href="child.url">{{ child.title }}</a>
                      </li>
                    </ul>
                  </transition>
                </li>
              </ul>
            </transition>
          </li>
        </ul>
      </nav>
    </transition>
  </div>
</template>

<script>
  import { mediaBreakpoints } from '../../../utils'

  export default {
    props: ['items'],

    data: () => ({
      open: false,
      activeChild: undefined,
      activeChildChild: undefined
    }),

    mounted () {
      this.onResize()

      window.addEventListener('resize', this.onResize.bind(this))
    },

    watch: {
      open (val) {
        const body = document.body || document.documentElement

        body.classList.toggle('nav-IsOpen', val)
      }
    },

    methods: {
      handleParentLink (dataItem, item, index) {
        if (item.children.length) {
          if (this[dataItem] === index) {
            this[dataItem] = null
          } else {
            this[dataItem] = index
          }
        } else {
          window.location = item.url
        }
      },

      onResize (event) {
        if (window.innerWidth >= mediaBreakpoints.lg && this.open) this.open = false
      }
    }
  }
</script>
