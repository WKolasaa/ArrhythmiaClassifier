<script setup>
import { RouterView } from 'vue-router'
import { Dark, useQuasar } from 'quasar'
import { useAuthStore } from './stores/auth'
import { computed } from 'vue'

const $q = useQuasar()
function toggleDarkMode () {
  Dark.toggle()
}

const auth = useAuthStore()
const isLoggedIn = computed(() => !!auth.user)

function handleLogout () {
  auth.logout()
}
</script>

<template>
  <q-layout view="lHh Lpr lFf" class="bg-background text-primary">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>Arrhythmia App</q-toolbar-title>
        <q-space />
        <q-btn flat label="Home" to="/" />

        <q-btn v-if="!isLoggedIn" flat label="Login" to="/login" />
        <q-btn v-if="!isLoggedIn" flat label="Register" to="/register" />
        <q-btn v-else flat label="Logout" @click="handleLogout" />

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
