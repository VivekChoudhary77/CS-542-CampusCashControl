<template>
  <div class="container-fluid p-0 vh-100">
    <div class="row no-gutters vh-100">
      <!-- Left Side: Full Image (50%) -->
      <div class="col-12 col-md-6 image-container">
        <div class="overlay d-flex flex-column justify-content-center align-items-center px-5 text-white text-center">
          <h1 class="display-4 fw-bold mb-3">CampusCashControl</h1>
          <p class="lead mb-0">Manages your University expense</p>
        </div>
      </div>

      <!-- Right Side: Login Form (50%) -->
      <div class="col-12 col-md-6 form-container d-flex justify-content-center align-items-center">
        <LoginForm />
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from "@/components/LoginForm.vue";

export default {
  components: {
    LoginForm,
  },
};
</script>

<style scoped>
/* Full Screen - No Scrolling */
.vh-100 {
  height: 100vh;
  overflow: hidden;
}

/* Left side: Full-screen image (50%) */
.image-container {
  background: url("https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1050&q=80") no-repeat center center;
  background-size: cover;
  height: 100vh; /* Full height */
  position: relative;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent overlay */
  height: 100%;
}

/* Right side: Login Form (50%) with gradient black background */
.form-container {
  background: linear-gradient(to top, #000c40 , #f0f2f0); /* Gradient background */
  height: 100vh; /* Full height */
  color: white; /* White text */
}

/* Responsive adjustments */
@media (max-width: 767.98px) {
  .image-container {
    height: 30vh; /* Reduced height on mobile */
  }
  
  .form-container {
    height: 70vh; /* More space for form on mobile */
  }
}
</style>