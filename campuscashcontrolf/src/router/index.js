import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/components/HomePage.vue"; // Login/landing page
import Dashboard from "@/components/DashboardPage.vue"; 
import DepartmentPage from "@/components/DepartmentPage.vue";
import UploadPage from "@/components/UploadPage.vue";
import ReportPage from "@/components/ReportPage.vue";

const routes = [
  { path: "/", name: "home", component: HomePage },
  { path: "/dashboard", name: "dashboard", component: Dashboard },
  { path: "/departments", name: "department", component: DepartmentPage },
  { path: "/upload", name: "upload", component: UploadPage },
  { path: "/reports", name: "report", component: ReportPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global navigation guard to enforce authentication rules:
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("access_token");

  // Unauthenticated users can only access the home (login) page.
  if (!isAuthenticated && to.name !== "home") {
    return next({ name: "home" });
  }

  // Authenticated users should not see the login page.
  if (isAuthenticated && to.name === "home") {
    return next({ name: "dashboard" });
  }

  // Otherwise, allow navigation.
  next();
});

export default router;