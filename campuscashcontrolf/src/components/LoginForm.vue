<template>
  <div class="card">
    <!-- Form Header -->
    <h2 class="text-center mb-4">
      {{ formMode === 'login' ? 'Sign In' : formMode === 'signup' ? 'Create Account' : 'Reset Password' }}
    </h2>
    <p class="text-muted text-center mb-4">
      {{ formMode === 'login' ? 'Enter your credentials to access your account' :
        formMode === 'signup' ? 'Fill in the details to create your account' :
          'Enter your email to receive a reset link' }}
    </p>

    <!-- Alert Messages -->
    <div v-if="message" :class="`alert alert-${messageType} mb-4`">
      {{ message }}
    </div>

    <form @submit.prevent="handleSubmit">
      <!-- Email Field -->
      <div class="mb-3">
        <label for="email" class="form-label">Email:</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fa-solid fa-envelope"></i>
          </span>
          <input v-model="email" type="email" id="email" class="form-control" placeholder="your@email.com"
            @blur="validateForm" required />
          <button type="button" class="btn btn-outline-danger border-start-0" disabled v-if="emailError">
            <i class="fa-solid fa-exclamation-circle"></i>
          </button>
        </div>
        <div v-if="emailError" class="invalid-feedback">
          Please enter a valid email address
        </div>
      </div>

      <!-- Password Field - Not shown in forgot password mode -->
      <div v-if="formMode !== 'forgot'" class="mb-3">
        <div class="d-flex justify-content-between align-items-center">
          <label for="password" class="form-label">Password:</label>
          <button v-if="formMode === 'login'" type="button" class="btn btn-link text-decoration-none p-0"
            @click="setFormMode('forgot')">
            Forgot password?
          </button>
        </div>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fa-solid fa-lock"></i>
          </span>
          <input v-model="password" :type="showPassword ? 'text' : 'password'" id="password" class="form-control"
            :class="{ 'is-invalid': passwordError }" placeholder="••••••••" @input="validatePassword" required />
          <button type="button" class="btn btn-outline-secondary" @click="toggleShowPassword">
            <i :class="showPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
          </button>
        </div>
        <div v-if="passwordError" class="invalid-feedback">
          Password must be at least 8 characters long
        </div>
      </div>

      <!-- Confirm Password Field - Only shown in signup mode -->
      <div v-if="formMode === 'signup'" class="mb-3">
        <label for="confirmPassword" class="form-label">Confirm Password:</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fa-solid fa-lock"></i>
          </span>
          <input v-model="confirmPassword" :type="showPassword ? 'text' : 'password'" id="confirmPassword"
            class="form-control" :class="{ 'is-invalid': confirmPasswordError }" placeholder="••••••••"
            @input="validateConfirmPassword" required />
          <button type="button" class="btn btn-outline-secondary" @click="toggleShowPassword">
            <i :class="showPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
          </button>
        </div>
        <div v-if="confirmPasswordError" class="invalid-feedback">
          Passwords do not match
        </div>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary w-100" :disabled="formIsInvalid || isLoading">
        <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
        {{ formMode === 'login' ? 'Sign In' : formMode === 'signup' ? 'Create Account' : 'Send Reset Link' }}
      </button>
    </form>

    <!-- Form Switch Options -->
    <div class="text-center mt-3">
      <template v-if="formMode === 'login'">
        Don't have an account?
        <button type="button" class="btn btn-link text-decoration-none" @click="setFormMode('signup')">
          Sign up
        </button>
      </template>
      <template v-else-if="formMode === 'signup'">
        Already have an account?
        <button type="button" class="btn btn-link text-decoration-none" @click="setFormMode('login')">
          Sign in
        </button>
      </template>
      <template v-else-if="formMode === 'forgot'">
        Remember your password?
        <button type="button" class="btn btn-link text-decoration-none" @click="setFormMode('login')">
          Sign in
        </button>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formMode: 'login', // 'login', 'signup', or 'forgot'
      email: "",
      password: "",
      confirmPassword: "",
      showPassword: false,
      emailError: false,
      passwordError: false,
      confirmPasswordError: false,
      isLoading: false,
      message: '',
      messageType: 'info'
    };
  },
  computed: {
    formIsInvalid() {
      if (this.formMode === 'login') {
        return this.emailError || this.passwordError || !this.email || !this.password;
      } else if (this.formMode === 'signup') {
        return this.emailError || this.passwordError || this.confirmPasswordError ||
          !this.email || !this.password || !this.confirmPassword;
      } else {
        // Forgot password mode
        return this.emailError || !this.email;
      }
    },
  },
  methods: {
    setFormMode(mode) {
      this.formMode = mode;
      this.message = '';
      this.emailError = false;
      this.passwordError = false;
      this.confirmPasswordError = false;
    },
    toggleShowPassword() {
      this.showPassword = !this.showPassword;
    },
    validateForm() {
      this.emailError = !this.isValidEmail(this.email);

      if (this.formMode !== 'forgot') {
        // Validate password field on blur or submit
        this.passwordError = this.password.length < 8;
      }

      if (this.formMode === 'signup') {
        // Ensure confirmPassword validation is run
        this.validateConfirmPassword();
      }

      // Return overall validity (this is not used explicitly)
      return !this.emailError &&
        (this.formMode === 'forgot' || !this.passwordError) &&
        (this.formMode !== 'signup' || !this.confirmPasswordError);
    },
    validatePassword() {
      // Live validation: if password length is 8 or more, clear the error.
      this.passwordError = this.password.length < 8;

      // In signup mode, validate confirmPassword too, so errors update as password changes
      if (this.formMode === 'signup') {
        this.validateConfirmPassword();
      }
    },
    validateConfirmPassword() {
      // When confirmPassword input changes, check that it matches password.
      this.confirmPasswordError = this.password !== this.confirmPassword;
    },
    isValidEmail(email) {
      const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      return regex.test(email);
    },
    handleSubmit() {
      // Final validation before submit
      if (!this.validateForm()) return;

      this.isLoading = true;
      this.message = '';

      setTimeout(() => {
        if (this.formMode === 'login') {
          this.handleLogin();
        } else if (this.formMode === 'signup') {
          this.handleSignup();
        } else {
          this.handleForgotPassword();
        }
        this.isLoading = false;
      }, 1000);
    },
    handleLogin() {
      // For demo purposes
      if (this.email === "test@example.com" && this.password === "password123") {
        this.message = "Login successful!";
        this.messageType = "success";
        setTimeout(() => {
          this.$router.replace("/dashboard");
        }, 1000);
      } else {
        this.message = "Invalid credentials. Try: test@example.com / password123";
        this.messageType = "danger";
      }
    },
    handleSignup() {
      // Simulate account creation
      if (this.email && this.password && this.password === this.confirmPassword) {
        this.message = `Account created successfully for ${this.email}`;
        this.messageType = "success";
        // Reset fields
        this.email = "";
        this.password = "";
        this.confirmPassword = "";
        // Switch to login form after a delay
        setTimeout(() => {
          this.setFormMode('login');
        }, 2000);
      } else {
        this.message = "Please fill in all fields correctly";
        this.messageType = "danger";
      }
    },
    handleForgotPassword() {
      if (this.email) {
        this.message = `Password reset link has been sent to ${this.email}`;
        this.messageType = "success";
      } else {
        this.message = "Please enter your email address";
        this.messageType = "danger";
      }
    }
  },
};
</script>

<style scoped>
/* Form card styling */
.card {
  background-color: rgba(255, 255, 255, 0.9);
  /* Light background with transparency */
  border-radius: 10px;
  padding: 30px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  /* Subtle shadow */
}

/* Title in the form */
.card h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}

/* Invalid form feedback */
.invalid-feedback {
  display: block;
  color: #dc3545;
}

/* Button styling */
.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
  padding: 10px;
  font-weight: 500;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0b5ed7;
}

/* Input group styling */
.input-group-text {
  background-color: #f8f9fa;
  border-right: none;
}

.input-group .form-control {
  border-left: none;
}

.input-group .form-control:focus {
  border-color: #ced4da;
  box-shadow: none;
}
</style>