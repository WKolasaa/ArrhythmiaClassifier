import { defineStore } from "pinia";
import axios from "../plugins/axios";
import { useRouter } from "vue-router";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: null,
    email: null,
    error: null,
  }),
  actions: {
    async login(email, password) {
      try {
        const response = await api.post("/auth/login", { email, password });
        this.user = response.data.user;
        this.token = response.data.token;
        localStorage.setItem("token", this.token);
        return true;
      } catch (error) {
        console.error(
          "Login failed:",
          error.response?.data?.message || error.message
        );
        return false;
      }
    },

    async register(email, password) {
      try {
        const res = await axios.post("/auth/register", {
          email: email,
          password: password,
          role: 'doctor',
        });
        console.log("Register response:", res.data);
        return true;
      } catch (error) {
        this.error = error;
        console.error(
          "Register failed:", error
        );
        return false;
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("token");
    },
  },
});
