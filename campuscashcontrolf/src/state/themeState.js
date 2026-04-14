import { reactive } from "vue";

const THEME_STORAGE_KEY = "cc_theme_dark_mode";

function readInitialDarkMode() {
  if (typeof window === "undefined") {
    return false;
  }

  return localStorage.getItem(THEME_STORAGE_KEY) === "true";
}

export const themeState = reactive({
  isDarkMode: readInitialDarkMode(),
});

export function setDarkMode(value) {
  const normalized = !!value;
  themeState.isDarkMode = normalized;

  if (typeof window !== "undefined") {
    localStorage.setItem(THEME_STORAGE_KEY, normalized ? "true" : "false");
  }
}
