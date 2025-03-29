import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/components/HomePage.vue"; // Ensure this file exists

const routes = [{ path: "/", component: HomePage }];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
