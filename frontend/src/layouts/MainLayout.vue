<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>

        <q-toolbar-title>
          Arrhythmia App
        </q-toolbar-title>

        <q-btn flat label="Home" to="/" />
        <q-btn flat v-if="!isLoggedIn" label="Login" to="/login" />
        <q-btn flat v-if="!isLoggedIn" label="Register" to="/register" />
        <q-btn flat v-if="isLoggedIn" label="Dashboard" to="/dashboard" />
        <q-btn flat v-if="isLoggedIn" label="Logout" @click="logout" />
      </q-toolbar>
    </q-header>

    <q-page-container class="q-pa-md">
      <slot />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'

// TODO: Replace with actual auth logic or Pinia later
const isLoggedIn = ref(false)

function logout() {
  isLoggedIn.value = false
  // Redirect or clean auth token here later
}
</script>
