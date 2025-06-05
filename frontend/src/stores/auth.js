import { defineStore } from "pinia";
import axios from "../plugins/axios"; // Make sure this path is correct and axios is properly set up

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
        const res = await axios.post("/auth/login", {
          email: email,
          password: password,
        });
        this.user = res.data.user;
        this.token = res.data.token;
        localStorage.setItem("token", this.token);
        return true;
      } catch (error) {
        this.error = error;
        console.error("Login failed:", error);
        return false;
      }
    },

    async register(email, password) {
      try {
        const res = await axios.post("/auth/register", {
          email: email,
          password: password,
          role: "doctor",
        });
        console.log("Register response:", res.data);
        return true;
      } catch (error) {
        this.error = error;
        console.error("Register failed:", error);
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
