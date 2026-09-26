import { defineStore } from "pinia";
import resources from "@/services/resources";


export const useFeedbackStore = defineStore("feedback", {
  state: () => ({}),
  getters: {

  },
  actions: {
    // Отправка сообщения обратной связи
    async sendFeedback(data) {
      const res = await resources.feedback.sendFeedback(data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Список обращений (админка)
    async loadFeedback(config) {
      const res = await resources.feedback.getFeedback(config);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Счётчики обращений (админка)
    async loadFeedbackStats() {
      const res = await resources.feedback.getFeedbackStats();
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Изменение статуса / заметки
    async updateFeedback(id, data) {
      const res = await resources.feedback.updateFeedback(id, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Повторная отправка письма
    async resendFeedback(id) {
      const res = await resources.feedback.resendFeedback(id);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Удаление обращения
    async deleteFeedback(id) {
      const res = await resources.feedback.deleteFeedback(id);
      if (res.__state === "success") {
        return true
      }
      return null
    },
  },
})
