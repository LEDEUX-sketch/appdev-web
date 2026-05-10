<script setup>
import { useRoute } from 'vue-router'
import AppSidebar from './components/AppSidebar.vue'

const route = useRoute()

const isFullPage = () => {
  return route.name === 'Login' || route.name === 'Landing'
}
</script>

<template>
  <div id="app" :class="{ 'has-sidebar': !isFullPage() }">
    <AppSidebar v-if="route.name && !isFullPage()" />
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<style scoped>
#app {
  width: 100%;
}
.has-sidebar .main-content {
  margin-left: 290px;
  padding: 20px 20px 20px 0;
  min-height: 100vh;
}
</style>
