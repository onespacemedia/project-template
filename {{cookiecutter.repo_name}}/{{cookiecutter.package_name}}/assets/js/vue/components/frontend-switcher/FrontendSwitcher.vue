<template>
  <div class="fs-Outer">
    <div class="fs-Input">
      <label class="fs-Label">Page selector</label>

      <select class="fs-Switcher" v-model="selected" @change="handleSelect()">
        <option v-for="page in pages" :value="page" :selected="selected === page">{{ page|capitalize|normalCase }}</option>
      </select>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  export default {
    data () {
      return {
        selected: '',
        pages: window.frontendTemplates
      }
    },

    ready () {
      const parser = document.createElement('a')
      parser.href = window.location.href
      const splitPathname = parser.pathname.split('/')

      this.selected = splitPathname[splitPathname.length - 2]
    },

    methods: {
      handleSelect () {
        const parser = document.createElement('a')
        parser.href = window.location.href

        const url = `${parser.protocol}//${parser.hostname}:${parser.port}`

        window.location = `${url}/frontend/${this.selected}/`
      }
    },

    filters: {
      normalCase (value) {
        return value.replace(/-/g, ' ')
      }
    }
  }
</script>
