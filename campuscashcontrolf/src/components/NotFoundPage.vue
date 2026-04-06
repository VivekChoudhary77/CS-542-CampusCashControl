<template>
  <div class="not-found-wrap">
    <el-result icon="warning" title="404" sub-title="The page you are looking for does not exist.">
      <template #extra>
        <el-space>
          <el-button type="primary" @click="goPrimary">Go Back</el-button>
          <el-button @click="$router.replace({ name: 'home' })">Login Page</el-button>
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
      const isAuthenticated = !!localStorage.getItem("access_token");
      this.$router.replace({ name: isAuthenticated ? "dashboard" : "home" });
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
