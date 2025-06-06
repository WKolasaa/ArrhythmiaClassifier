<template>
  <q-page class="flex flex-center column q-pa-xl bg-grey-1 text-dark">
    <q-card flat bordered class="q-pa-xl" style="max-width: 600px; width: 100%">
      <q-card-section class="text-center">
        <q-icon name="favorite" size="64px" color="primary" class="q-mb-md" />
        <div class="text-h5 text-weight-bold">
          Fighter Jet EKG Arrhythmia Classifier
        </div>
        <div class="text-subtitle2 q-mt-sm">
          A precision tool for analyzing pilot EKG data to detect arrhythmias efficiently.
        </div>
      </q-card-section>

      <q-separator class="q-my-lg" />

      <q-card-section class="text-center">
        <div class="text-body1 q-mb-sm">
          Access powerful insights into cardiac rhythms and streamline your diagnosis workflow.
        </div>
        <div class="q-gutter-md q-mt-md row justify-center">
          <q-btn color="primary" to="/login" label="Login" unelevated />
          <q-btn color="secondary" to="/register" label="Register" outline />
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>
