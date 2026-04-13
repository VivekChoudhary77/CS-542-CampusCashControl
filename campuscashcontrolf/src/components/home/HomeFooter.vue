<template>
  <footer :class="['hero-footer', { 'is-dark': isDarkMode }]">
    <div class="footer-inner">
      <span class="footer-copy">© {{ currentYear }} CampusCashControl, All rights reserved.</span>
      <div class="footer-links" role="navigation" aria-label="Footer links">
        <el-button
          v-for="link in footerLinks"
          :key="link.title"
          text
          class="footer-link-btn"
          @click="$emit('link-click', link)"
        >
          {{ link.title }}
        </el-button>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "HomeFooter",
  props: {
    isDarkMode: {
      type: Boolean,
      default: false,
    },
    currentYear: {
      type: Number,
      required: true,
    },
    footerLinks: {
      type: Array,
      required: true,
    },
  },
  emits: ["link-click"],
};
</script>

<style scoped>
.hero-footer {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: var(--footer-space);
  box-sizing: border-box;
  z-index: 12;
  padding: 14px 24px 18px;
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.64), rgba(250, 251, 252, 0.78));
}

.hero-footer.is-dark {
  background: linear-gradient(160deg, rgba(11, 15, 24, 0.55), rgba(11, 15, 24, 0.72));
}

.footer-inner {
  max-width: 1060px;
  margin: 0 auto;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 2px;
  flex-wrap: wrap;
}

.footer-link-btn {
  font-size: 0.86rem;
  font-weight: 600;
  color: #273140;
  padding: 0 8px;
  height: 28px;
}

.footer-link-btn:hover {
  color: #f26d21;
  background: rgba(242, 109, 33, 0.08);
}

.hero-footer.is-dark .footer-link-btn {
  color: #d7e3f6;
}

.hero-footer.is-dark .footer-link-btn:hover {
  color: #ffb26e;
  background: rgba(255, 178, 110, 0.12);
}

.footer-copy {
  font-size: 0.82rem;
  font-weight: 500;
  color: #445061;
  white-space: nowrap;
}

.hero-footer.is-dark .footer-copy {
  color: #b8c6d8;
}

@media (max-width: 960px) {
  .hero-footer {
    padding: 10px 12px 14px;
  }

  .footer-inner {
    padding: 10px 8px;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .footer-links {
    gap: 0;
  }

  .footer-copy {
    font-size: 0.78rem;
  }
}
</style>
