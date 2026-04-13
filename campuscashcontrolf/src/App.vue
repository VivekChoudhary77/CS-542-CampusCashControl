<template>
  <div v-loading.fullscreen.lock="uiState.routeLoading">
    <router-view />
  </div>
</template>

<script>
import { uiState } from "@/state/uiState";

export default {
  name: "App",
  data() {
    return {
      uiState,
    };
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