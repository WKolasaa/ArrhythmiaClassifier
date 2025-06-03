<template>
  <div class="q-pa-md flex flex-center">
    <q-card class="q-pa-lg shadow-2" style="max-width: 400px; width: 100%;">
      <q-card-section class="text-h6 text-center text-primary">
        Login
      </q-card-section>

      <q-card-section>
        <q-input
          v-model="email"
          label="Email"
          type="email"
          outlined
          class="q-mb-md"
        />
        <q-input
          v-model="password"
          label="Password"
          type="password"
          outlined
          class="q-mb-md"
        />

        <q-btn
          label="Login"
          color="primary"
          unelevated
          class="full-width q-mt-sm"
          @click="handleLogin"
        />

        <div class="q-mt-md text-center">
          <router-link to="/register" class="text-primary">
            Don't have an account? <strong>Register</strong>
          </router-link>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')

function handleLogin () {
  if (!email.value || !password.value) {
    alert('Please fill in both fields.')
    return
  }

  console.log('Logging in with:', email.value)
  // TODO: hook into backend or auth flow
}
</script>
