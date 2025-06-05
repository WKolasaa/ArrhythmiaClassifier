<script setup>
import { RouterView, useRouter } from 'vue-router'
import { Dark, useQuasar } from 'quasar'
import { useAuthStore } from './stores/auth'
import { computed } from 'vue'

const $q = useQuasar()
const router = useRouter()
const auth = useAuthStore()

const isLoggedIn = computed(() => !!auth.user)

function toggleDarkMode() {
  Dark.toggle()
}

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>

<template>
  <q-layout view="lHh Lpr lFf" class="bg-background text-primary">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>Arrhythmia App</q-toolbar-title>
        <q-space />

        <!-- Navigation Buttons -->
        <q-btn v-if="isLoggedIn" flat label="Admin" to="/adminoverview" />
        <q-btn v-if="isLoggedIn" flat label="Dashboard" to="/dashboard" />
        <q-btn v-if="!isLoggedIn" flat label="Home" to="/" />
        <q-btn v-if="!isLoggedIn" flat label="Login" to="/login" />
        <q-btn v-if="!isLoggedIn" flat label="Register" to="/register" />
        <q-btn v-else flat label="Logout" @click="handleLogout" />

        <!-- Theme Toggle -->
        <q-btn flat round dense :icon="$q.dark.isActive ? 'light_mode' : 'dark_mode'" @click="toggleDarkMode" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <RouterView />
    </q-page-container>
  </q-layout>
</template>

<style>
html,
body,
#app {
  height: 100%;
  margin: 0;
}
</style>
