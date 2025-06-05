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
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const router = useRouter()
const auth = useAuthStore()

async function handleLogin() {
  const success = await auth.login(email.value, password.value)
  if (success) {
    router.push('/dashboard') // redirect after login
  } else {
    alert('Login failed')
  }
}
</script>