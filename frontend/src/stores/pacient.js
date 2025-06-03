import { defineStore } from "pinia";

export const usePacientStore = defineStore("PatientStore", {
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

    async fetchPatientDetails(pacientId) {
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
