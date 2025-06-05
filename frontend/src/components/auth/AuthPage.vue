<template>
  <div class="q-pa-md flex flex-center full-height">
    <q-card class="q-pa-lg shadow-2 auth-card">
      <LoginForm v-if="mode === 'login'" @switch="mode = $event" />
      <RegisterForm v-else @switch="mode = $event" />
    </q-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'
</script>

<style scoped>
.auth-card {
  width: 400px;
  max-width: 90vw;
  background: white;
  color: black;
  border-radius: 8px;
}
</style>
