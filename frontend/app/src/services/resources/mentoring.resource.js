import { ApiService } from "@/services/api/api.service";

export class MentoringResource extends ApiService {
  getMentoringContent() {
    return this.$get("/api/v1/mentoring/");
  }

  getAdminMentoringContent() {
    return this.$get("/api/v1/mentoring/admin/");
  }

  updateMentoringContent(data) {
    return this.$put("/api/v1/mentoring/", data);
  }
}
