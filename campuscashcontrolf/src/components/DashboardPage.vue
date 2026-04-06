<template>
  <div class="dashboard-wrap">
    <el-skeleton :loading="showSkeleton" animated :rows="8">
      <template #template>
        <el-card shadow="never" class="hero-card">
          <el-skeleton-item variant="h1" style="width: 44%; height: 28px;" />
          <el-skeleton-item variant="text" style="width: 60%; margin-top: 12px;" />
        </el-card>
        <el-card class="tableau-card" shadow="never" style="margin-top: 18px;">
          <el-skeleton-item variant="rect" style="width: 100%; height: 64vh; border-radius: 10px;" />
        </el-card>
      </template>

      <template #default>
        <el-space direction="vertical" fill :size="18" class="dashboard-content">
          <el-card shadow="never" class="hero-card">
            <h2>Data Visualization Dashboard</h2>
            <p>Interactive analytics for campus financial performance.</p>
          </el-card>

          <el-card class="tableau-card" shadow="hover">
            <div class="tableau-container">
              <iframe
                src="https://public.tableau.com/views/CampusCashControl/Dashboard2?:embed=y&:showVizHome=no&:toolbar=yes"
                frameborder="0"
                allowfullscreen
              ></iframe>
            </div>
          </el-card>
        </el-space>
      </template>
    </el-skeleton>
  </div>
</template>

<script>
export default {
  name: "DashboardPage",
  data() {
    return {
      showSkeleton: true,
    };
  },
  mounted() {
    setTimeout(() => {
      this.showSkeleton = false;
    }, 380);

    // Keep users on authenticated screens after login.
    window.history.pushState(null, "", window.location.href);
    window.onpopstate = () => {
      window.history.go(1);
    };
  },
  beforeUnmount() {
    window.onpopstate = null;
  },
};
</script>

<style scoped>
.dashboard-wrap {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

.dashboard-content {
  width: 100%;
}

.hero-card h2 {
  margin: 0;
  color: #0f3350;
}

.hero-card p {
  margin: 8px 0 0;
  color: #4b5e75;
}

.tableau-card {
  border-radius: 14px;
}

.tableau-container {
  width: 100%;
  max-width: 1240px;
  margin: 0 auto;
  position: relative;
  min-height: 66vh;
  height: 0;
  padding-bottom: 0;
  overflow: hidden;
  border-radius: 10px;
  border: 1px solid #d8e3f0;
}

.tableau-container iframe {
  position: absolute;
  inset: 0;
  width: 100% !important;
  height: 100% !important;
  display: block;
}

@media (max-width: 900px) {
  .tableau-container {
    min-height: 56vh;
  }
}
</style>