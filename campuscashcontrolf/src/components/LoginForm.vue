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

      <!-- Password Field -->
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

      <!-- Confirm Password Field - Only in signup mode -->
      <div v-if="formMode === 'signup'" class="mb-3">
        <label for="confirmPassword" class="form-label">Confirm Password:</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fa-solid fa-lock"></i>
          </span>
          <input v-model="confirmPassword" :type="showConfirmPassword ? 'text' : 'password'" id="confirmPassword"
            class="form-control" :class="{ 'is-invalid': confirmPasswordError }" placeholder="••••••••"
            @input="validateConfirmPassword" required />
          <button type="button" class="btn btn-outline-secondary" @click="toggleShowConfirmPassword">
            <i :class="showConfirmPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
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
import axios from 'axios';
export default {
  data() {
    return {
      formMode: 'login', // 'login', 'signup', or 'forgot'
      email: "",
      password: "",
      confirmPassword: "",
      showPassword: false,
      showConfirmPassword: false,
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
    toggleShowConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
    validateForm() {
      this.emailError = !this.isValidEmail(this.email);

      if (this.formMode !== 'forgot') {
        this.passwordError = this.password.length < 8;
      }

      if (this.formMode === 'signup') {
        this.validateConfirmPassword();
      }

      return !this.emailError &&
             (this.formMode === 'forgot' || !this.passwordError) &&
             (this.formMode !== 'signup' || !this.confirmPasswordError);
    },
    validatePassword() {
      this.passwordError = this.password.length < 8;
      if (this.formMode === 'signup') {
        this.validateConfirmPassword();
      }
    },
    validateConfirmPassword() {
      this.confirmPasswordError = this.password !== this.confirmPassword;
    },
    isValidEmail(email) {
      const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      return regex.test(email);
    },
    handleSubmit() {
      if (!this.validateForm()) return;

      this.isLoading = true;
      this.message = '';

      if (this.formMode === 'login') {
        this.handleLogin();
      } else if (this.formMode === 'signup') {
        this.handleSignup();
      } else {
        this.handleForgotPassword();
      }
    },
    // Real login: call JWT endpoint instead of dummy check.
    handleLogin() {
      axios.post('http://localhost:8000/api/token/', {
        username: this.email,  // using email as username
        password: this.password,
      })  
      .then(response => {
        const { access, refresh } = response.data;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        // Optionally set an authentication flag if you use one:
        localStorage.setItem("authenticated", "true");
        this.message = "Login successful!";
        this.messageType = "success";
        setTimeout(() => {  
          this.$router.replace("/dashboard");
        }, 1000);
      })
      .catch(error => {
        this.message = "Invalid credentials or login error.";
        this.messageType = "danger";
        console.error("Login error:", error.response.data);
      })
      .finally(() => {
        this.isLoading = false;
      });
    },
    // Real signup: call our /api/signup/ endpoint.
    handleSignup() {
      axios.post('http://localhost:8000/api/signup/', {
        email: this.email,
        password: this.password,
        confirm_password: this.confirmPassword,
      })
      .then(response => {
        this.message = response.data.message || `Account created successfully for ${this.email}.`;
        this.messageType = "success";
        // Reset fields and switch to login mode.
        this.email = "";
        this.password = "";
        this.confirmPassword = "";
        setTimeout(() => {
          this.setFormMode('login');
        }, 2000);
      })
      .catch(error => {
        this.message = "Signup failed. Please check the details.";
        this.messageType = "danger";
        console.error("Signup error:", error.response.data);
      })
      .finally(() => {
        this.isLoading = false;
      });
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
/* Keep your existing styling unchanged */
.card {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  padding: 30px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.card h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}
.invalid-feedback {
  display: block;
  color: #dc3545;
}
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