<script setup>
import { RouterView } from 'vue-router'
import { Dark, useQuasar } from 'quasar'

const $q = useQuasar()
function toggleDarkMode() {
  Dark.toggle()
}
</script>

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
          label="Toggle Dark Mode"
          @click="toggleDarkMode"
        />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <RouterView />
    </q-page-container>
  </q-layout>
</template>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
}
</style>
