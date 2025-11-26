// Configuration Management
export const CONFIG = {
  API_BASE_URL: "http://localhost:5000/api",
  ENABLE_MOCK_DATA: false,
  STORAGE_KEY: "expert_review_preferences",

  // Thresholds
  RECOMMENDATION: {
    HIGHLY_LIKELY: 0.8,
    WORTH_TRYING: 0.6,
    PROCEED_CAUTION: 0.4,
  },

  // CSS Classes
  CLASSES: {
    HIDDEN: "hidden",
    ACTIVE: "active",
    LOADING: "btn--loading",
  },

  // Validation
  RATING: {
    MIN: 1,
    MAX: 10,
  },

  // Timeouts
  ANALYSIS_TIMEOUT: 30000,
  REQUEST_TIMEOUT: 10000,
};

export const RECOMMENDATION_LEVELS = {
  HIGHLY_LIKELY: "Highly Likely",
  WORTH_TRYING: "Worth Trying",
  PROCEED_CAUTION: "Proceed with Caution",
  LIKELY_DISAPPOINT: "Likely to Disappoint",
};
