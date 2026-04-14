<template>
  <div class="not-found-wrap">
    <el-result icon="warning" title="404" sub-title="The page you are looking for does not exist.">
      <template #extra>
        <el-space>
          <el-button type="primary" @click="goPrimary">Go Back</el-button>
          <el-button @click="logoutToLogin">Login Page</el-button>
        </el-space>
      </template>
    </el-result>
  </div>
</template>

<script>
export default {
  name: "NotFoundPage",
  methods: {
    goPrimary() {
      if (window.history.length > 1) {
        this.$router.go(-1);
        return;
      }

      const isAuthenticated = !!(
        sessionStorage.getItem("access_token") || localStorage.getItem("access_token")
      );
      this.$router.replace({ name: isAuthenticated ? "dashboard" : "home" });
    },
    logoutToLogin() {
      sessionStorage.removeItem("access_token");
      sessionStorage.removeItem("refresh_token");
      sessionStorage.removeItem("authenticated");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("authenticated");
      this.$router.replace({ name: "home" });
    },
  },
};
</script>

<style scoped>
.not-found-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
}
</style>
