import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/components/HomePage.vue"; // Your login page component
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
  // Add additional routes (Departments, Upload, Reports) if you create components for them.
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
