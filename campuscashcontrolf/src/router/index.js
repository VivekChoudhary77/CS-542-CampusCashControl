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
  const isAuthenticated = localStorage.getItem("authenticated") === "true";

  // If not authenticated, force any navigation to go to the login page ("home")
  if (!isAuthenticated && to.name !== "home") {
    return next({ name: "home" });
  }
  
  // If authenticated and trying to access the login page ("home"), redirect to dashboard
  if (isAuthenticated && to.name === "home") {
    return next({ name: "dashboard" });
  }
  
  // Otherwise, allow the navigation to the requested route
  next();
});

export default router;