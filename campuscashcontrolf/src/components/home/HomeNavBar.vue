<template>
  <div>
    <el-card :class="['floating-nav', modeClass, { 'is-dark': isDarkMode }]" shadow="always">
      <div class="brand-wrap">
        <el-icon><WalletFilled /></el-icon>
        <span>CampusCashControl</span>
      </div>

      <div class="hero-links" role="navigation" aria-label="Primary">
        <el-button text class="hero-link-btn" @click="emitNavigate('/dashboard')">
          <el-icon><DataAnalysis /></el-icon>
          <span>Dashboard</span>
        </el-button>
        <el-button text class="hero-link-btn" @click="emitNavigate('/departments')">
          <el-icon><OfficeBuilding /></el-icon>
          <span>Departments</span>
        </el-button>
        <el-button text class="hero-link-btn" @click="emitNavigate('/upload')">
          <el-icon><UploadFilled /></el-icon>
          <span>Upload</span>
        </el-button>
        <el-button text class="hero-link-btn" @click="emitNavigate('/reports')">
          <el-icon><Document /></el-icon>
          <span>Reports</span>
        </el-button>
        <el-button text class="hero-link-btn" @click="emitNavigate('/useraccess')">
          <el-icon><User /></el-icon>
          <span>User Access</span>
        </el-button>
      </div>

      <div class="nav-actions">
        <el-switch
          :model-value="isDarkMode"
          class="theme-toggle"
          :active-action-icon="Moon"
          :inactive-action-icon="Sunny"
          inline-prompt
          active-text="Dark"
          inactive-text="Light"
          @update:model-value="updateDarkMode"
        />

        <el-dropdown v-if="isAuthenticated" trigger="click" class="avatar-dropdown">
          <el-button class="login-avatar-btn" circle aria-label="Open account actions">
            <el-icon><UserFilled /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$emit('logout')">Logout</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <el-button v-else class="login-avatar-btn" circle aria-label="Open login" @click="$emit('open-login')">
          <el-icon><UserFilled /></el-icon>
        </el-button>
      </div>

      <el-button class="mobile-nav-toggle" circle @click="updateMobileMenu(true)">
        <el-icon><Menu /></el-icon>
      </el-button>
    </el-card>

    <el-drawer
      :model-value="mobileMenuOpen"
      direction="ltr"
      size="280px"
      title="Navigate"
      @update:model-value="updateMobileMenu"
    >
      <div class="mobile-nav-list">
        <el-button text @click="emitNavigate('/dashboard')">Dashboard</el-button>
        <el-button text @click="emitNavigate('/departments')">Departments</el-button>
        <el-button text @click="emitNavigate('/upload')">Upload</el-button>
        <el-button text @click="emitNavigate('/reports')">Reports</el-button>
        <el-button text @click="emitNavigate('/useraccess')">User Access</el-button>
        <el-button v-if="isAuthenticated" type="danger" @click="$emit('logout')">Logout</el-button>
        <el-button v-else type="primary" @click="$emit('open-login')">Login</el-button>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import {
  DataAnalysis,
  OfficeBuilding,
  UploadFilled,
  Document,
  User,
  UserFilled,
  Menu,
  WalletFilled,
  Sunny,
  Moon,
} from "@element-plus/icons-vue";

export default {
  name: "HomeNavBar",
  components: {
    DataAnalysis,
    OfficeBuilding,
    UploadFilled,
    Document,
    User,
    UserFilled,
    Menu,
    WalletFilled,
  },
  props: {
    mode: {
      type: String,
      default: "floating",
      validator: (value) => ["floating", "fixed"].includes(value),
    },
    isDarkMode: {
      type: Boolean,
      default: false,
    },
    mobileMenuOpen: {
      type: Boolean,
      default: false,
    },
    isAuthenticated: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:isDarkMode", "update:mobileMenuOpen", "navigate", "open-login", "logout"],
  data() {
    return {
      Sunny,
      Moon,
    };
  },
  computed: {
    modeClass() {
      return this.mode === "fixed" ? "fixed-nav" : "";
    },
  },
  methods: {
    emitNavigate(path) {
      this.$emit("navigate", path);
    },
    updateDarkMode(value) {
      this.$emit("update:isDarkMode", value);
    },
    updateMobileMenu(value) {
      this.$emit("update:mobileMenuOpen", value);
    },
  },
};
</script>

<style scoped>
.floating-nav {
  position: absolute;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  width: min(1040px, calc(100% - 36px));
  z-index: 30;
  border: 1px solid rgba(255, 255, 255, 0.48);
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.floating-nav.fixed-nav {
  position: fixed;
  top: 0;
  left: 0;
  transform: none;
  width: 100%;
  border-radius: 0;
  z-index: 1200;
  border-left: none;
  border-right: none;
  border-top: none;
  border-bottom: 1px solid rgba(26, 38, 52, 0.12);
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.64), rgba(250, 251, 252, 0.78));
  box-shadow: none;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
}

.floating-nav.is-dark {
  border: 1px solid rgba(164, 181, 203, 0.35);
  background: rgba(8, 12, 19, 0.62);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
}

.floating-nav.fixed-nav.is-dark {
  border-left: none;
  border-right: none;
  border-top: none;
  border-bottom: 1px solid rgba(166, 188, 216, 0.22);
  background: linear-gradient(160deg, rgba(11, 15, 24, 0.42), rgba(11, 15, 24, 0.58));
  box-shadow: none;
}

.floating-nav :deep(.el-card__body) {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 6px 12px;
  flex-wrap: nowrap;
}

.brand-wrap {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
  color: #212121;
  white-space: nowrap;
  font-size: 1rem;
  flex: 0 0 auto;
}

.floating-nav.is-dark .brand-wrap {
  color: #edf2fb;
}

.hero-links {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  overflow: visible;
}

.hero-link-btn {
  height: 32px;
  padding: 0 8px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #212121;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 8px;
  white-space: nowrap;
  flex: 0 0 auto;
}

.hero-link-btn:hover {
  color: #f26d21;
  background: rgba(242, 109, 33, 0.08);
}

.floating-nav.is-dark .hero-link-btn {
  color: #d8e2f1;
}

.floating-nav.is-dark .hero-link-btn:hover {
  color: #ffb26e;
  background: rgba(255, 178, 110, 0.12);
}

.nav-actions {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  flex: 0 0 auto;
}

.theme-toggle {
  --el-switch-on-color: #111a28;
  --el-switch-off-color: #e7edf5;
  --el-switch-border-color: rgba(20, 27, 38, 0.36);
}

.floating-nav.is-dark .theme-toggle {
  --el-switch-on-color: #000000;
  --el-switch-off-color: #55657d;
  --el-switch-border-color: rgba(220, 232, 247, 0.4);
}

.theme-toggle :deep(.el-switch__core) {
  border-width: 1px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.08);
}

.theme-toggle :deep(.el-switch__action) {
  color: #1c2532;
}

.floating-nav.is-dark .theme-toggle :deep(.el-switch__action) {
  color: #0f1724;
}

.theme-toggle :deep(.el-switch__inner) {
  font-weight: 700;
}

.theme-toggle :deep(.el-switch__label) {
  color: #6a7789;
}

.theme-toggle :deep(.el-switch__label.is-active) {
  color: #1a2433;
}

.floating-nav.is-dark .theme-toggle :deep(.el-switch__label) {
  color: #90a6c4;
}

.floating-nav.is-dark .theme-toggle :deep(.el-switch__label.is-active) {
  color: #f5f8ff;
}

.theme-toggle.is-checked :deep(.el-switch__action .el-icon) {
  color: #f5f8ff;
}

.floating-nav.is-dark .theme-toggle.is-checked :deep(.el-switch__action .el-icon) {
  color: #000000;
}

.theme-toggle:not(.is-checked) :deep(.el-switch__action .el-icon) {
  color: #1c2532;
}

.mobile-nav-toggle {
  display: none;
}

.login-avatar-btn {
  width: 34px;
  height: 34px;
  min-width: 34px;
  max-width: 34px;
  padding: 0 !important;
  border-radius: 999px;
  background: rgba(18, 18, 18, 0.9);
  border: 1px solid rgba(18, 18, 18, 0.95);
  color: #ffffff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 1 / 1;
  flex: 0 0 34px;
}

.avatar-dropdown {
  display: inline-flex;
}

.login-avatar-btn:hover {
  background: #242424;
  border-color: #242424;
  color: #ffffff;
}

.floating-nav.is-dark .login-avatar-btn {
  background: rgba(241, 246, 255, 0.95);
  border-color: rgba(241, 246, 255, 0.95);
  color: #111826;
}

.floating-nav.is-dark .login-avatar-btn:hover {
  background: #ffffff;
  border-color: #ffffff;
  color: #111826;
}

.mobile-nav-list {
  display: grid;
  gap: 8px;
}

.mobile-nav-list .el-button {
  justify-content: flex-start;
}

@media (max-width: 960px) {
  .login-avatar-btn {
    display: none;
  }

  .theme-toggle {
    display: none;
  }

  .hero-links {
    display: none;
  }

  .mobile-nav-toggle {
    display: inline-flex;
  }

  .floating-nav {
    left: 50%;
    transform: translateX(-50%);
    width: calc(100% - 20px);
    top: 10px;
  }

  .floating-nav :deep(.el-card__body) {
    padding: 6px 10px;
  }
}
</style>
