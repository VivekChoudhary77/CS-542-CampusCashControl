<template>
  <AppShell>
    <router-view />
  </AppShell>
</template>

<script>
import AppShell from "@/components/AppShell.vue";

export default {
  name: "ProtectedLayout",
  components: {
    AppShell,
  },
};
</script>
