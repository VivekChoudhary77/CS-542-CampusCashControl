const LOCAL_API_BASE_URL = "http://localhost:8000/api";
const configuredApiBaseUrl = normalizeBaseUrl(process.env.VUE_APP_API_BASE_URL);

export const isProductionBuild = process.env.NODE_ENV === "production";
export const isApiBaseUrlMissingInProduction = isProductionBuild && !configuredApiBaseUrl;

function normalizeBaseUrl(url) {
  return (url || "").replace(/\/+$/, "");
}

function withApiSuffix(url) {
  const normalized = normalizeBaseUrl(url);
  if (!normalized) {
    return "";
  }
  return normalized.endsWith("/api") ? normalized : `${normalized}/api`;
}

export const API_BASE_URL = withApiSuffix(configuredApiBaseUrl) || LOCAL_API_BASE_URL;

export function apiUrl(path) {
  const normalizedPath = String(path || "").startsWith("/") ? path : `/${path}`;
  return `${API_BASE_URL}${normalizedPath}`;
}
