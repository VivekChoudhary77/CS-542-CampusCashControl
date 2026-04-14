<template>
  <el-container :class="['app-shell', { 'is-dark': isDarkMode }]">
    <HeroDotBackground ref="dotBackground" :is-dark-mode="isDarkMode" />

    <HomeNavBar
      mode="fixed"
      :is-dark-mode="isDarkMode"
      :mobile-menu-open="mobileMenuOpen"
      :is-authenticated="true"
      @update:isDarkMode="isDarkMode = $event"
      @update:mobileMenuOpen="mobileMenuOpen = $event"
      @navigate="navigate"
      @logout="logout"
    />

    <el-main class="app-main" @mousemove="handleShellPointerMove" @mouseleave="handleShellPointerLeave">
      <slot />
    </el-main>

    <HomeFooter
      :is-shell-mode="true"
      :is-dark-mode="isDarkMode"
      :current-year="currentYear"
      :footer-links="footerLinks"
      @link-click="handleFooterLink"
    />
  </el-container>
</template>

<script>
import { ElNotification } from "element-plus";
import HomeNavBar from "@/components/home/HomeNavBar.vue";
import HomeFooter from "@/components/home/HomeFooter.vue";
import HeroDotBackground from "@/components/home/HeroDotBackground.vue";
import { setDarkMode, themeState } from "@/state/themeState";

export default {
  name: "AppShell",
  components: {
    HomeNavBar,
    HomeFooter,
    HeroDotBackground,
  },
  data() {
    return {
      mobileMenuOpen: false,
      footerLinks: [
        { title: "Features" },
        { title: "Dashboard", path: "/dashboard" },
        { title: "Departments", path: "/departments" },
        { title: "Upload", path: "/upload" },
        { title: "Reports", path: "/reports" },
        { title: "User Access", path: "/useraccess" },
      ],
    };
  },
  computed: {
    isDarkMode: {
      get() {
        return themeState.isDarkMode;
      },
      set(value) {
        setDarkMode(value);
      },
    },
    currentYear() {
      return new Date().getFullYear();
    },
  },
  methods: {
    navigate(path) {
      this.mobileMenuOpen = false;
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    },
    handleFooterLink(link) {
      if (!link?.path) {
        return;
      }
      this.navigate(link.path);
    },
    handleShellPointerMove(event) {
      this.$refs.dotBackground?.onPointerMove?.(event);
    },
    handleShellPointerLeave() {
      this.$refs.dotBackground?.onPointerLeave?.();
    },
    logout() {
      sessionStorage.removeItem("access_token");
      sessionStorage.removeItem("refresh_token");
      sessionStorage.removeItem("authenticated");
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
  --footer-space: 118px;
  --panel-bg: #ffffff;
  --content-overlay: linear-gradient(160deg, rgba(255, 255, 255, 0.64), rgba(250, 251, 252, 0.78));
  --content-separator: rgba(26, 38, 52, 0.12);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background: var(--panel-bg);
}

.app-shell.is-dark {
  --panel-bg: #000000;
  --content-overlay: linear-gradient(160deg, rgba(11, 15, 24, 0.55), rgba(11, 15, 24, 0.72));
  --content-separator: rgba(166, 188, 216, 0.22);
}

.app-main {
  flex: 1;
  position: relative;
  z-index: 10;
  padding: 92px 24px calc(var(--footer-space) + 16px);
  background: var(--content-overlay);
  border-top: 1px solid var(--content-separator);
  border-bottom: 1px solid var(--content-separator);
}

@media (max-width: 980px) {
  .app-shell {
    --footer-space: 146px;
  }

  .app-main {
    padding-top: 76px;
  }
}
</style>
