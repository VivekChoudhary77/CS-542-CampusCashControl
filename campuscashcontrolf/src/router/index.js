import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/components/HomePage.vue"; // Login/landing page
import Dashboard from "@/components/DashboardPage.vue";
import DepartmentPage from "@/components/DepartmentPage.vue";
import UploadPage from "@/components/UploadPage.vue";
import UserAccessPage from "@/components/UserAccessPage.vue";
import ReportPage from "@/components/ReportPage.vue";
import NotFoundPage from "@/components/NotFoundPage.vue";
import ProtectedLayout from "@/layouts/ProtectedLayout.vue";
import { uiState } from "@/state/uiState";

const routes = [
  { path: "/", name: "home", component: HomePage },
  {
    path: "/",
    component: ProtectedLayout,
    children: [
      { path: "dashboard", name: "dashboard", component: Dashboard },
      { path: "useraccess", name: "useraccess", component: UserAccessPage },
      { path: "departments", name: "department", component: DepartmentPage },
      { path: "upload", name: "upload", component: UploadPage },
      { path: "reports", name: "report", component: ReportPage },
    ],
  },
  { path: "/:pathMatch(.*)*", name: "not-found", component: NotFoundPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

let routeLoadStartedAt = 0;

function startRouteLoader() {
  routeLoadStartedAt = Date.now();
  uiState.routeLoading = true;
}

function closeRouteLoader() {
  const elapsed = Date.now() - routeLoadStartedAt;
  const minVisible = 260;
  const delay = elapsed < minVisible ? minVisible - elapsed : 0;

  setTimeout(() => {
    uiState.routeLoading = false;
  }, delay);
}

// Global navigation guard to enforce authentication rules:
router.beforeEach((to, from, next) => {
  startRouteLoader();

  const isAuthenticated = !!localStorage.getItem("access_token");

  // Unauthenticated users can only access the home (login) page.
  if (!isAuthenticated && !["home", "not-found"].includes(to.name)) {
    return next({ name: "home" });
  }

  // Authenticated users should not see the login page.
  if (isAuthenticated && to.name === "home") {
    return next({ name: "dashboard" });
  }

  // Otherwise, allow navigation.
  next();
});

router.afterEach(() => {
  closeRouteLoader();
});

router.onError(() => {
  closeRouteLoader();
  if (router.currentRoute.value.name !== "not-found") {
    router.replace({ name: "not-found" });
  }
});

export default router;