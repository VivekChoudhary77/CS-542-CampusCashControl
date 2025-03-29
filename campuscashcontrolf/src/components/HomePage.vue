<template>
  <div class="container-fluid p-0 vh-100">
    <div class="row no-gutters vh-100">
      <!-- Left Side: Full Image (50%) -->
      <div class="col-12 col-md-6 image-container"></div>

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
  background: url("https://plus.unsplash.com/premium_photo-1680807988328-7ba28ad24d9f?q=80&w=2071&auto=format&fit=crop&ixlib=rB-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D") no-repeat center center;
  background-size: cover;
  height: 100vh; /* Full height */
}

/* Right side: Login Form (50%) with gradient black background */
.form-container {
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.4)); /* Gradient background */
  height: 100vh; /* Full height */
  color: white; /* White text */
}

/* Form content styling */
.form-container .card {
  background-color: rgba(255, 255, 255, 0.9); /* Light transparent background */
  padding: 30px;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
}

.form-container h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.card h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}
</style>
