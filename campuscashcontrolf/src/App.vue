<template>
  <div v-loading.fullscreen.lock="uiState.routeLoading">
    <router-view />
  </div>
</template>

<script>
import { ElNotification } from "element-plus";
import { uiState } from "@/state/uiState";
import { isApiBaseUrlMissingInProduction } from "@/config/api";

export default {
  name: "App",
  data() {
    return {
      uiState,
    };
  },
  mounted() {
    if (!isApiBaseUrlMissingInProduction) {
      return;
    }

    ElNotification({
      title: "Missing API configuration",
      message: "VUE_APP_API_BASE_URL is not set for this production build. API actions will fail until it is configured in Amplify environment variables.",
      type: "warning",
      duration: 0,
    });
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --app-bg: #ffffff;
}

* {
  box-sizing: border-box;
  font-family: 'Manrope', sans-serif;
}

body {
  margin: 0;
  background: var(--app-bg);
}
</style>