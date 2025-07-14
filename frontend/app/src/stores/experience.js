import { defineStore } from "pinia";
import resources from "@/services/resources";


export const useExperienceStore = defineStore("experience", {
  state: () => ({}),
  getters: {

  },
  actions: {
    // Загрузка списка записей об опыте работы (пагинированный)
    async loadExperiences(config) {
      const res = await resources.experience.getExperiences(config);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Добавление записи об опыте работы
    async createExperience(data) {
      const res = await resources.experience.createExperience(data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Редактирование записи об опыте работы
    async updateExperience(id, data) {
      const res = await resources.experience.updateExperience(id, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Удаление записи об опыте работы
    async deleteExperience(id) {
      const res = await resources.experience.deleteExperience(id);
      if (res.__state === "success") {
        return true
      }
      return null
    },
    // Добавление перевода
    async addTranslationToExperience(id, data) {
      const res = await resources.experience.addTranslationToExperience(id, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Редактирование перевода
    async updateTranslationInExperience(id, lang, data) {
      const res = await resources.experience.updateTranslationInExperience(id, lang, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Удаление перевода
    async deleteTranslationFromExperience(id, lang) {
      const res = await resources.experience.deleteTranslationFromExperience(id, lang);
      if (res.__state === "success") {
        return true
      }
      return null
    },
  },
})