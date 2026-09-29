import { defineStore } from "pinia";
import resources from "@/services/resources";

export const useAchievementStore = defineStore("achievement", {
  actions: {
    async loadAchievements(config) {
      const response = await resources.achievement.getAchievements(config);
      return response.__state === "success" ? response.data : null;
    },
    async loadAdminAchievements(config) {
      const response = await resources.achievement.getAdminAchievements(config);
      return response.__state === "success" ? response.data : null;
    },
    async createAchievement(data) {
      const response = await resources.achievement.createAchievement(data);
      return response.__state === "success" ? response.data : null;
    },
    async updateAchievement(id, data) {
      const response = await resources.achievement.updateAchievement(id, data);
      return response.__state === "success" ? response.data : null;
    },
    async deleteAchievement(id) {
      const response = await resources.achievement.deleteAchievement(id);
      return response.__state === "success" ? true : null;
    },
  },
});
