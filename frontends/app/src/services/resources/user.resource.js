import { ApiService } from "@/services/api/api.service";
import { authClient } from "@/services/api/axios.clients";

export class UserResource extends ApiService {
  constructor() {
    super();
    this.client = authClient;
  }

  getUsers(params) {
    return this.$get(`/api/v1/users/`, params);
  }

  createUser(data) {
    return this.$post(`/api/v1/users/`, data);
  }

  updateUser(id, data) {
    return this.$patch(`/api/v1/users/${id}/`, data);
  }

  deleteUser(id) {
    return this.$delete(`/api/v1/users/${id}/`);
  }

  resetPassword(id, data) {
    return this.$patch(`/api/v1/users/${id}/reset-password/`, data);
  }

  uploadPhoto(id, data) {
    return this.$patch(`/api/v1/users/${id}/photo/`, data);
  }

  deletePhoto(id) {
    return this.$delete(`/api/v1/users/${id}/photo/`);
  }
}