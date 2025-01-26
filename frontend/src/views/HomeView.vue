<template>
  <div>
    <h1>Welcome to the Learning CMS!</h1>
    <button @click="fetchData">Fetch Data from Backend</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: ''
    }
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('/api/');  // 访问后端 API
        const data = await response.json();
        this.message = data.message;
      } catch (error) {
        this.message = 'Failed to fetch data from backend';
      }
    }
  }
}
</script> 