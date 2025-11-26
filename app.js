// Expert Review Analysis System V2 - Main Application
//
// AI Development Notice:
// This code was developed with AI assistance (GitHub Copilot, Claude).
// All code has been reviewed, tested, and validated by human developers.
//
// Fixed: XSS vulnerabilities, error handling, data persistence, API integration

import { CONFIG, RECOMMENDATION_LEVELS } from "./config.js";
import { StorageManager } from "./storage.js";
import { APIClient, MockAPIClient } from "./api.js";
import {
  sanitizeHTML,
  escapeHTML,
  formatTheme,
  isValidURL,
  isValidRating,
  getRatingClass,
  showToast,
  getElement,
  querySelector,
  querySelectorAll,
  showLoading,
  hideLoading,
  createSpinner,
} from "./utils.js";

// Application State
class AppState {
  constructor() {
    this.preferences = [];
    this.currentAnalysis = null;
    this.systemMetrics = null;
    this.isLoading = false;
  }
}

// Main Application Class
class ExpertReviewApp {
  constructor() {
    this.state = new AppState();
    this.storage = new StorageManager();
    this.api = CONFIG.ENABLE_MOCK_DATA ? new MockAPIClient() : new APIClient();
    this.editingIndex = null;
  }

  /**
   * Initialize the application
   */
  async init() {
    try {
      console.log("Initializing Expert Review System V2...");

      // Load user preferences from storage
      this.state.preferences = this.storage.loadPreferences();

      // Initialize UI components
      this.initializeNavigation();
      this.initializeAnalysisForm();
      this.initializePreferencesManager();
      this.initializeModal();

      // Load system metrics
      await this.loadSystemMetrics();

      // Render initial data
      this.renderPreferencesTable();

      console.log("Application initialized successfully");
    } catch (error) {
      console.error("Failed to initialize application:", error);
      showToast("Failed to initialize application", "error");
    }
  }

  /**
   * Initialize navigation system
   */
  initializeNavigation() {
    const navTabs = querySelectorAll(".nav-tab");

    navTabs.forEach((tab) => {
      tab.addEventListener("click", (e) => {
        e.preventDefault();
        const sectionId = tab.getAttribute("data-section");
        this.switchSection(sectionId);
      });
    });
  }

  /**
   * Switch between sections
   */
  switchSection(sectionId) {
    try {
      const navTabs = querySelectorAll(".nav-tab");
      const contentSections = querySelectorAll(".content-section");

      // Update nav tabs
      navTabs.forEach((tab) => {
        if (tab.getAttribute("data-section") === sectionId) {
          tab.classList.add(CONFIG.CLASSES.ACTIVE);
        } else {
          tab.classList.remove(CONFIG.CLASSES.ACTIVE);
        }
      });

      // Update content sections
      contentSections.forEach((section) => {
        if (section.id === `${sectionId}-section`) {
          section.classList.add(CONFIG.CLASSES.ACTIVE);
        } else {
          section.classList.remove(CONFIG.CLASSES.ACTIVE);
        }
      });
    } catch (error) {
      console.error("Failed to switch section:", error);
    }
  }

  /**
   * Initialize analysis form
   */
  initializeAnalysisForm() {
    const form = getElement("analysis-form");

    if (form) {
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        await this.handleAnalysis();
      });
    }
  }

  /**
   * Handle title analysis
   */
  async handleAnalysis() {
    if (this.state.isLoading) {
      showToast("Analysis already in progress", "warning");
      return;
    }

    try {
      // Get form data
      const titleInput = getElement("title-input");
      const mediaTypeSelect = getElement("media-type");
      const imdbURL = getElement("imdb-url");
      const steamURL = getElement("steam-url");
      const metacriticURL = getElement("metacritic-url");

      // Validate inputs
      const titleName = titleInput?.value.trim();
      const mediaType = mediaTypeSelect?.value;

      if (!titleName || !mediaType) {
        showToast("Please fill in title name and select media type", "warning");
        return;
      }

      // Build request data
      const titleData = {
        title: titleName,
        media_type: mediaType,
      };

      // Add optional URLs if provided and valid
      if (imdbURL?.value && isValidURL(imdbURL.value)) {
        titleData.imdb_url = imdbURL.value;
      }
      if (steamURL?.value && isValidURL(steamURL.value)) {
        titleData.steam_url = steamURL.value;
      }
      if (metacriticURL?.value && isValidURL(metacriticURL.value)) {
        titleData.metacritic_url = metacriticURL.value;
      }

      // Show loading state
      this.setAnalysisLoading(true);

      // Call API
      const result = await this.api.analyzeTitle(titleData);

      // Store result
      this.state.currentAnalysis = result;

      // Display results
      this.displayAnalysisResults(result);

      showToast("Analysis completed successfully", "success");
    } catch (error) {
      console.error("Analysis failed:", error);
      showToast(error.message || "Analysis failed. Please try again.", "error");
    } finally {
      this.setAnalysisLoading(false);
    }
  }

  /**
   * Set loading state for analysis
   */
  setAnalysisLoading(isLoading) {
    this.state.isLoading = isLoading;
    const form = getElement("analysis-form");
    const resultsCard = getElement("analysis-results");

    if (form) {
      if (isLoading) {
        showLoading(form, "form");
      } else {
        hideLoading(form, "form");
      }
    }

    // Show loading overlay on results card if it exists
    if (resultsCard && !resultsCard.classList.contains(CONFIG.CLASSES.HIDDEN)) {
      if (isLoading) {
        showLoading(resultsCard, "overlay");
      } else {
        hideLoading(resultsCard, "overlay");
      }
    }
  }

  /**
   * Display analysis results
   */
  displayAnalysisResults(result) {
    try {
      const resultsPlaceholder = getElement("results-placeholder");
      const analysisResults = getElement("analysis-results");

      if (resultsPlaceholder && analysisResults) {
        resultsPlaceholder.classList.add(CONFIG.CLASSES.HIDDEN);
        analysisResults.classList.remove(CONFIG.CLASSES.HIDDEN);
      }

      // Update result title (sanitized)
      const resultTitle = getElement("result-title");
      if (resultTitle) {
        resultTitle.textContent = `Analysis: ${result.title}`;
      }

      // Update UI components
      this.updateRecommendationBadge(
        result.recommendation,
        result.compatibility_score
      );
      this.updateCompatibilityScore(result.compatibility_score);
      this.updateThemeTags(result.theme_alignment);
      this.updateSentimentBars(result.sentiment_summary);
      this.updateMatchingTitles(result.matching_titles);
    } catch (error) {
      console.error("Failed to display results:", error);
      showToast("Failed to display results", "error");
    }
  }

  /**
   * Update recommendation badge
   */
  updateRecommendationBadge(recommendation, score) {
    const badge = getElement("rec-badge");
    if (!badge) return;

    const scorePercent = Math.round(score * 100);

    // Remove existing modifier classes
    badge.className = "rec-badge";

    // Add appropriate class based on recommendation
    const classMap = {
      [RECOMMENDATION_LEVELS.HIGHLY_LIKELY]: "rec-badge--highly-likely",
      [RECOMMENDATION_LEVELS.WORTH_TRYING]: "rec-badge--worth-trying",
      [RECOMMENDATION_LEVELS.PROCEED_CAUTION]: "rec-badge--proceed-caution",
      [RECOMMENDATION_LEVELS.LIKELY_DISAPPOINT]: "rec-badge--likely-disappoint",
    };

    const badgeClass = classMap[recommendation] || "rec-badge--worth-trying";
    badge.classList.add(badgeClass);

    // Update text content (sanitized)
    const badgeText = querySelector(".rec-badge__text", badge);
    const badgeScore = querySelector(".rec-badge__score", badge);

    if (badgeText) badgeText.textContent = recommendation;
    if (badgeScore) badgeScore.textContent = `${scorePercent}% Match`;
  }

  /**
   * Update compatibility score display
   */
  updateCompatibilityScore(score) {
    const progressFill = getElement("compatibility-progress");
    const progressLabel = querySelector(".progress-label");
    const percent = Math.round(score * 100);

    if (progressFill) {
      progressFill.style.width = `${percent}%`;
    }
    if (progressLabel) {
      progressLabel.textContent = `${percent}%`;
    }
  }

  /**
   * Update theme tags (XSS safe)
   */
  updateThemeTags(themes) {
    const container = getElement("theme-tags");
    if (!container || !Array.isArray(themes)) return;

    // Clear existing content
    container.innerHTML = "";

    // Create elements safely
    themes.forEach((theme) => {
      const tag = document.createElement("span");
      tag.className = "theme-tag";
      tag.textContent = formatTheme(theme); // Safe text content
      container.appendChild(tag);
    });
  }

  /**
   * Update sentiment bars
   */
  updateSentimentBars(sentiment) {
    if (!sentiment) return;

    const bars = querySelectorAll(".sentiment-fill");
    const values = querySelectorAll(".sentiment-value");

    if (bars.length >= 3 && values.length >= 3) {
      bars[0].style.width = `${sentiment.positive}%`;
      bars[1].style.width = `${sentiment.neutral}%`;
      bars[2].style.width = `${sentiment.negative}%`;

      values[0].textContent = `${sentiment.positive}%`;
      values[1].textContent = `${sentiment.neutral}%`;
      values[2].textContent = `${sentiment.negative}%`;
    }
  }

  /**
   * Update matching titles (XSS safe)
   */
  updateMatchingTitles(matchingTitles) {
    const container = getElement("matching-titles-list");
    if (!container || !Array.isArray(matchingTitles)) return;

    // Clear existing content
    container.innerHTML = "";

    // Create elements safely
    matchingTitles.forEach((match) => {
      const item = document.createElement("div");
      item.className = "matching-item";

      const titleSpan = document.createElement("span");
      titleSpan.className = "matching-title";
      titleSpan.textContent = match.title || match;

      const scoreSpan = document.createElement("span");
      scoreSpan.className = "matching-score";
      const score = match.score ? Math.round(match.score * 100) : 85;
      scoreSpan.textContent = `${score}% match`;

      item.appendChild(titleSpan);
      item.appendChild(scoreSpan);
      container.appendChild(item);
    });
  }

  /**
   * Initialize preferences manager
   */
  initializePreferencesManager() {
    // Event delegation for edit/delete buttons
    const tbody = getElement("preferences-tbody");
    if (tbody) {
      tbody.addEventListener("click", (e) => {
        const target = e.target;

        if (target.classList.contains("action-btn--edit")) {
          const index = parseInt(target.dataset.index, 10);
          this.editPreference(index);
        } else if (target.classList.contains("action-btn--delete")) {
          const index = parseInt(target.dataset.index, 10);
          this.deletePreference(index);
        }
      });
    }
  }

  /**
   * Render preferences table (XSS safe with event delegation)
   */
  renderPreferencesTable() {
    const tbody = getElement("preferences-tbody");
    if (!tbody) return;

    // Clear existing content
    tbody.innerHTML = "";

    // Create rows safely
    this.state.preferences.forEach((pref, index) => {
      const row = document.createElement("tr");

      // Title cell
      const titleCell = document.createElement("td");
      const titleDiv = document.createElement("div");
      titleDiv.className = "title-cell";
      const titleStrong = document.createElement("strong");
      titleStrong.textContent = pref.title; // Safe
      titleDiv.appendChild(titleStrong);
      titleCell.appendChild(titleDiv);

      // Rating cell
      const ratingCell = document.createElement("td");
      const ratingBadge = document.createElement("span");
      ratingBadge.className = `rating-badge ${getRatingClass(
        pref.user_rating
      )}`;
      ratingBadge.textContent = pref.user_rating;
      ratingCell.appendChild(ratingBadge);

      // Media type cell
      const mediaCell = document.createElement("td");
      const mediaBadge = document.createElement("span");
      mediaBadge.className = `media-type-badge media-type-badge--${pref.media_type.toLowerCase()}`;
      mediaBadge.textContent = pref.media_type;
      mediaCell.appendChild(mediaBadge);

      // Themes cell
      const themesCell = document.createElement("td");
      themesCell.className = "themes-cell";
      const themesDiv = document.createElement("div");
      themesDiv.className = "theme-mini-tags";

      pref.themes.slice(0, 3).forEach((theme) => {
        const tag = document.createElement("span");
        tag.className = "theme-mini-tag";
        tag.textContent = formatTheme(theme);
        themesDiv.appendChild(tag);
      });

      if (pref.themes.length > 3) {
        const moreTag = document.createElement("span");
        moreTag.className = "theme-mini-tag";
        moreTag.textContent = `+${pref.themes.length - 3}`;
        themesDiv.appendChild(moreTag);
      }

      themesCell.appendChild(themesDiv);

      // Actions cell (using event delegation - NO inline handlers)
      const actionsCell = document.createElement("td");
      const editBtn = document.createElement("button");
      editBtn.className = "action-btn action-btn--edit";
      editBtn.textContent = "Edit";
      editBtn.dataset.index = index; // Store index in data attribute

      const deleteBtn = document.createElement("button");
      deleteBtn.className = "action-btn action-btn--delete";
      deleteBtn.textContent = "Delete";
      deleteBtn.dataset.index = index;

      actionsCell.appendChild(editBtn);
      actionsCell.appendChild(deleteBtn);

      // Build row
      row.appendChild(titleCell);
      row.appendChild(ratingCell);
      row.appendChild(mediaCell);
      row.appendChild(themesCell);
      row.appendChild(actionsCell);

      tbody.appendChild(row);
    });
  }

  /**
   * Edit preference
   */
  editPreference(index) {
    try {
      const pref = this.state.preferences[index];
      if (!pref) {
        showToast("Preference not found", "error");
        return;
      }

      // Store editing index
      this.editingIndex = index;

      // Fill form with existing data
      const prefTitle = getElement("pref-title");
      const prefRating = getElement("pref-rating");
      const prefMediaType = getElement("pref-media-type");
      const prefThemes = getElement("pref-themes");

      if (prefTitle) prefTitle.value = pref.title;
      if (prefRating) prefRating.value = pref.user_rating;
      if (prefMediaType) prefMediaType.value = pref.media_type;
      if (prefThemes) prefThemes.value = pref.themes.join(", ");

      // Show modal
      this.showModal();
    } catch (error) {
      console.error("Failed to edit preference:", error);
      showToast("Failed to edit preference", "error");
    }
  }

  /**
   * Delete preference
   */
  deletePreference(index) {
    try {
      const pref = this.state.preferences[index];
      if (!pref) return;

      if (confirm(`Are you sure you want to delete "${pref.title}"?`)) {
        this.state.preferences.splice(index, 1);
        this.storage.savePreferences(this.state.preferences);
        this.renderPreferencesTable();
        showToast("Preference deleted", "success");
      }
    } catch (error) {
      console.error("Failed to delete preference:", error);
      showToast("Failed to delete preference", "error");
    }
  }

  /**
   * Initialize modal
   */
  initializeModal() {
    const addBtn = getElement("add-preference-btn");
    const modal = getElement("add-preference-modal");
    const modalOverlay = getElement("modal-overlay");
    const modalClose = getElement("modal-close");
    const cancelBtn = getElement("cancel-preference");
    const form = getElement("preference-form");

    if (addBtn) {
      addBtn.addEventListener("click", () => this.showModal());
    }

    if (modalClose) {
      modalClose.addEventListener("click", () => this.hideModal());
    }

    if (modalOverlay) {
      modalOverlay.addEventListener("click", () => this.hideModal());
    }

    if (cancelBtn) {
      cancelBtn.addEventListener("click", () => this.hideModal());
    }

    if (form) {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        this.handlePreferenceSubmission();
      });
    }
  }

  /**
   * Show modal
   */
  showModal() {
    const modal = getElement("add-preference-modal");
    if (modal) {
      modal.classList.remove(CONFIG.CLASSES.HIDDEN);
      document.body.style.overflow = "hidden";
    }
  }

  /**
   * Hide modal
   */
  hideModal() {
    const modal = getElement("add-preference-modal");
    const form = getElement("preference-form");

    if (modal) {
      modal.classList.add(CONFIG.CLASSES.HIDDEN);
      document.body.style.overflow = "";
    }

    if (form) {
      form.reset();
    }

    this.editingIndex = null;
  }

  /**
   * Handle preference form submission
   */
  handlePreferenceSubmission() {
    try {
      const prefTitle = getElement("pref-title");
      const prefRating = getElement("pref-rating");
      const prefMediaType = getElement("pref-media-type");
      const prefThemes = getElement("pref-themes");

      // Validate
      const title = prefTitle?.value.trim();
      const rating = parseInt(prefRating?.value);
      const mediaType = prefMediaType?.value;
      const themesInput = prefThemes?.value.trim();

      if (!title) {
        showToast("Title is required", "warning");
        return;
      }

      if (!isValidRating(rating, CONFIG.RATING.MIN, CONFIG.RATING.MAX)) {
        showToast(
          `Rating must be between ${CONFIG.RATING.MIN} and ${CONFIG.RATING.MAX}`,
          "warning"
        );
        return;
      }

      if (!mediaType) {
        showToast("Media type is required", "warning");
        return;
      }

      // Parse themes
      const themes = themesInput
        ? themesInput
            .split(",")
            .map((t) => t.trim().toLowerCase().replace(/\s+/g, "_"))
            .filter((t) => t)
        : [];

      const newPreference = {
        title,
        user_rating: rating,
        media_type: mediaType,
        themes,
      };

      // Update or add
      if (this.editingIndex !== null) {
        this.state.preferences[this.editingIndex] = newPreference;
        showToast("Preference updated", "success");
      } else {
        this.state.preferences.push(newPreference);
        showToast("Preference added", "success");
      }

      // Save to storage
      this.storage.savePreferences(this.state.preferences);

      // Update UI
      this.renderPreferencesTable();
      this.hideModal();
    } catch (error) {
      console.error("Failed to save preference:", error);
      showToast("Failed to save preference", "error");
    }
  }

  /**
   * Load system metrics
   */
  async loadSystemMetrics() {
    try {
      this.state.systemMetrics = await this.api.getMetrics();
      this.displaySystemMetrics();
    } catch (error) {
      console.error("Failed to load system metrics:", error);
      // Non-critical, continue
    }
  }

  /**
   * Display system metrics
   */
  displaySystemMetrics() {
    if (!this.state.systemMetrics) return;

    const metricValues = querySelectorAll(".metric-value");
    if (metricValues.length >= 4) {
      metricValues[0].textContent =
        this.state.systemMetrics.reviews_processed_today.toLocaleString();
      metricValues[1].textContent = `${this.state.systemMetrics.system_accuracy.toFixed(
        1
      )}%`;
      metricValues[2].textContent = `${Math.round(
        this.state.systemMetrics.processing_speed
      )}ms`;
      metricValues[3].textContent =
        this.state.systemMetrics.active_platforms.toString();
    }
  }
}

// Initialize app when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  window.app = new ExpertReviewApp();
  window.app.init();
});

// Export for module usage
export { ExpertReviewApp };
