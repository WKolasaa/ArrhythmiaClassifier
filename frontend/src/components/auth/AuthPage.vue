<template>
  <div>
    <LoginForm v-if="mode === 'login'" @switch="mode = $event" />
    <RegisterForm v-else @switch="mode = $event" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'

const mode = ref('login')
</script>
