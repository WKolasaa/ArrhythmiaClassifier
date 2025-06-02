<template>
  <MainLayout>
    <div class="q-pa-md">
      <div class="text-h4 q-mb-md">Welcome to the Fighter Jet EKG Classifier</div>
      <p>This tool helps classify arrhythmia in pilots using EKG data.</p>
      <q-separator spaced />
      <p>
        Please <q-btn flat color="primary" to="/login" label="Login" /> or
        <q-btn flat color="secondary" to="/register" label="Register" /> to get started.
      </p>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/layouts/MainLayout.vue'
</script>
