import { ApiService } from "@/services/api/api.service";

export class FeedbackResource extends ApiService {
  constructor() {
    super();
  }

  // Публичная форма обратной связи
  sendFeedback(data) {
    return this.$post(`/api/v1/feedback/`, data);
  }

  // --- Админка ---
  getFeedback(config) {
    return this.$get(`/api/v1/feedback/`, config);
  }

  getFeedbackStats() {
    return this.$get(`/api/v1/feedback/stats/`);
  }

  updateFeedback(id, data) {
    return this.$patch(`/api/v1/feedback/${id}/`, data);
  }

  resendFeedback(id) {
    return this.$post(`/api/v1/feedback/${id}/resend/`);
  }

  deleteFeedback(id) {
    return this.$delete(`/api/v1/feedback/${id}/`);
  }
}
