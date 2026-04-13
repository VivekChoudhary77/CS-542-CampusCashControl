<template>
  <div class="dot-background" aria-hidden="true">
    <canvas ref="dotCanvas" class="dot-canvas"></canvas>
  </div>
</template>

<script>
export default {
  name: "HeroDotBackground",
  props: {
    isDarkMode: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      pointerX: 0,
      pointerY: 0,
      pointerActive: false,
      dotAnimationFrame: null,
      flowTick: 0,
      canvasCtx: null,
      canvasWidth: 0,
      canvasHeight: 0,
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initDotCanvas();
      window.addEventListener("resize", this.resizeDotCanvas);
    });
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.resizeDotCanvas);
    this.stopDotAnimation();
  },
  methods: {
    initDotCanvas() {
      const canvas = this.$refs.dotCanvas;
      if (!canvas) {
        return;
      }

      this.canvasCtx = canvas.getContext("2d");
      this.resizeDotCanvas();
      this.startDotAnimation();
    },
    resizeDotCanvas() {
      const canvas = this.$refs.dotCanvas;
      if (!canvas || !this.canvasCtx) {
        return;
      }

      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      this.canvasWidth = rect.width;
      this.canvasHeight = rect.height;
      canvas.width = Math.max(1, Math.floor(rect.width * dpr));
      canvas.height = Math.max(1, Math.floor(rect.height * dpr));
      this.canvasCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    },
    startDotAnimation() {
      if (this.dotAnimationFrame) {
        return;
      }

      const tick = () => {
        this.flowTick += 1;
        this.drawDotField();
        this.dotAnimationFrame = requestAnimationFrame(tick);
      };

      this.dotAnimationFrame = requestAnimationFrame(tick);
    },
    stopDotAnimation() {
      if (this.dotAnimationFrame) {
        cancelAnimationFrame(this.dotAnimationFrame);
        this.dotAnimationFrame = null;
      }
    },
    mixColor(colorA, colorB, amount) {
      return [
        Math.round(colorA[0] + (colorB[0] - colorA[0]) * amount),
        Math.round(colorA[1] + (colorB[1] - colorA[1]) * amount),
        Math.round(colorA[2] + (colorB[2] - colorA[2]) * amount),
      ];
    },
    pickPaletteColor(seed) {
      const palette = this.isDarkMode
        ? [
            [255, 134, 96],
            [255, 214, 109],
            [122, 212, 255],
            [198, 150, 255],
          ]
        : [
            [255, 92, 64],
            [255, 178, 54],
            [74, 180, 255],
            [166, 87, 246],
          ];

      const normalized = ((seed % 1) + 1) % 1;
      const scaled = normalized * palette.length;
      const index = Math.floor(scaled) % palette.length;
      const nextIndex = (index + 1) % palette.length;
      const t = scaled - Math.floor(scaled);
      return this.mixColor(palette[index], palette[nextIndex], t);
    },
    drawDotField() {
      if (!this.canvasCtx || !this.canvasWidth || !this.canvasHeight) {
        return;
      }

      const ctx = this.canvasCtx;
      ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

      const spacing = this.canvasWidth < 768 ? 16 : 18;
      const baseSize = this.canvasWidth < 768 ? 0.94 : 1.05;
      const influenceRadius = this.canvasWidth < 768 ? 170 : 230;
      const baseColor = this.isDarkMode ? [214, 226, 242] : [37, 52, 69];
      const baseAlpha = this.isDarkMode ? 0.3 : 0.35;

      for (let y = spacing * 0.5; y < this.canvasHeight; y += spacing) {
        for (let x = spacing * 0.5; x < this.canvasWidth; x += spacing) {
          let influence = 0;
          if (this.pointerActive) {
            const dx = x - this.pointerX;
            const dy = y - this.pointerY;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < influenceRadius) {
              const near = 1 - dist / influenceRadius;
              const pulse = (Math.sin(this.flowTick * 0.085 + x * 0.052 + y * 0.038) + 1) * 0.5;
              influence = near * (0.72 + pulse * 0.28);
            }
          }

          const lift = influence * influence;
          const size = baseSize + lift * 3.2;
          const seed = x * 0.013 + y * 0.009 + this.flowTick * 0.008;
          const lively = this.pickPaletteColor(seed);
          const color = this.mixColor(baseColor, lively, Math.min(1, lift * 1.2));
          const alpha = Math.min(1, baseAlpha + lift * 0.92);

          ctx.fillStyle = `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${alpha})`;
          ctx.beginPath();
          ctx.arc(x, y, size, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    },
    onPointerMove(event) {
      const rect = event.currentTarget.getBoundingClientRect();
      this.pointerActive = true;
      this.pointerX = Math.min(this.canvasWidth, Math.max(0, event.clientX - rect.left));
      this.pointerY = Math.min(this.canvasHeight, Math.max(0, event.clientY - rect.top));
    },
    onPointerLeave() {
      this.pointerActive = false;
    },
  },
};
</script>

<style scoped>
.dot-background {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background-color: var(--panel-bg);
  transition: background-color 220ms ease;
}

.dot-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
}
</style>
