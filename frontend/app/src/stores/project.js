import { defineStore } from "pinia";
import resources from "@/services/resources";


export const useProjectStore = defineStore("project", {
  state: () => ({}),
  getters: {

  },
  actions: {
    // Загрузка списка проектов (пагинированный)
    async loadProjects(config) {
      const res = await resources.project.getProjects(config);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Добавление проекта
    async createProject(data) {
      const res = await resources.project.createProject(data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Редактирование проекта
    async updateProject(id, data) {
      const res = await resources.project.updateProject(id, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Удаление проекта
    async deleteProject(id) {
      const res = await resources.project.deleteProject(id);
      if (res.__state === "success") {
        return true
      }
      return null
    },
    // Добавление перевода
    async addTranslationToProject(id, data) {
      const res = await resources.project.addTranslationToProject(id, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Редактирование перевода
    async updateTranslationInProject(id, lang, data) {
      const res = await resources.project.updateTranslationInProject(id, lang, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Удаление перевода
    async deleteTranslationFromProject(id, lang) {
      const res = await resources.project.deleteTranslationFromProject(id, lang);
      if (res.__state === "success") {
        return true
      }
      return null
    },
    // Изменение порядка
    async reorderProjects(data) {
      const res = await resources.project.reorderProjects(data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
  },
})