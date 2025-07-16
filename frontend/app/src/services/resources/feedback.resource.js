import { ApiService } from "@/services/api/api.service";

export class FeedbackResource extends ApiService {
  constructor() {
    super();
  }

  sendFeedback(data) {
    return this.$post(`/api/v1/feedback/`, data);
  }
}