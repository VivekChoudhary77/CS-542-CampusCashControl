<template>
  <el-container class="app-shell">
    <el-header class="app-header">
      <router-link to="/dashboard" class="brand-link">
        <img src="@/assets/CCC Dashboard Logo.png" alt="CampusCashControl" class="brand-logo" />
      </router-link>

      <el-menu
        mode="horizontal"
        :default-active="activeMenu"
        router
        class="top-menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <span>Dashboard</span>
        </el-menu-item>
        <el-menu-item index="/departments">
          <el-icon><OfficeBuilding /></el-icon>
          <span>Departments</span>
        </el-menu-item>
        <el-menu-item index="/upload">
          <el-icon><UploadFilled /></el-icon>
          <span>Upload</span>
        </el-menu-item>
        <el-menu-item index="/reports">
          <el-icon><Document /></el-icon>
          <span>Reports</span>
        </el-menu-item>
        <el-menu-item index="/useraccess">
          <el-icon><User /></el-icon>
          <span>User Access</span>
        </el-menu-item>
      </el-menu>

      <el-dropdown trigger="click" class="user-actions">
        <el-avatar :icon="UserFilled" />
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">Logout</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-header>

    <el-main class="app-main">
      <slot />
    </el-main>

    <el-footer class="app-footer">© <span id="year">2026</span> CampusCashControl</el-footer>
  </el-container>
</template>

<script>
import { ElNotification } from "element-plus";
import { DataAnalysis, OfficeBuilding, UploadFilled, Document, User, UserFilled } from "@element-plus/icons-vue";

export default {
  name: "AppShell",
  components: {
    DataAnalysis,
    OfficeBuilding,
    UploadFilled,
    Document,
    User,
  },
  data() {
    return {
      UserFilled,
    };
  },
  computed: {
    activeMenu() {
      const allowed = ["/dashboard", "/departments", "/upload", "/reports", "/useraccess"];
      return allowed.includes(this.$route.path) ? this.$route.path : "/dashboard";
    },
  },
  mounted() {
    document.getElementById("year").textContent = new Date().getFullYear();
  },
  methods: {
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("authenticated");
      ElNotification({
        title: "Logged out",
        message: "You have been signed out successfully.",
        type: "info",
      });
      this.$router.replace({ name: "home" });
    },
  },
};
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.app-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 22px;
  background: linear-gradient(120deg, #0a2840 0%, #144f72 100%);
  box-shadow: 0 10px 30px rgba(10, 40, 64, 0.2);
}

.brand-link {
  display: inline-flex;
  align-items: center;
}

.brand-logo {
  height: 38px;
  object-fit: contain;
}

.top-menu {
  flex: 1;
  border-bottom: none;
  background-color: transparent;
}

.top-menu :deep(.el-menu-item) {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #ecf6ff;
  border-bottom: 2px solid transparent;
  font-weight: 700;
}

.top-menu :deep(.el-menu-item.is-active) {
  color: #ffffff;
  border-bottom-color: #f0c95a;
}

.top-menu :deep(.el-menu-item:hover) {
  color: #fef4cf;
  background: rgba(255, 255, 255, 0.08);
}

.user-actions {
  margin-left: auto;
  cursor: pointer;
}

.app-main {
  flex: 1;
  padding: 24px;
  background: #ffffff;
}

.app-footer {
  text-align: center;
  color: #3f5166;
  border-top: 1px solid #d8dfeb;
  background: rgba(255, 255, 255, 0.45);
}

@media (max-width: 980px) {
  .app-header {
    flex-wrap: wrap;
    row-gap: 8px;
  }

  .top-menu {
    order: 3;
    width: 100%;
  }
}
</style>
