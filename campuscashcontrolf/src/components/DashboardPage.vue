<template>
  <div class="dashboard">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/dashboard">
          <img src="@/assets/CCC Dashboard Logo.png" alt="CampusCashControl" class="navbar-logo" />
        </router-link>
        <!-- Navbar Links -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/departments">Departments</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/upload">Upload</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/reports">Reports</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/UserAccess">User Access</router-link>
          </li>
        </ul>
        <!-- User Logo (Circular, no arrow) -->
        <div class="user-logo" ref="userLogo" @click.stop="toggleDropdown">
          <i class="fas fa-user"></i>
          <div v-show="dropdownVisible" class="logout-menu">
            <button class="logout-btn" @click="logout">Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <div class="content container">
      <h2>Welcome to the Dashboard</h2>
      <p>This is your dashboard content</p>
    </div>

    <!-- Footer -->
    <footer class="footer text-center">
      <p>&copy; 2025 CampusCashControl</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "DashboardPage",
  data() {
    return {
      dropdownVisible: false,
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("authenticated");
      this.$router.replace({ name: "home" });
    },
    handleClickOutside(event) {
      if (this.$refs.userLogo && !this.$refs.userLogo.contains(event.target)) {
        this.dropdownVisible = false;
      }
    }
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
    // Push a state and override back button behavior
    window.history.pushState(null, "", window.location.href);
    window.onpopstate = () => {
      window.history.go(1);
    };
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
    // Restore default back button
    window.onpopstate = null;
  }
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.navbar-logo {
  height: 40px;
  object-fit: contain;
}
.content {
  flex: 1;
  margin-top: 20px;
}
.navbar {
  padding: 10px 20px;
}
.container {
  text-align: center;
}
.user-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: white;
  border: 2px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  position: relative;
}
.user-logo i {
  font-size: 18px;
  color: #333;
}
.logout-menu {
  position: absolute;
  top: 45px;
  right: 0;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
.logout-btn {
  background: none;
  border: none;
  padding: 10px 15px;
  width: 100%;
  text-align: left;
  cursor: pointer;
}
.logout-btn:hover {
  background-color: #f8f9fa;
}
.footer {
  background-color: #f8f9fa;
  padding: 10px;
  border-top: 1px solid #e7e7e7;
}
</style>