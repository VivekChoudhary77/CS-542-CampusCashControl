import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/components/HomePage.vue"; // Your login page component
import Dashboard from "@/components/DashboardPage.vue";      // The new dashboard component

const routes = [
  { path: "/", name: "home", component: HomePage },
  { path: "/dashboard", name: "dashboard", component: Dashboard },
  // Add additional routes (Departments, Upload, Reports) if you create components for them.
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
