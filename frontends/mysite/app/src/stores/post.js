import { defineStore } from "pinia";
import resources from "@/services/resources";


export const usePostStore = defineStore("post", {
  state: () => ({}),
  getters: {

  },
  actions: {
    // Загрузка списка постов (пагинированный)
    async loadPosts(config) {
      const res = await resources.post.getPosts(config);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Добавление поста
    async createPost(data) {
      const res = await resources.post.createPost(data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Редактирование поста
    async updatePost(id, data) {
      const res = await resources.post.updatePost(id, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Удаление поста
    async deletePost(id) {
      const res = await resources.post.deletePost(id);
      if (res.__state === "success") {
        return true
      }
      return null
    },
  },
})