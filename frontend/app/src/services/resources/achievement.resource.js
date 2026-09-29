import { ApiService } from "@/services/api/api.service";

export class AchievementResource extends ApiService {
  getAchievements(config) {
    return this.$get("/api/v1/achievements/", config);
  }

  getAdminAchievements(config) {
    return this.$get("/api/v1/achievements/admin/", config);
  }

  createAchievement(data) {
    return this.$post("/api/v1/achievements/", data);
  }

  updateAchievement(id, data) {
    return this.$patch(`/api/v1/achievements/${id}/`, data);
  }

  deleteAchievement(id) {
    return this.$delete(`/api/v1/achievements/${id}/`);
  }
}
