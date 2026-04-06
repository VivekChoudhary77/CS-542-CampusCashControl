<template>
  <el-row justify="center">
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
  mounted() {
    setTimeout(() => {
      this.showSkeleton = false;
    }, 260);
  },
};
</script>

<style scoped>
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
