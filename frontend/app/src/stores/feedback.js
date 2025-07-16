import { defineStore } from "pinia";
import resources from "@/services/resources";


export const useFeedbackStore = defineStore("feedback", {
  state: () => ({}),
  getters: {

  },
  actions: {
    // Отправь сообщение обратной связи
    async sendFeedback(data) {
      const res = await resources.feedback.sendFeedback(data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
  },
})