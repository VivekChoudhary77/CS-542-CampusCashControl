<template>
  <div class="auth-wrapper">
    <div class="auth-header">
      <h2>{{ formMode === 'login' ? 'Sign In' : formMode === 'signup' ? 'Create Account' : 'Reset Password' }}</h2>
      <p>
        {{ formMode === 'login' ? 'Enter your credentials to access your account' :
           formMode === 'signup' ? 'Fill in the details to create your account' :
           'Enter your email to receive a reset link' }}
      </p>
    </div>

    <el-alert
      v-if="message"
      :title="message"
      :type="messageType"
      :closable="false"
      show-icon
      class="alert-box"
    />

    <el-form label-position="top" @submit.prevent="handleSubmit">
      <el-form-item label="Email" :error="emailError ? 'Please enter a valid email address' : ''">
        <el-input
          v-model="email"
          type="email"
          placeholder="your@email.com"
          @blur="validateForm"
          clearable
        />
      </el-form-item>

      <el-form-item
        v-if="formMode !== 'forgot'"
        label="Password"
        :error="passwordError ? 'Password must be at least 8 characters long' : ''"
      >
        <template #label>
          <div class="password-label-row">
            <span>Password</span>
            <el-button
              v-if="formMode === 'login'"
              type="primary"
              text
              @click="setFormMode('forgot')"
            >
              Forgot password?
            </el-button>
          </div>
        </template>
        <el-input
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Enter password"
          @input="validatePassword"
        >
          <template #suffix>
            <el-button text @click="toggleShowPassword">
              <el-icon><component :is="showPassword ? Hide : View" /></el-icon>
            </el-button>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item
        v-if="formMode === 'signup'"
        label="Confirm Password"
        :error="confirmPasswordError ? 'Passwords do not match' : ''"
      >
        <el-input
          v-model="confirmPassword"
          :type="showConfirmPassword ? 'text' : 'password'"
          placeholder="Re-enter password"
          @input="validateConfirmPassword"
        >
          <template #suffix>
            <el-button text @click="toggleShowConfirmPassword">
              <el-icon><component :is="showConfirmPassword ? Hide : View" /></el-icon>
            </el-button>
          </template>
        </el-input>
      </el-form-item>

      <el-button
        type="primary"
        size="large"
        class="submit-btn"
        :loading="isLoading"
        :disabled="formIsInvalid || isLoading"
        @click="handleSubmit"
      >
        {{ formMode === 'login' ? 'Sign In' : formMode === 'signup' ? 'Create Account' : 'Send Reset Link' }}
      </el-button>
    </el-form>

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
import { View, Hide } from "@element-plus/icons-vue";

export default {
  components: {
    View,
    Hide,
  },
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
      ElNotification({
        title: "Signing in",
        message: "Please wait while we verify your credentials.",
        type: "primary",
      });

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
      axios.post('http://localhost:8000/api/signup/', {
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
  width: 100%;
}

.auth-header h2 {
  margin: 0;
  font-size: 1.65rem;
  font-weight: 700;
}

.auth-header p {
  margin: 10px 0 0;
  color: #5e6b79;
  font-size: 0.95rem;
}

.alert-box {
  margin: 18px 0;
}

.password-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.submit-btn {
  width: 100%;
  margin-top: 8px;
  font-weight: 700;
}

.switch-row {
  margin-top: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: #546273;
}

.switch-row :deep(.el-button) {
  padding: 4px;
}
</style>