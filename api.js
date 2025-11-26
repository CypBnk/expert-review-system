// API Communication Layer
import { CONFIG } from "./config.js";

export class APIClient {
  constructor(baseURL = CONFIG.API_BASE_URL) {
    this.baseURL = baseURL;
    this.timeout = CONFIG.REQUEST_TIMEOUT;
  }

  /**
   * Generic fetch wrapper with timeout and error handling
   * @private
   */
  async _fetch(endpoint, options = {}) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        signal: controller.signal,
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(
          error.message || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error.name === "AbortError") {
        throw new Error("Request timeout - please try again");
      }

      throw error;
    }
  }

  /**
   * Analyze a media title
   * @param {Object} titleData - Title information
   * @returns {Promise<Object>} Analysis results
   */
  async analyzeTitle(titleData) {
    try {
      // Validate input
      this._validateTitleData(titleData);

      // Map title to name for backend compatibility
      const payload = { ...titleData };
      if (payload.title && !payload.name) {
        payload.name = payload.title;
      }

      return await this._fetch("/analyze", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    } catch (error) {
      console.error("Analysis request failed:", error);
      throw new Error(`Failed to analyze title: ${error.message}`);
    }
  }

  /**
   * Get system metrics
   * @returns {Promise<Object>} System metrics
   */
  async getMetrics() {
    try {
      return await this._fetch("/metrics", {
        method: "GET",
      });
    } catch (error) {
      console.error("Failed to fetch metrics:", error);
      throw error;
    }
  }

  /**
   * Validate title data before sending
   * @private
   */
  _validateTitleData(data) {
    const title = data.title || data.name;
    if (!title || typeof title !== "string") {
      throw new Error("Title is required and must be a string");
    }

    if (
      !data.media_type ||
      !["movie", "tv_show", "game"].includes(data.media_type)
    ) {
      throw new Error("Valid media_type is required (movie, tv_show, or game)");
    }

    // Validate URLs if provided
    const urlFields = ["imdb_url", "steam_url", "metacritic_url"];
    for (const field of urlFields) {
      if (data[field] && !this._isValidURL(data[field])) {
        throw new Error(`Invalid ${field}`);
      }
    }
  }

  /**
   * Validate URL format
   * @private
   */
  _isValidURL(string) {
    try {
      new URL(string);
      return true;
    } catch {
      return false;
    }
  }
}

/**
 * Mock API Client for development/demo
 */
export class MockAPIClient extends APIClient {
  async analyzeTitle(titleData) {
    // Simulate network delay
    await this._delay(1500 + Math.random() * 1000);

    // Generate mock response
    return this._generateMockAnalysis(titleData);
  }

  async getMetrics() {
    await this._delay(300);

    return {
      reviews_processed_today: 15420 + Math.floor(Math.random() * 1000),
      system_accuracy: 91.2 + Math.random() * 2,
      processing_speed: 1000 + Math.floor(Math.random() * 300),
      active_platforms: 3,
      total_analyses: 98765,
    };
  }

  _delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  _generateMockAnalysis(titleData) {
    const compatibilityScore = 0.3 + Math.random() * 0.65;

    let recommendation;
    if (compatibilityScore >= CONFIG.RECOMMENDATION.HIGHLY_LIKELY) {
      recommendation = "Highly Likely";
    } else if (compatibilityScore >= CONFIG.RECOMMENDATION.WORTH_TRYING) {
      recommendation = "Worth Trying";
    } else if (compatibilityScore >= CONFIG.RECOMMENDATION.PROCEED_CAUTION) {
      recommendation = "Proceed with Caution";
    } else {
      recommendation = "Likely to Disappoint";
    }

    const themes = [
      "character_development",
      "moral_complexity",
      "world_building",
      "storytelling",
      "visual_effects",
      "emotional_depth",
      "exploration",
      "mystery",
      "humor",
      "philosophy",
    ];

    const selectedThemes = themes.sort(() => Math.random() - 0.5).slice(0, 4);

    const positiveBase =
      compatibilityScore > 0.7 ? 70 : compatibilityScore > 0.5 ? 55 : 40;
    const positive = Math.floor(positiveBase + Math.random() * 20);
    const neutral = Math.floor(10 + Math.random() * 20);
    const negative = Math.max(1, 100 - positive - neutral);

    return {
      title: titleData.title,
      recommendation,
      compatibility_score: compatibilityScore,
      theme_alignment: selectedThemes,
      sentiment_summary: {
        positive,
        neutral,
        negative,
      },
      matching_titles: [
        { title: "Fallout TV", score: 0.92 },
        { title: "Dark", score: 0.85 },
        { title: "3 Body Problem", score: 0.81 },
      ],
      analysis_id: `mock_${Date.now()}`,
      timestamp: new Date().toISOString(),
    };
  }
}
