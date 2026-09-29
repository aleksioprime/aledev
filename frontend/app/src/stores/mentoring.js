import { defineStore } from "pinia";
import resources from "@/services/resources";

export const useMentoringStore = defineStore("mentoring", {
  actions: {
    async loadMentoringContent() {
      const response = await resources.mentoring.getMentoringContent();
      return response.__state === "success" ? response.data : null;
    },
    async loadAdminMentoringContent() {
      const response = await resources.mentoring.getAdminMentoringContent();
      return response.__state === "success" ? response.data : null;
    },
    async updateMentoringContent(data) {
      const response = await resources.mentoring.updateMentoringContent(data);
      return response.__state === "success" ? response.data : null;
    },
  },
});
