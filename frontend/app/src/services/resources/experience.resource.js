import { ApiService } from "@/services/api/api.service";

export class ExperienceResource extends ApiService {
  constructor() {
    super();
  }

  getExperiences(params) {
    return this.$get(`/api/v1/experiences/`, params);
  }

  createExperience(data) {
    return this.$post(`/api/v1/experiences/`, data);
  }

  updateExperience(id, data) {
    return this.$patch(`/api/v1/experiences/${id}/`, data);
  }

  deleteExperience(id) {
    return this.$delete(`/api/v1/experiences/${id}/`);
  }

  addTranslationToExperience(data) {
    return this.$post(`/api/v1/experiences/${id}/translation/`, data);
  }

  updateTranslationInExperience(id, lang, data) {
    return this.$patch(`/api/v1/experiences/${id}/translation/${lang}`, data);
  }

  deleteTranslationFromExperience(id, lang) {
    return this.$delete(`/api/v1/experiences/${id}/translation/${lang}`);
  }
}