<template>
  <q-form @submit.prevent="onLogin">
    <q-input v-model="email" label="Email" type="email" filled />
    <q-input v-model="password" label="Password" type="password" filled class="q-mt-md" />
    <div class="q-mt-md">
      <q-btn type="submit" label="Login" color="primary" class="full-width" />
    </div>
    <div class="q-mt-sm text-center">
      <q-btn flat label="Don't have an account? Register" @click="$emit('switch', 'register')" />
    </div>
  </q-form>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')

function onLogin() {
  console.log('Login:', email.value, password.value)
  // Call backend API here later
}
</script>
