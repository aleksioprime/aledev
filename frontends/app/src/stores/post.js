import { defineStore } from "pinia";
import resources from "@/services/resources";

export const usePostStore = defineStore("post", {
  state: () => ({
    posts: [],
    currentPost: null,
    loading: false,
    error: null,
    pagination: {
      total: 0,
      page: 1,
      perPage: 10
    }
  }),

  getters: {
    getPostBySlug: (state) => (slug) => {
      return state.posts.find(post => post.slug === slug);
    },
    getPostById: (state) => (id) => {
      return state.posts.find(post => post.id === id);
    },
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error
  },

  actions: {
    setLoading(loading) {
      this.loading = loading;
    },

    setError(error) {
      this.error = error;
    },

    clearError() {
      this.error = null;
    },

    // Загрузка списка постов (пагинированный)
    async loadPosts(config = {}) {
      this.setLoading(true);
      this.clearError();

      try {
        const res = await resources.post.getPosts(config);
        if (res.__state === "success") {
          this.posts = res.data.items || res.data;
          if (res.data.pagination) {
            this.pagination = { ...this.pagination, ...res.data.pagination };
          }
          return res.data;
        } else {
          this.setError('Ошибка загрузки постов');
          return null;
        }
      } catch (error) {
        this.setError(error.message || 'Ошибка загрузки постов');
        return null;
      } finally {
        this.setLoading(false);
      }
    },

    // Загрузка конкретного поста
    async loadPost(identifier) {
      this.setLoading(true);
      this.clearError();

      try {
        // Если передан slug, ищем по slug, иначе по id
        const res = await resources.post.getPost(identifier);
        if (res.__state === "success") {
          this.currentPost = res.data;
          return res.data;
        } else {
          this.setError('Пост не найден');
          return null;
        }
      } catch (error) {
        this.setError(error.message || 'Ошибка загрузки поста');
        return null;
      } finally {
        this.setLoading(false);
      }
    },

    // Добавление поста
    async createPost(data) {
      this.setLoading(true);
      this.clearError();

      try {
        const res = await resources.post.createPost(data);
        if (res.__state === "success") {
          this.posts.unshift(res.data); // Добавляем в начало списка
          return res.data;
        } else {
          this.setError('Ошибка создания поста');
          return null;
        }
      } catch (error) {
        this.setError(error.message || 'Ошибка создания поста');
        return null;
      } finally {
        this.setLoading(false);
      }
    },

    // Редактирование поста
    async updatePost(id, data) {
      this.setLoading(true);
      this.clearError();

      try {
        const res = await resources.post.updatePost(id, data);
        if (res.__state === "success") {
          // Обновляем пост в списке
          const index = this.posts.findIndex(post => post.id === id);
          if (index !== -1) {
            this.posts[index] = res.data;
          }
          // Обновляем текущий пост, если он совпадает
          if (this.currentPost && this.currentPost.id === id) {
            this.currentPost = res.data;
          }
          return res.data;
        } else {
          this.setError('Ошибка обновления поста');
          return null;
        }
      } catch (error) {
        this.setError(error.message || 'Ошибка обновления поста');
        return null;
      } finally {
        this.setLoading(false);
      }
    },

    // Удаление поста
    async deletePost(id) {
      this.setLoading(true);
      this.clearError();

      try {
        const res = await resources.post.deletePost(id);
        if (res.__state === "success") {
          // Удаляем из списка
          this.posts = this.posts.filter(post => post.id !== id);
          // Очищаем текущий пост, если он был удален
          if (this.currentPost && this.currentPost.id === id) {
            this.currentPost = null;
          }
          return true;
        } else {
          this.setError('Ошибка удаления поста');
          return false;
        }
      } catch (error) {
        this.setError(error.message || 'Ошибка удаления поста');
        return false;
      } finally {
        this.setLoading(false);
      }
    },

    // Очистка данных
    clearPosts() {
      this.posts = [];
      this.currentPost = null;
      this.pagination = {
        total: 0,
        page: 1,
        perPage: 10
      };
    },

    setCurrentPost(post) {
      this.currentPost = post;
    },

    clearCurrentPost() {
      this.currentPost = null;
    }
  },
})