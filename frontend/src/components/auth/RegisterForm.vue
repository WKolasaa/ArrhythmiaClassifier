<template>
  <q-form @submit.prevent="onRegister">
    <q-input v-model="email" label="Email" type="email" filled />
    <q-input v-model="password" label="Password" type="password" filled class="q-mt-md" />
    <q-input v-model="confirmPassword" label="Confirm Password" type="password" filled class="q-mt-md" />
    <div class="q-mt-md">
      <q-btn type="submit" label="Register" color="primary" class="full-width" />
    </div>
    <div class="q-mt-sm text-center">
      <q-btn flat label="Already have an account? Login" @click="$emit('switch', 'login')" />
    </div>
  </q-form>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const confirmPassword = ref('')

function onRegister() {
  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match')
    return
  }
  console.log('Register:', email.value, password.value)
  // Call backend API here later
}
</script>
