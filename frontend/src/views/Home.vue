<template>
  <q-page class="flex flex-center column q-pa-lg bg-background text-primary">
    <div class="text-h4 text-center q-mb-md">
      Welcome to the Fighter Jet EKG Classifier
    </div>
    <div class="text-body1 q-mb-sm text-center">
      This tool helps classify arrhythmia in pilots using EKG data.
    </div>
    <q-separator class="q-my-md" />
    <div class="text-center">
      Please
      <q-btn flat color="primary" to="/login" label="Login" />
      or
      <q-btn flat color="secondary" to="/register" label="Register" />
      to get started.
    </div>
  </q-page>
</template>
