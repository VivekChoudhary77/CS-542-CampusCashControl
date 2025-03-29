<template>
  <div class="card">
    <h1 class="text-center">Login</h1>

    <form @submit.prevent="handleLogin">
      <!-- Email Field -->
      <div class="mb-3">
        <label for="email" class="form-label">Email:</label>
        <input
          v-model="email"
          type="email"
          id="email"
          class="form-control"
          :class="{'is-invalid': emailError}"
          required
        />
        <div v-if="emailError" class="invalid-feedback">
          Please enter a valid email address.
        </div>
      </div>

      <!-- Password Field -->
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input
          v-model="password"
          type="password"
          id="password"
          class="form-control"
          :class="{'is-invalid': passwordError}"
          required
        />
        <div v-if="passwordError" class="invalid-feedback">
          Password must be at least 6 characters long.
        </div>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary w-100" :disabled="formIsInvalid">Login</button>
    </form>

    <!-- Forgot Password Link -->
    <div class="text-center mt-3">
      <button class="btn btn-link text-dark" @click="forgotPassword">Forgot Password?</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      emailError: false,
      passwordError: false,
    };
  },
  computed: {
    formIsInvalid() {
      return this.emailError || this.passwordError || !this.email || !this.password;
    },
  },
  methods: {
    validateForm() {
      this.emailError = !this.isValidEmail(this.email);
      this.passwordError = this.password.length < 6;
    },
    isValidEmail(email) {
      const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      return regex.test(email);
    },
    handleLogin() {
      this.validateForm();
      if (!this.emailError && !this.passwordError) {
        // Dummy credential check
        if (this.email === "test@example.com" && this.password === "password123") {
          alert("Login successful!");
          // Use Vue router to navigate to the dashboard component
          this.$router.push("/dashboard");
        } else {
          alert("Invalid credentials. Try: test@example.com / password123");
        }
      }
    },
    forgotPassword() {
      alert("Forgot password clicked! Implement reset logic later.");
    },
  },
};
</script>

<style scoped>
/* Form card styling */
.card {
  background-color: rgba(255, 255, 255, 0.9); /* Light background with transparency */
  border-radius: 10px;
  padding: 30px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
}

/* Title in the form */
.card h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

/* Invalid form feedback */
.invalid-feedback {
  display: block;
  color: red;
}
</style>
