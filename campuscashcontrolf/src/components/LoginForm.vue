<template>
  <div :class="['auth-wrapper', { 'is-dark': isDark }]">
    <div class="auth-brand">
      <div class="auth-brand-line" aria-label="CampusCashControl">
        <div class="auth-brand-icon" aria-hidden="true">
          <el-icon><WalletFilled /></el-icon>
        </div>
        <span class="auth-brand-name">CampusCashControl</span>
      </div>
      <div class="auth-brand-copy">
        <h2>{{ formMode === 'login' ? 'Welcome back' : formMode === 'signup' ? 'Create account' : 'Reset password' }}</h2>
        <p>{{ formMode === 'login' ? 'Enter your credentials to login to your account.' : formMode === 'signup' ? 'We just need a few details to get you started.' : 'Enter your email to receive a reset link.' }}</p>
      </div>
    </div>

    <el-alert
      v-if="message"
      :title="message"
      :type="messageType"
      :closable="false"
      show-icon
      class="alert-box"
    />

    <el-form label-position="top" class="auth-form" @submit.prevent="handleSubmit">
      <el-form-item label="Email" :error="emailError ? 'Please enter a valid email address' : ''">
        <el-input
          v-model="email"
          type="email"
          class="input-no-hover"
          placeholder="hi@yourcompany.com"
          autocomplete="username"
          @blur="validateForm"
          clearable
        />
      </el-form-item>

      <el-form-item
        v-if="formMode !== 'forgot'"
        :error="passwordError ? 'Password must be at least 8 characters long' : ''"
      >
        <template #label>
          <div class="password-label-row">
            <span>Password</span>
          </div>
        </template>
        <el-input
          v-model="password"
          class="input-no-hover"
          type="password"
          show-password
          autocomplete="current-password"
          placeholder="Please input password"
          @input="validatePassword"
        />
      </el-form-item>

      <el-form-item
        v-if="formMode === 'signup'"
        label="Confirm Password"
        :error="confirmPasswordError ? 'Passwords do not match' : ''"
      >
        <el-input
          v-model="confirmPassword"
          class="input-no-hover"
          type="password"
          show-password
          autocomplete="new-password"
          placeholder="Re-enter password"
          @input="validateConfirmPassword"
        />
      </el-form-item>

      <div v-if="formMode === 'login'" class="meta-row">
        <el-checkbox v-model="rememberMe">Remember me</el-checkbox>
        <el-button
          type="primary"
          text
          class="forgot-link"
          @click="setFormMode('forgot')"
        >
          Forgot password?
        </el-button>
      </div>

      <el-button
        type="primary"
        size="large"
        native-type="submit"
        class="submit-btn"
        :loading="isLoading"
        :disabled="formIsInvalid || isLoading"
      >
        {{ formMode === 'login' ? 'Sign in' : formMode === 'signup' ? 'Sign up' : 'Send reset link' }}
      </el-button>
    </el-form>

    <div v-if="formMode !== 'forgot'" class="or-divider">
      <span>Or</span>
    </div>

    <el-button v-if="formMode !== 'forgot'" class="google-btn" plain>
      Continue with Google
    </el-button>

    <p v-if="formMode === 'signup'" class="terms-text">
      By signing up you agree to our Terms.
    </p>

    <div class="switch-row">
      <template v-if="formMode === 'login'">
        <span>Don't have an account?</span>
        <el-button type="primary" text @click="setFormMode('signup')">Sign up</el-button>
      </template>
      <template v-else-if="formMode === 'signup'">
        <span>Already have an account?</span>
        <el-button type="primary" text @click="setFormMode('login')">Sign in</el-button>
      </template>
      <template v-else>
        <span>Remember your password?</span>
        <el-button type="primary" text @click="setFormMode('login')">Sign in</el-button>
      </template>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ElNotification } from "element-plus";
import { WalletFilled } from "@element-plus/icons-vue";
import { apiUrl } from "@/config/api";

export default {
  props: {
    isDark: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    WalletFilled,
  },
  data() {
    return {
      formMode: 'login', // 'login', 'signup', or 'forgot'
      email: "",
      password: "",
      confirmPassword: "",
      emailError: false,
      passwordError: false,
      confirmPasswordError: false,
      isLoading: false,
      message: '',
      messageType: 'info'
      ,
      rememberMe: false,
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
      ElNotification({
        title: "Signing in",
        message: "Please wait while we verify your credentials.",
        type: "primary",
      });

      axios.post(apiUrl('/token/'), {
        username: this.email,  // using email as username
        password: this.password,
      })  
      .then(response => {
        const { access, refresh } = response.data;
        sessionStorage.setItem('access_token', access);
        sessionStorage.setItem('refresh_token', refresh);
        sessionStorage.setItem("authenticated", "true");
        // Clear old persistent tokens if present from previous sessions.
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem("authenticated");
        this.message = "Login successful!";
        this.messageType = "success";
        ElNotification({
          title: "Login success",
          message: "Welcome back.",
          type: "success",
        });
        setTimeout(() => {  
          this.$router.replace("/dashboard");
        }, 1000);
      })
      .catch(error => {
        this.message = "Invalid credentials or login error";
        this.messageType = "error";
        console.error("Login error:", error.response?.data || error);
        ElNotification({
          title: "Login failed",
          message: "Invalid credentials or login error.",
          type: "error",
        });
      })
      .finally(() => {
        this.isLoading = false;
      });
    },
    // Real signup: call our /api/signup/ endpoint.
    handleSignup() {
      axios.post(apiUrl('/signup/'), {
        email: this.email,
        password: this.password,
        confirm_password: this.confirmPassword,
      })
      .then(response => {
        this.message = response.data.message || `Account created successfully for ${this.email}.`;
        this.messageType = "success";
        ElNotification({
          title: "Signup success",
          message: "Your account was created. You can now sign in.",
          type: "success",
        });
        // Reset fields and switch to login mode.
        this.email = "";
        this.password = "";
        this.confirmPassword = "";
        setTimeout(() => {
          this.setFormMode('login');
        }, 2000);
      })
      .catch(error => {
        this.message = "Signup failed. Please check the details";
        this.messageType = "error";
        console.error("Signup error:", error.response?.data || error);
        ElNotification({
          title: "Signup failed",
          message: "Please check the details and try again.",
          type: "error",
        });
      })
      .finally(() => {
        this.isLoading = false;
      });
    },
    handleForgotPassword() {
      if (this.email) {
        this.message = `Password reset link has been sent to ${this.email}`;
        this.messageType = "success";
        ElNotification({
          title: "Reset link sent",
          message: `Password reset link sent to ${this.email}`,
          type: "info",
        });
      } else {
        this.message = "Please enter your email address";
        this.messageType = "error";
        ElNotification({
          title: "Email required",
          message: "Please enter your email address.",
          type: "warning",
        });
      }
    }
  },
};
</script>

<style scoped>
.auth-wrapper {
  --auth-text: #1f2835;
  --auth-muted: #5f6d7d;
  --auth-input-bg: #ffffff;
  --auth-input-border: #d4dbe5;
  --auth-icon: #111827;
  --auth-divider: #748191;
  --auth-divider-line: rgba(109, 126, 146, 0.24);
  --auth-switch: #546273;
  --auth-terms: #6d7b8b;
  --auth-autofill-text: #111827;
  --auth-autofill-bg: #ffffff;
  background: #ffffff;
  color: var(--auth-text);
  width: 100%;
}

.auth-wrapper.is-dark {
  --auth-text: #e5edfb;
  --auth-muted: #9db0c9;
  --auth-input-bg: #000000;
  --auth-input-border: #304968;
  --auth-icon: #d8e6fb;
  --auth-divider: #a3b8d3;
  --auth-divider-line: rgba(142, 165, 194, 0.35);
  --auth-switch: #9fb5d1;
  --auth-terms: #9db0c9;
  --auth-autofill-text: #e5edfb;
  --auth-autofill-bg: #000000;
  background: #000000;
}

.auth-brand {
  display: grid;
  gap: 8px;
  margin-bottom: 14px;
  justify-items: center;
  text-align: center;
}

.auth-brand-line {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.auth-brand-icon {
  width: 42px;
  height: 42px;
  border-radius: 999px;
  border: 1px solid color-mix(in srgb, var(--auth-text) 18%, transparent);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--auth-text);
  background: color-mix(in srgb, var(--auth-input-bg) 76%, transparent);
  font-size: 1.2rem;
}

.auth-brand-name {
  font-size: 1rem;
  font-weight: 800;
  color: var(--auth-text);
}

.auth-brand-copy h2 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  line-height: 1.2;
}

.auth-brand-copy p {
  margin: 3px 0 0;
  font-size: 0.88rem;
  color: var(--auth-muted);
}

.auth-form {
  margin-top: 10px;
}

.alert-box {
  margin: 14px 0;
}

.password-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 8px;
}

.forgot-link {
  font-size: 0.78rem;
  padding: 0;
  height: auto;
}

.forgot-link:hover,
.forgot-link:focus,
.forgot-link:active {
  color: inherit !important;
  background: transparent !important;
}

.auth-form :deep(.input-no-hover .el-input__wrapper) {
  background-color: var(--auth-input-bg) !important;
  box-shadow: 0 0 0 1px var(--auth-input-border) inset !important;
  transition: none !important;
}

.auth-form :deep(.input-no-hover .el-input__wrapper:hover) {
  background-color: var(--auth-input-bg) !important;
  box-shadow: 0 0 0 1px var(--auth-input-border) inset !important;
}

.auth-form :deep(.input-no-hover.is-focus .el-input__wrapper) {
  background-color: var(--auth-input-bg) !important;
}

.auth-form :deep(.input-no-hover .el-input__inner) {
  background-color: var(--auth-input-bg) !important;
  color: var(--auth-text) !important;
}

.auth-form :deep(.input-no-hover .el-input__inner::placeholder) {
  color: var(--auth-muted) !important;
}

.auth-form :deep(.input-no-hover .el-input__inner:-webkit-autofill),
.auth-form :deep(.input-no-hover .el-input__inner:-webkit-autofill:hover),
.auth-form :deep(.input-no-hover .el-input__inner:-webkit-autofill:focus),
.auth-form :deep(.input-no-hover .el-input__inner:-webkit-autofill:active) {
  -webkit-text-fill-color: var(--auth-autofill-text) !important;
  box-shadow: 0 0 0 1000px var(--auth-autofill-bg) inset !important;
  -webkit-box-shadow: 0 0 0 1000px var(--auth-autofill-bg) inset !important;
  caret-color: var(--auth-autofill-text) !important;
  transition: background-color 99999s ease-out 0s;
}

.auth-form :deep(.el-input__suffix) {
  display: inline-flex;
  align-items: center;
}

.auth-form :deep(.el-input__suffix-inner) {
  display: inline-flex;
  align-items: center;
  color: var(--auth-icon) !important;
  opacity: 1 !important;
}

.auth-form :deep(.el-input__icon) {
  color: var(--auth-icon) !important;
  opacity: 1 !important;
}

.auth-form :deep(.el-form-item__label) {
  color: var(--auth-text) !important;
}

.auth-form :deep(.el-checkbox__label) {
  color: var(--auth-text) !important;
}

.meta-row {
  margin-top: -2px;
  margin-bottom: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.submit-btn {
  width: 100%;
  margin-top: 8px;
  font-weight: 700;
}

.or-divider {
  margin: 14px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--auth-divider);
  font-size: 0.78rem;
}

.or-divider::before,
.or-divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--auth-divider-line);
}

.google-btn {
  width: 100%;
  font-weight: 600;
}

.terms-text {
  margin: 11px 0 0;
  text-align: center;
  font-size: 0.74rem;
  color: var(--auth-terms);
}

.switch-row {
  margin-top: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: var(--auth-switch);
  font-size: 0.88rem;
}

.switch-row :deep(.el-button) {
  padding: 4px;
  height: auto;
  font-weight: 600;
}
</style>