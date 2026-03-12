import { ApiService } from "@/services/api/api.service";
import { authClient } from "@/services/api/axios.clients";

export class AuthResource extends ApiService {
  constructor() {
    super(authClient);
  }

  whoAmI() {
    return this.$get(`/api/v1/users/me/`);
  }

  login(data) {
    return this.$post(`/api/v1/login/`, data);
  }

  refresh(params) {
    return this.$post(`/api/v1/refresh/`, params);
  }

  logout(params) {
    return this.$post(`/api/v1/logout/`, params);
  }
}