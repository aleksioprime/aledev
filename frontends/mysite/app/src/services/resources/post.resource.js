import { ApiService } from "@/services/api/api.service";
import { blogClient } from "@/services/api/axios.clients";

export class PostResource extends ApiService {
  constructor() {
    super(blogClient);
  }

  getPosts(params) {
    return this.$get(`/api/v1/posts/`, params);
  }

  createPost(data) {
    return this.$post(`/api/v1/posts/`, data);
  }

  updatePost(id, data) {
    return this.$patch(`/api/v1/posts/${id}/`, data);
  }

  deletePost(id) {
    return this.$delete(`/api/v1/posts/${id}/`);
  }
}