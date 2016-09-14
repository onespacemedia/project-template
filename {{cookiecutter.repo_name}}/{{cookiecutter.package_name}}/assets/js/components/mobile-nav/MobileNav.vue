<template>
  <div class="mbn-MobileNav"
       v-show="show"
       @click="toggleMobileNav()">
    <nav class="mbn-Items" @click.stop>
      <div class="mbn-Item"
           v-for="item in items" track-by="$index">
        <a class="mbn-Item_Action"
           :href="item.children.length ? null : item.url"
           @click.stop="item.children.length ? activeItem = $index : toggleMobileNav()">
          {{ item.title }}

          <span class="mbn-Children_Indicator" v-show="item.children.length"></span>
        </a>

        <div class="mbn-Children"
             v-show="item.children.length && activeItem === $index"
             transition="trn-Swipe"
             :aria-selected="activeItem == $index | toString">
          <div class="mbn-Child_Item">
            <a class="mbn-Child_ItemAction" @click.stop="activeItem = null">
              <span class="mbn-BackIndicator"></span>
              <span>Back</span>
            </a>
          </div>

          <div class="mbn-Child_Item">
            <a class="mbn-Child_ItemAction" :href="item.url">
              <span>{{ item.title }}</span>
            </a>
          </div>

          <div class="mbn-Child_Item" v-for="child in item.children">
            <a class="mbn-Child_ItemAction" :href="child.url">
              <span>{{ child.title }}</span>
            </a>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script type="text/ecmascript-6">
  export default {
    data () {
      return {
        activeItem: null,
        items: [],
        show: false
      }
    },

    ready () {
      this.items = window.navigationData

      document.addEventListener('keydown', (e) => {
        if (this.show && e.keyCode === 27) {
          this.toggleMobileNav()
        }
      })
    },

    methods: {
      handleParentLink (item, index) {
        if (item.children.length) {
          this.activeItem = index
        } else {
          window.location = item.url
        }
      }
    }
  }
</script>
