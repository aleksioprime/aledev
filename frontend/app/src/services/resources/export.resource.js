import { ApiService } from "@/services/api/api.service";

export class ExportResource extends ApiService {
  exportPortfolio(lang) {
    return this.$get("/api/v1/export/portfolio/", { params: { lang }, responseType: "blob" });
  }
}
