<template>
  <div class="q-pa-md flex flex-center">
    <q-card class="q-pa-lg shadow-2" style="max-width: 400px; width: 100%">
      <q-card-section class="text-h6 text-center text-primary">
        Register
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
        <q-input
          v-model="confirmPassword"
          label="Confirm Password"
          type="password"
          outlined
          class="q-mb-md"
        />

        <q-btn
          label="Register"
          color="primary"
          unelevated
          class="full-width q-mt-sm"
          @click="handleRegister"
        />

        <div class="q-mt-md text-center">
          <router-link to="/login" class="text-primary">
            Already have an account? <strong>Login</strong>
          </router-link>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { errorMessages } from "vue/compiler-sfc";

const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const router = useRouter();
const auth = useAuthStore();

async function handleRegister() {
  try {
    if (!email.value || !password.value || !confirmPassword.value) {
      alert("Please fill out all fields.");
      return;
    }

    if (password.value !== confirmPassword.value) {
      alert("Passwords do not match.");
      return;
    }

    const success = await auth.register(email.value, password.value);
    if (success) {
      alert("Registration successful! Please log in.");
      router.push("/login");
    } else {
      alert("Registration failed.");
    }
  } catch (error) {
    console.error(error);
  };
}
</script>
