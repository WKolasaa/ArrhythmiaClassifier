<template>
  <q-page class="q-pa-md flex flex-center">
    <div class="row items-center justify-around full-width q-col-gutter-xl">
      <!-- Jet Image -->
      <div class="col-12 col-md-8">
        <q-img
          src="/images/jet_ekg.jpg"
          alt="Jet fighter"
          style="border-radius: 12px;"
        />
      </div>

      <!-- Text + Buttons -->
      <div class="col-12 col-md-4 flex column justify-center" style="min-height: 400px;">
        <div class="text-h4 text-bold text-primary">
          Fighter Jet EKG Arrhythmia Classifier
        </div>
        <div class="text-body1 q-mt-sm">
          A high-precision diagnostic interface for hyperspace pilots. Use real EKG data to detect arrhythmias and improve mission safety.
        </div>
        <q-banner class="bg-blue-1 text-blue-10 q-pa-sm q-mt-sm" dense>
          Empowering doctors with real-time analysis tools for cardiac health optimization.
        </q-banner>

        <div class="row q-col-gutter-sm q-mt-md">
          <q-btn to="/login" label="Login" color="primary" unelevated  size="lg"/>
          <q-btn to="/register" label="Register" color="primary" flat size="lg"/>
        </div>
      </div>
    </div>
  </q-page>
</template>
