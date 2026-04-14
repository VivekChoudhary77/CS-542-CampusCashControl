<template>
  <el-row justify="center" :class="['user-access-page-wrap', { 'is-dark': isDarkMode }]">
    <el-col :xs="24" :md="18" :lg="14">
      <el-skeleton :loading="showSkeleton" animated :rows="6">
        <template #template>
          <el-card shadow="never" class="access-card">
            <el-skeleton-item variant="h1" style="width: 45%; height: 28px;" />
            <el-skeleton-item variant="text" style="width: 80%; margin-top: 12px;" />
            <el-skeleton-item variant="rect" style="width: 100%; height: 180px; margin-top: 16px;" />
          </el-card>
        </template>

        <template #default>
          <el-card shadow="hover" class="access-card">
            <h2>
              <el-icon><User /></el-icon>
              User Access
            </h2>
            <p>Manage permissions, roles, and account-level access policies from this section.</p>
            <el-empty description="User access management panel will appear here." />
          </el-card>
        </template>
      </el-skeleton>
    </el-col>
  </el-row>
</template>

<script>
import { User } from "@element-plus/icons-vue";
import { themeState } from "@/state/themeState";

export default {
  name: "UserAccessPage",
  components: {
    User,
  },
  data() {
    return {
      showSkeleton: true,
    };
  },
  computed: {
    isDarkMode() {
      return themeState.isDarkMode;
    },
  },
  mounted() {
    setTimeout(() => {
      this.showSkeleton = false;
    }, 260);
  },
};
</script>

<style scoped>
.user-access-page-wrap.is-dark :deep(.el-card) {
  background: linear-gradient(160deg, rgba(11, 15, 24, 0.68), rgba(11, 15, 24, 0.82));
  border-color: rgba(166, 188, 216, 0.24);
}

.user-access-page-wrap.is-dark .access-card h2 {
  color: #e7eefc;
}

.user-access-page-wrap.is-dark .access-card p {
  color: #b7c5d8;
}

.user-access-page-wrap.is-dark :deep(.el-empty__description p) {
  color: #c6d4e8;
}

.access-card {
  border-radius: 14px;
  text-align: center;
}

.access-card h2 {
  margin: 0;
  color: #11334f;
}

.access-card p {
  color: #587088;
}
</style>
