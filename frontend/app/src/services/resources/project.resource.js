import { ApiService } from "@/services/api/api.service";

export class ProjectResource extends ApiService {
  constructor() {
    super();
  }

  getProjects(params) {
    return this.$get(`/api/v1/projects/`, params);
  }

  createProject(data) {
    return this.$post(`/api/v1/projects/`, data);
  }

  updateProject(id, data) {
    return this.$patch(`/api/v1/projects/${id}/`, data);
  }

  deleteProject(id) {
    return this.$delete(`/api/v1/projects/${id}/`);
  }

  addTranslationToProject(id, data) {
    return this.$post(`/api/v1/projects/${id}/translation/`, data);
  }

  updateTranslationInProject(project_id, lang, data) {
    return this.$patch(`/api/v1/projects/${project_id}/translation/${lang}`, data);
  }

  deleteTranslationFromProject(project_id, lang) {
    return this.$delete(`/api/v1/projects/${project_id}/translation/${lang}`);
  }

  reorderProjects(data) {
    return this.$post(`/api/v1/projects/reorder/`, data);
  }
}