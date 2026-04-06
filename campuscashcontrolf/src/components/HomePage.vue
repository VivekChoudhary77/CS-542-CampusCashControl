<template>
  <el-container class="home-root">
    <el-main class="home-main-wrap">
      <el-skeleton :loading="showSkeleton" animated :rows="6">
        <template #template>
          <div class="home-main">
            <el-skeleton-item variant="rect" style="width: 100%; height: 100%;" />
            <el-skeleton-item variant="rect" style="width: 100%; height: 100%;" />
          </div>
        </template>

        <template #default>
          <div class="home-main">
            <div class="hero-panel">
              <div class="hero-overlay">
                <h1>CampusCashControl</h1>
                <p>Manage and monitor university financial activity with clarity.</p>
              </div>
            </div>

            <div class="form-panel">
              <el-card class="login-card" shadow="hover">
                <LoginForm />
              </el-card>
            </div>
          </div>
        </template>
      </el-skeleton>
    </el-main>
  </el-container>
</template>

<script>
import LoginForm from "@/components/LoginForm.vue";

export default {
  data() {
    return {
      showSkeleton: true,
    };
  },
  components: {
    LoginForm,
  },
  mounted() {
    setTimeout(() => {
      this.showSkeleton = false;
    }, 260);
  },
};
</script>

<style scoped>
.home-root {
  min-height: 100vh;
}

.home-main-wrap {
  min-height: 100vh;
  padding: 0;
}

.home-main {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  min-height: 100vh;
  padding: 0;
}

.hero-panel {
  background: url("https://images.unsplash.com/photo-1577985043696-8bd54d9f093f?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D") no-repeat center center;
  background-size: cover;
  position: relative;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  color: #fff;
  background: linear-gradient(150deg, rgba(3, 31, 49, 0.65), rgba(3, 17, 29, 0.45));
  padding: 48px;
}

.hero-overlay h1 {
  margin: 0 0 12px;
  font-size: 3rem;
  font-weight: 800;
}

.hero-overlay p {
  margin: 0;
  font-size: 1.1rem;
  max-width: 520px;
}

.form-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: linear-gradient(145deg, #fafcff 0%, #f5efe2 100%);
}

.login-card {
  width: 100%;
  max-width: 460px;
  border-radius: 18px;
}

@media (max-width: 960px) {
  .home-main {
    grid-template-columns: 1fr;
  }

  .hero-panel {
    min-height: 36vh;
  }
}
</style>