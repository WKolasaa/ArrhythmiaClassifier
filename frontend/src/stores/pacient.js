import { defineStore } from "pinia";
import axios from "../plugins/axios";

export const usePatientStore = defineStore("PatientStore", {
  state: () => ({
    all: [],
    selectedPatient: null,
  }),

  actions: {
    async fetchAllPatients() {
      try {
        const res = await axios.get(`/patients`);
        this.all = res.data;
      } catch (err) {
        this.error = err;
        console.log("Failed to fetch all patients: ", err);
      }
    },

    async fetchPatientDetails(patientId) {
      try {
        const res = await axios.get(`/patients/${patientId}`);
        this.selectedPatient = res.data;
      } catch (err) {
        this.error = err;
        console.log("Failed to fetch the selected patient: ", err);
      }
    },
  },
});
