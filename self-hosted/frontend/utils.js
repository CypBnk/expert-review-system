// Utility Functions

/**
 * Sanitize HTML to prevent XSS attacks
 * @param {string} str - String to sanitize
 * @returns {string} Sanitized string
 */
export function sanitizeHTML(str) {
  if (typeof str !== "string") return "";

  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

/**
 * Escape HTML special characters
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
export function escapeHTML(text) {
  if (typeof text !== "string") return "";

  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

/**
 * Format theme string for display
 * @param {string} theme - Theme string (e.g., 'character_development')
 * @returns {string} Formatted theme (e.g., 'Character Development')
 */
export function formatTheme(theme) {
  if (!theme) return "";
  return theme.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
}

/**
 * Validate URL format
 * @param {string} url - URL to validate
 * @returns {boolean} Is valid URL
 */
export function isValidURL(url) {
  if (!url) return false;
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

/**
 * Validate rating value
 * @param {number} rating - Rating to validate
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {boolean} Is valid rating
 */
export function isValidRating(rating, min = 1, max = 10) {
  return (
    typeof rating === "number" &&
    rating >= min &&
    rating <= max &&
    Number.isInteger(rating)
  );
}

/**
 * Debounce function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Deep clone an object
 * @param {Object} obj - Object to clone
 * @returns {Object} Cloned object
 */
export function deepClone(obj) {
  try {
    return JSON.parse(JSON.stringify(obj));
  } catch (error) {
    console.error("Failed to clone object:", error);
    return obj;
  }
}

/**
 * Get rating CSS class based on value
 * @param {number} rating - Rating value
 * @returns {string} CSS class name
 */
export function getRatingClass(rating) {
  if (rating >= 8) return "rating-badge--high";
  if (rating >= 6) return "rating-badge--medium";
  return "rating-badge--low";
}

/**
 * Show toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type: 'success', 'error', 'warning', 'info'
 */
export function showToast(message, type = "info") {
  // Check if toast container exists, create if not
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast toast--${type}`;
  toast.textContent = message;

  container.appendChild(toast);

  // Trigger animation
  setTimeout(() => toast.classList.add("toast--show"), 10);

  // Remove after delay
  setTimeout(() => {
    toast.classList.remove("toast--show");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

/**
 * Format date to readable string
 * @param {string|Date} date - Date to format
 * @returns {string} Formatted date
 */
export function formatDate(date) {
  try {
    const d = new Date(date);
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return "Invalid date";
  }
}

/**
 * Safely get element by ID with error handling
 * @param {string} id - Element ID
 * @returns {HTMLElement|null} Element or null
 */
export function getElement(id) {
  try {
    return document.getElementById(id);
  } catch (error) {
    console.error(`Failed to get element: ${id}`, error);
    return null;
  }
}

/**
 * Safely query selector with error handling
 * @param {string} selector - CSS selector
 * @param {HTMLElement} parent - Parent element
 * @returns {HTMLElement|null} Element or null
 */
export function querySelector(selector, parent = document) {
  try {
    return parent.querySelector(selector);
  } catch (error) {
    console.error(`Failed to query selector: ${selector}`, error);
    return null;
  }
}

/**
 * Safely query all with error handling
 * @param {string} selector - CSS selector
 * @param {HTMLElement} parent - Parent element
 * @returns {NodeList} Node list (empty if error)
 */
export function querySelectorAll(selector, parent = document) {
  try {
    return parent.querySelectorAll(selector);
  } catch (error) {
    console.error(`Failed to query all: ${selector}`, error);
    return [];
  }
}

/**
 * Show loading state on an element
 * @param {HTMLElement} element - Element to show loading on
 * @param {string} type - Type of loading ('button', 'form', 'card', 'overlay')
 */
export function showLoading(element, type = "overlay") {
  if (!element) return;

  switch (type) {
    case "button":
      element.classList.add("btn--loading");
      element.disabled = true;
      element.setAttribute("aria-busy", "true");
      break;

    case "form":
      element.classList.add("form--loading");
      element.setAttribute("aria-busy", "true");
      const submitBtn = element.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.classList.add("btn--loading");
        submitBtn.disabled = true;
      }
      break;

    case "card":
      element.classList.add("card--loading");
      element.setAttribute("aria-busy", "true");
      break;

    case "overlay":
    default:
      let overlay = element.querySelector(".loading-overlay");
      if (!overlay) {
        overlay = document.createElement("div");
        overlay.className = "loading-overlay";
        overlay.setAttribute("role", "status");
        overlay.setAttribute("aria-live", "polite");

        const spinner = document.createElement("div");
        spinner.className = "loading-spinner loading-spinner--large";
        spinner.setAttribute("aria-hidden", "true");

        const text = document.createElement("div");
        text.className = "loading-overlay__text";
        text.textContent = "Loading...";

        overlay.appendChild(spinner);
        overlay.appendChild(text);

        // Make element position: relative if needed
        const position = window.getComputedStyle(element).position;
        if (position === "static") {
          element.style.position = "relative";
        }

        element.appendChild(overlay);
      }

      // Use requestAnimationFrame to ensure DOM is updated
      requestAnimationFrame(() => {
        overlay.classList.add("loading-overlay--active");
      });
      element.setAttribute("aria-busy", "true");
      break;
  }
}

/**
 * Hide loading state on an element
 * @param {HTMLElement} element - Element to hide loading on
 * @param {string} type - Type of loading ('button', 'form', 'card', 'overlay')
 */
export function hideLoading(element, type = "overlay") {
  if (!element) return;

  switch (type) {
    case "button":
      element.classList.remove("btn--loading");
      element.disabled = false;
      element.removeAttribute("aria-busy");
      break;

    case "form":
      element.classList.remove("form--loading");
      element.removeAttribute("aria-busy");
      const submitBtn = element.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.classList.remove("btn--loading");
        submitBtn.disabled = false;
      }
      break;

    case "card":
      element.classList.remove("card--loading");
      element.removeAttribute("aria-busy");
      break;

    case "overlay":
    default:
      const overlay = element.querySelector(".loading-overlay");
      if (overlay) {
        overlay.classList.remove("loading-overlay--active");
        element.removeAttribute("aria-busy");
        // Remove overlay after animation
        setTimeout(() => {
          if (overlay.parentNode) {
            overlay.parentNode.removeChild(overlay);
          }
        }, 200);
      }
      break;
  }
}

/**
 * Create a spinner element
 * @param {string} size - Size ('small', 'large', or default)
 * @returns {HTMLElement} Spinner element
 */
export function createSpinner(size = "") {
  const spinner = document.createElement("div");
  spinner.className = `loading-spinner${
    size ? ` loading-spinner--${size}` : ""
  }`;
  spinner.setAttribute("role", "status");
  spinner.setAttribute("aria-label", "Loading");
  return spinner;
}
