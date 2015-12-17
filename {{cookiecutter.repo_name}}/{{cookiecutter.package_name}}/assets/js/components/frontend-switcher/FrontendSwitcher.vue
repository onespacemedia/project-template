<template>
  <div class="fs-Outer">
    <div class="fs-Input">
      <label class="fs-Label">Page selector</label>

      <select class="fs-Switcher" v-model="selected" @change="handleSelect()">
        <option v-for="page in pages" :value="page">{{ page|capitalize }}</option>
      </select>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  export default {
    data () {
      return {
        selected: '',
        pages: [
          'test'
        ]
      }
    },

    methods: {
      handleSelect () {
        const parser = document.createElement('a')
        parser.href = window.location.href

        const url = `${parser.protocol}//${parser.hostname}:${parser.port}`

        window.location = `${url}/frontend/${this.selected}/`
      }
    }
  }
</script>

<style scoped>
  .fs-Outer {
    position: fixed;
    top: 10px;
    left: 10px;

    align-items: center;

    display: flex;
    padding: 10px;
    width: 300px;

    background-color: #fff;
    border: 1px solid #dedede;
    border-radius: 3px;
    opacity: 0.3;

    transition: opacity 0.18s ease;
    will-change: transform;
  }

  .fs-Outer:hover {
    opacity: 1;
  }

  .fs-Input {
    position: relative;

    align-items: center;
    flex: 1;

    display: flex;
  }

  .fs-Label {
    flex-shrink: 0;

    display: block;
    margin-right: 10px;

    font-size: 14px;
  }

  .fs-Switcher {
    width: 100%;
  }
</style>