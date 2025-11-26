// Data Persistence Layer
//
// AI Development Notice:
// This code was developed with AI assistance (GitHub Copilot, Claude).
// All code has been reviewed, tested, and validated by human developers.

import { CONFIG } from "./config.js";

export class StorageManager {
  constructor() {
    this.storageKey = CONFIG.STORAGE_KEY;
  }

  /**
   * Save user preferences to localStorage
   * @param {Array} preferences - Array of preference objects
   * @returns {boolean} Success status
   */
  savePreferences(preferences) {
    try {
      const data = {
        preferences,
        lastUpdated: new Date().toISOString(),
      };
      localStorage.setItem(this.storageKey, JSON.stringify(data));
      return true;
    } catch (error) {
      console.error("Failed to save preferences:", error);
      return false;
    }
  }

  /**
   * Load user preferences from localStorage
   * @returns {Array} Array of preference objects or default data
   */
  loadPreferences() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (!stored) {
        return this.getDefaultPreferences();
      }

      const data = JSON.parse(stored);
      return data.preferences || this.getDefaultPreferences();
    } catch (error) {
      console.error("Failed to load preferences:", error);
      return this.getDefaultPreferences();
    }
  }

  /**
   * Clear all stored preferences
   */
  clearPreferences() {
    try {
      localStorage.removeItem(this.storageKey);
      return true;
    } catch (error) {
      console.error("Failed to clear preferences:", error);
      return false;
    }
  }

  /**
   * Get default preferences
   * @returns {Array} Default preference data
   */
  getDefaultPreferences() {
    return [
      {
        title: "Beacon 23",
        user_rating: 6,
        media_type: "TV",
        themes: ["isolation", "psychological", "mystery"],
      },
      {
        title: "Star Trek TNG",
        user_rating: 9,
        media_type: "TV",
        themes: ["philosophy", "character_development", "moral_dilemmas"],
      },
      {
        title: "Discovery",
        user_rating: 5,
        media_type: "TV",
        themes: ["visual_effects", "complex_story", "mixed_reception"],
      },
      {
        title: "Deep Space Nine",
        user_rating: 8,
        media_type: "TV",
        themes: ["political_intrigue", "character_arcs", "moral_complexity"],
      },
      {
        title: "Voyager",
        user_rating: 8,
        media_type: "TV",
        themes: ["exploration", "character_development", "alien_cultures"],
      },
      {
        title: "Enterprise",
        user_rating: 9,
        media_type: "TV",
        themes: ["prequel", "exploration", "character_arcs"],
      },
      {
        title: "Strange New Worlds",
        user_rating: 7,
        media_type: "TV",
        themes: ["episodic", "character_development", "nostalgia"],
      },
      {
        title: "Dark Matter 2015",
        user_rating: 7,
        media_type: "TV",
        themes: ["memory_loss", "ensemble_cast", "mystery"],
      },
      {
        title: "Dark Matter 2024",
        user_rating: 6,
        media_type: "TV",
        themes: ["new_concept", "mixed_execution", "potential"],
      },
      {
        title: "3 Body Problem",
        user_rating: 9,
        media_type: "TV",
        themes: ["hard_sci_fi", "philosophical", "real_science"],
      },
      {
        title: "Monarch",
        user_rating: 8,
        media_type: "TV",
        themes: ["monster_universe", "visual_effects", "human_drama"],
      },
      {
        title: "Fallout TV",
        user_rating: 9,
        media_type: "TV",
        themes: ["post_apocalyptic", "humor", "video_game_adaptation"],
      },
      {
        title: "Dark",
        user_rating: 9,
        media_type: "TV",
        themes: ["time_travel", "complex_narrative", "philosophy"],
      },
      {
        title: "For All Mankind",
        user_rating: 9,
        media_type: "TV",
        themes: ["alternate_history", "space_exploration", "realism"],
      },
      {
        title: "Fallout NV",
        user_rating: 9,
        media_type: "Game",
        themes: ["player_choice", "moral_complexity", "world_building"],
      },
      {
        title: "Mass Effect",
        user_rating: 8,
        media_type: "Game",
        themes: ["character_development", "space_opera", "moral_choices"],
      },
      {
        title: "Minecraft",
        user_rating: 10,
        media_type: "Game",
        themes: ["creativity", "building", "exploration"],
      },
      {
        title: "Witcher 3",
        user_rating: 9,
        media_type: "Game",
        themes: ["open_world", "storytelling", "moral_complexity"],
      },
      {
        title: "Half-Life 2",
        user_rating: 10,
        media_type: "Game",
        themes: ["physics_gameplay", "storytelling", "innovation"],
      },
      {
        title: "Horizon Zero Dawn",
        user_rating: 9,
        media_type: "Game",
        themes: ["open_world", "exploration", "unique_setting"],
      },
      {
        title: "GTA V",
        user_rating: 10,
        media_type: "Game",
        themes: ["open_world", "freedom", "immersion"],
      },
    ];
  }

  /**
   * Export preferences as JSON file
   */
  exportPreferences() {
    try {
      const preferences = this.loadPreferences();
      const dataStr = JSON.stringify(preferences, null, 2);
      const dataBlob = new Blob([dataStr], { type: "application/json" });
      const url = URL.createObjectURL(dataBlob);

      const link = document.createElement("a");
      link.href = url;
      link.download = `preferences_${
        new Date().toISOString().split("T")[0]
      }.json`;
      link.click();

      URL.revokeObjectURL(url);
      return true;
    } catch (error) {
      console.error("Failed to export preferences:", error);
      return false;
    }
  }
}
