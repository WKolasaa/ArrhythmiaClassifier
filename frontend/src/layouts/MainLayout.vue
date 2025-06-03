<template>
  <q-layout view="lHh Lpr lFf" class="bg-background text-primary">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>Arrhythmia App</q-toolbar-title>
        <q-space />
        <q-btn flat label="Home" to="/" />
        <q-btn flat label="Login" to="/login" />
        <q-btn flat label="Register" to="/register" />
        <q-btn
          flat
          round
          dense
          icon="brightness_6"
          @click="toggleDarkMode"
        />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <RouterView />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { Dark } from 'quasar'
import { computed } from 'vue'

const layoutClass = computed(() =>
  Dark.isActive ? 'bg-dark text-white' : 'bg-white text-black'
)
</script>

<style scoped>
.q-layout {
  min-height: 100vh;
}
</style>
